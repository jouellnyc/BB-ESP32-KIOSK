"""
Credit: https://forum.micropython.org/viewtopic.php?t=12294&p=66757
"""

import network
import time
from .wifi_config import SSID, PSWD

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
while True:
	try:
		sta_if.connect(SSID,PSWD)
		time.sleep(2)
	except Exception as e:
		print(e)
	time.sleep(1)
	if sta_if.isconnected():
		print('Connected to Wifi') 
		break
time.sleep(2)
print(sta_if.ifconfig())
