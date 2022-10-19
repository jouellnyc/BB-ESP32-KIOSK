import time
import network
ap = network.WLAN(network.AP_IF)
ap.config(essid="mlb32jc2", password='123456789')
ap.active(True)
# The system completely blows up
# without  enough sleep after setting up 'ap'
time.sleep(5)

ip_addr = ap.ifconfig()[0]
import mlbapp.esp32_oled
mlbapp.esp32_oled.oled.text('Setup at '  ,0,0)
mlbapp.esp32_oled.oled.text(f"http://"   ,0,17)
mlbapp.esp32_oled.oled.text(f"{ip_addr}" ,0,34)
mlbapp.esp32_oled.oled.show()


""" INITIAL SETUP """
import gc
gc.collect()
from . import microdot_runner
