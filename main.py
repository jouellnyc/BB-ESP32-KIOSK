""" Send as much as possible to the screen as early as possible   """
""" If no error on the screen, likely it is a hw / screen problem """

""" Quickly Bail out if in debug """
mode = 'normal'
if mode=="debug":
    import sys
    sys.exit(0)

from hardware.screen_runner import display as d
d.print_setup("Booting Up...")

try:
    
    import os
    import time
    time.sleep(5)

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
        import bbapp.bb_app_runner
        
    else:
        """ Run the Setup """    
        d.print_setup("Running Setup ...")
        import appsetup.setup

except Exception as e:
    """ Dump to the screen """
    print(str(e))
    d.print_err(e)
    
    