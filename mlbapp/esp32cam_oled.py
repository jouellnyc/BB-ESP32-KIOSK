#https://www.youtube.com/watch?v=hrdWvyhYyS8&ab_channel=anErik

from machine import Pin, SoftI2C
from . import ssd1306
from time import sleep

i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

if __name__ == "__main__":
    oled.text('hi',0,0)
    oled.show()
