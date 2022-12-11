import time
import network
essid="mlb32jc2"
ap = network.WLAN(network.AP_IF)
ap.config(essid=essid, password='123456789')
ap.active(True)
# The system completely blows up
# without  enough sleep after setting up 'ap'
time.sleep(5)

ip_addr = ap.ifconfig()[0]

from hardware.config import screen 

if screen == 'ili9341':
    """ OLED SETUP """
    from hardware.esp32_oled_2_8_inch import display, red, black, white, drk_grn
    from hardware.esp32_oled_2_8_inch import score_font, date_font, sm_font, draw_outline_box, clear_fill    
    from hardware.config import case
    if case == "upright":
        date_font=sm_font
        score_font=sm_font
    clear_fill()
    draw_outline_box()
    display.draw_text(5, 5,  'Setup at',      date_font,  white , drk_grn)
    display.draw_text(5, 45, 'http://',       score_font, white , drk_grn)
    display.draw_text(5, 85, f"{ip_addr}",    score_font, white , drk_grn)
    display.draw_text(5, 125, f"Wifi ssid:",  score_font, white , drk_grn)
    display.draw_text(5, 165, f"{essid}",     score_font, white , drk_grn)
elif screen == 'oled': 
    import mlbapp.esp32cam_oled
    mlbapp.esp32cam_oled.oled.text('Setup at '  ,0,0)
    mlbapp.esp32cam_oled.oled.text(f"http://"   ,0,17)
    mlbapp.esp32cam_oled.oled.text(f"{ip_addr}" ,0,34)
    mlbapp.esp32cam_oled.oled.show()

""" INITIAL SETUP """
import gc
gc.collect()
from . import microdot_runner