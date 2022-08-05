"""
# Esp-32 CAM (Bare) to OLED on bread board and on the Net.

PINS: https://stackoverflow.com/questions/71853347/interfacing-oled-to-esp32-cam
CODE: https://randomnerdtutorials.com/micropython-oled-display-esp32-esp8266/


Connect USB / FTDI programmer to esp-cam as per the link.
And then to OLED:

esp32cam OLED
IO15     sda
IO13     scl
"""

from machine import Pin, SoftI2C
from . import ssd1306
from time import sleep

i2c = SoftI2C(scl=Pin(13), sda=Pin(15))
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)