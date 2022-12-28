""" Send as much as possible to the screen as early as possible   """
""" If no error on the screen, likely it is a hw / screen problem """

from hardware.err_to_screen import errr
from hardware.config import screen 
from hardware.esp32_oled_2_8_inch import print_setup

print_setup("Booting Up...")

try:
    
    import os
    import time
    time.sleep(2)

    def file_or_dir_exists(filename):
        try:
            os.stat(filename)
        except OSError:
            return False
        else:
            return True

    mode='normal'

    if mode=="debug":

        pass

    else:

        if file_or_dir_exists('/appsetup/setup_complete.txt'):        

            """ NETWORK SETUP """
            print_setup("Network Setup ...")
            import hardware.network_setup

            """ NTP SETUP """
            print_setup("Time Setup ...")
            import hardware.ntp_setup
            hardware.ntp_setup.main()

            """ Run MLB APP """
            print_setup("Launch BB Kiosk ")
            if screen == 'ili9341':
                import mlbapp.mlb_app_runner_ili9341 as mlb_app_runner
            elif screen == 'oled': 
                import mlbapp.mlb_app_runner_oled as mlb_app_runner

        else:
            print_setup("Running Setup ...")
            import appsetup.setup

except Exception as e:
    
    from hardware.err_to_screen import print_err
    print_err(e)    
