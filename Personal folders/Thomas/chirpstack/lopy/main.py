from network import LoRa
import pycom
import socket
import time
import ubinascii
import struct
# import adafruit_us100

# create an OTAA authentication parameters
dev_eui = ubinascii.unhexlify('be3f661454d53eae')           # possibly the wrong value but the uplink transmissions work without it
app_eui = ubinascii.unhexlify('0000000000000000')
app_key = ubinascii.unhexlify('c46d071ad49b09ce5d776f2981349ba0')
#app_key = ubinascii.unhexlify('cd4005ab70fa0a1e940cf29f7204b0e3')

# Initialise LoRa in LORAWAN mode.
#lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868, device_class=LoRa.CLASS_C)
# Restoring previous lora sessions
lora.nvram_restore()

# Join the network
if not lora.has_joined():
    lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0, dr=0)
    # lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0, dr=0)
    while not lora.has_joined():
        time.sleep(2)
        print('Not yet joined...')

print("Connected!")

# Create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# Set the LoRaWAN data rate to DR 0 = SF12BW125
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 0)

# make the socket blocking
# (waits for the data to be sent and for the 2 receive windows to expire)
s.setblocking(True)

battery = 93
fullness = 47
temperature = 26

pkg = struct.pack('Iib',battery,fullness,temperature)
# pkg = struct.pack('iii', 1, 2, 3)

#Send the package
try:
    s.send(pkg)
except OSError as e:
    if e.args[0] == 11:
        print("error sending")

# make the socket non-blocking (because if there's no data received it will block forever...)
s.setblocking(False)

while True:
    data = s.recv(64)
    lora.nvram_save()
    print(data)
#    if data == b'':
#        break
    time.sleep(1)
