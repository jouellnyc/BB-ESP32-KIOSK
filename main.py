""" Send as much as possible to the screen as early as possible   """
""" If no error on the screen, likely it is a hw / screen problem """

import sys
from hardware.config import screen, gui_screen_types, mode
from hardware.screen_runner import display as d
if mode=="debug":
    sys.exit(0)

d.print_setup("Booting Up...")

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

    
    
    if file_or_dir_exists('/appsetup/setup_complete.txt'):        

        """ NETWORK SETUP """
        d.print_setup("Network Setup ...")
        import hardware.network_setup

        """ NTP SETUP """
        d.print_setup("Time Setup ...")
        import hardware.ntp_setup
        hardware.ntp_setup.main()

        """ Run BB APP """
        d.print_setup("Launch BB Kiosk ")
        if screen in gui_screen_types:
            import bbapp.bb_app_runner
        elif screen == 'oled': 
            import bbapp.mlb_app_runner_oled as mlb_app_runner
        print(screen)
    
    else:
        d.print_setup("Running Setup ...")
        import appsetup.setup


except Exception as e:
    print(str(e))
    d.print_setup(str(e))
    
