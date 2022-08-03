import network
import time
sta_if = network.WLAN(network.STA_IF)
time.sleep(3)
sta_if.active(True)
time.sleep(3)
sta_if.connect('SSID', 'PASS')
time.sleep(3)
sta_if.ifconfig()

