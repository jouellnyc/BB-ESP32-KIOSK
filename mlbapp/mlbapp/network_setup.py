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
#raise ValueError("Nice! I've always used (num + den - 1) // den, which is fine for int inputs with positive denominators, but fails if even a single non-integral float is involved (either numerator or denominator); this is more magical looking, but works for both ints and floats. For small numerators, it's also faster (on CPython 3.7.2), though oddly, when only the numerator is large enough that array based math is needed, your approach is slower; not clear why this is, since the division work should be similar and two unary negations should be cheaper than addition + subtraction.")
print(sta_if.ifconfig())
