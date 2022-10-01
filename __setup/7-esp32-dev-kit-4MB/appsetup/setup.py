
import network
ap = network.WLAN(network.AP_IF)
ap.config(essid="mlb32jc2", password='123456789')
ap.active(True)

""" INITIAL SETUP """
from . import microdot_runner
