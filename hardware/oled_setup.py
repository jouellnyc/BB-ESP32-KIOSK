from machine import Pin, SoftI2C
from . import ssd1306
from . import sh1106 
from time import sleep

oled_width = 128
oled_height = 64

#Define Whatever OLEDs you have here

#ssd1306
i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=400000)
oled1 = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

#sh1106
i2c2 = SoftI2C(scl=Pin(25), sda=Pin(26), freq=400000)
oled2 = sh1106.SH1106_I2C(oled_width, oled_height, i2c2, None, 0x3c,  rotate=180)



