""" The whole point of this file is to serve as an  abstraction/proxy such """
""" the all the app runner needs to do is import one variable: 'display'   """

""" All Devices  Need These """
from .config import screen

""" Break Down of Individual Personalities                """
if 'ili' in screen:
    
    from .ili9341_runner import display
                
elif screen == "lilygo_watch":

    from .lilygo_watch_1_54_inch import display

elif screen == 'esp32-s3-box-lite':

    from .espboxlite import display
    
