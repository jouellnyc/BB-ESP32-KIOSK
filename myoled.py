from machine import Pin, SoftI2C
import ssd1306
from time import sleep

i2c = SoftI2C(scl=Pin(13), sda=Pin(15))
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
