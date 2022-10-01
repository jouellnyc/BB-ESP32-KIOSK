"""
NOTE: All the legs of the LED must be pressed firmly into the bread board and have a good,
solid connection, otherwise the colors will 'bleed' and look awkward
"""

from machine import Pin 
g = Pin(14, Pin.OUT) 
b = Pin(12, Pin.OUT)
r = Pin(2, Pin.OUT) 


def all_on():
    g.value(1)
    r.value(1)
    b.value(1)
    
def all_off():
    g.value(0)
    r.value(0)
    b.value(0)
    
""" On boot turn off all the colors """
all_off()
    
