""" These value are for the ESP32-S3-BOX as per Russ      """
""" https://github.com/orgs/micropython/discussions/10435 """
""" https://github.com/orgs/micropython/discussions/10391 """

import hardware.russ_config  as tft_config
ldisplay = tft_config.config(3)
ldisplay.init()

from machine import Pin, SPI
spi = SPI(1, baudrate=40000000, sck=Pin(7), mosi=Pin(6))

from .ili9341 import Display
display = Display(spi, dc=Pin(4), cs=Pin(5), rst=Pin(48), width=320, height=240, rotation=0)
""" At this point the ili9341 display driver takes over after being init'ed above """
