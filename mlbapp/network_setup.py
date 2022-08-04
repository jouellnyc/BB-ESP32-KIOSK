"""
Credit: https://forum.micropython.org/viewtopic.php?t=12294&p=66757
"""

import network
import time
from .net_config import SSID, PSWD

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
while True:
	try:
		sta_if.connect(SSID,PSWD)
	except OSError as e:
		print(e)
	time.sleep(1)
	if sta_if.isconnected():
		print('Connected to Wifi') 
		break
time.sleep(3)
sta_if.ifconfig()
