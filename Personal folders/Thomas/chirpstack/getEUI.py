from network import LoRa
import binascii
lora = LoRa(mode=LoRa.LORAWAN,region=LoRa.EU868)
print(binascii.hexlify(lora.mac()))

app_eui = binascii.unhexlify("0101010101010101")
app_key = "c4 6d 07 1a d4 9b 09 ce 5d 77 6f 29 81 34 9b a0"

print("DevEUI: %s" % binascii.hexlify(lora.mac()))
print("AppEUI: %s" % binascii.hexlify(app_eui))
print("AppKey: %s" % binascii.hexlify(app_key))

lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)
