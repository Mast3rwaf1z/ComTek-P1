from network import LoRa
import binascii
lora = LoRa(mode=LoRa.LORAWAN,region=LoRa.EU868)
print(binascii.hexlify(lora.mac()))

app_eui = binascii.unhexlify("0000000000000000")
app_key = binascii.unhexlify("01020304050607080910111213141516")

print("DevEUI: %s" % binascii.hexlify(lora.mac()))
print("AppEUI: %s" % binascii.hexlify(app_eui))
print("AppKey: %s" % binascii.hexlify(app_key))

lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)

#ef51
#70b3d54993383389

#9401
#70b3d549997bb2a5
