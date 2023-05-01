""" These value are for the ESP32-S3-BOX-LITE """
from machine import Pin, SPI
import time

from .ili9341 import color565, Display

dc=4
cs=5
rst=48
width=320
height=240
rotation=180

spi = SPI(1, baudrate=40000000, sck=Pin(7), mosi=Pin(6))
display = Display(spi, dc=Pin(dc), cs=Pin(cs), rst=Pin(rst), width=width, height=height, rotation=rotation)

