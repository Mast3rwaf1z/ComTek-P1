# from network import LoRa
# import binascii
# print(binascii.hexlify(LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868).mac()))

from network import LoRa
import struct
import binascii
import socket
freq = 868100000
# freq = 902300000


# Initialize LoRa in LORAWAN mode.
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
#Setup the single channel for connection to the gateway
for channel in range(0, 72):
   lora.remove_channel(channel)
for chan in range(0, 8):
   lora.add_channel(chan,  frequency=freq,  dr_min=0,  dr_max=3)
#Device Address
dev_addr = struct.unpack(">l", binascii.unhexlify('00ba0064'))[0]       #   http://loratest.lanestolen.dk:8080/api/devices/{dev_eui}/getRandomDevAddr
#Network Session Key
nwk_swkey = binascii.unhexlify('c46d071ad49b09ce5d776f2981349ba0')      #   http://loratest.lanestolen.dk:8080/api/devices/{dev_eui}/keys
#App Session Key
app_swkey = binascii.unhexlify('00000000000000000000000000000000')
lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))
# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 3)
# make the socket non-blocking
s.setblocking(False)
