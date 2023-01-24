"""
Credit: https://forum.micropython.org/viewtopic.php?t=12294&p=66757
"""

import time
import network

from .wifi_config import SSID, PSWD
#Can't import w/o import all of mdr
setup_file='/appsetup/setup_complete.txt'

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)

"""  We are not displaying  errors to the screen        """
"""  We just handle wifi errors magically at setup time """
"""  if the user mistypes the SSID password or if it is """
"""  changed to a non-working password                  """

count=0
while True:
    try:
        sta_if.connect(SSID,PSWD)
        time.sleep(2)
    except OSError as e:
        count+=1
        print(f"Wifi Err Count: {count}")
        time.sleep(2)
    except Exception as e:
        print(e)
    if sta_if.isconnected():
        print('Connected to Wifi') 
        break
    if count > 12:
        print("Fatal Wifi Error")
        import uos
        uos.remove(setup_file)
        import machine
        machine.reset()
time.sleep(2)
print(sta_if.ifconfig())