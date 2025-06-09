import sh1106
from machine import Pin, SoftI2C

oled_width = 128
oled_height = 64
i2c2 = SoftI2C(scl=Pin(2), sda=Pin(0), freq=400000)
oled2 = sh1106.SH1106_I2C(oled_width, oled_height, i2c2, None, 0x3c,  rotate=180)
oled2.text('test', 0, 0)
oled2.show()
