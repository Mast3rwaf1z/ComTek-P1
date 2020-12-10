# main.py -- put your code here!
# Mohamad Was here
import pycom
import time

pycom.heartbeat(False)
for i in range(2):
    pycom.rgbled(0x330033)
    time.sleep(1)
    pycom.rgbled(0x660066)
    time.sleep(1)
    pycom.rgbled(0x990099)
    time.sleep(1)
    pycom.rgbled(0xCC00CC)
    time.sleep(1)
    pycom.rgbled(0x990099)
    time.sleep(1)
    pycom.rgbled(0x660066)
    time.sleep(1)
    pycom.rgbled(0x330033)
    time.sleep(1)
    pycom.rgbled(0x000000)
    time.sleep(3)
