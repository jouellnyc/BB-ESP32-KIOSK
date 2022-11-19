"""
import mlbapp.esp32_oled as myoled 
import mlbapp.err2oled
"""

import os

def file_or_dir_exists(filename):
    try:
        os.stat(filename)
    except OSError:
        return False
    else:
        return True

mode='debug'

if mode=="normal":

    pass

else:

#    try:
        
    if file_or_dir_exists('/appsetup/setup_complete.txt'):        


        """ NETWORK SETUP """
        import mlbapp.network_setup

        """ NTP SETUP """
        import mlbapp.ntp_setup
        mlbapp.ntp_setup.main()

        """ Run MLB APP """
        import mlbapp.mlb_app_runner2


    else:

        import appsetup.setup.py
        
"""
    except Exception as e:
        #myoled.oled.fill(0)
        #myoled.oled.show()
        #mlbapp.err2oled.printout(str(e),myoled.oled)
        #myoled.oled.show()
        print(e)   
"""

