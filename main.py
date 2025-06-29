""" Send as much as possible to the screen as early as possible   """
""" If no error on the screen, likely it is a hw / screen problem """

""" Quickly Bail out if in debug """
mode = 'normal'
if mode=="debug":
    import sys
    sys.exit(0)

from hardware.screen_runner import display as d

try:

    import os
    import time
             
    def upgrade():
        d.print_setup("Upgrading...")
        import hardware.network_setup
        import myugit
        d.print_setup("Updating...")
        myugit.pull_all()
   
    def file_or_dir_exists(filename):
        try:
            os.stat(filename)
        except OSError:
            return False
        else:
            return True
    
    d.print_setup("Booting Up...")
    time.sleep(5)
    
    if d.check_upgrade():
        upgrade()
        
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
        import bbapp.app.py

    else:
        """ Run the Setup """
        d.print_setup("Running Setup ...")
        import appsetup.setup

except Exception as e:
    """ Dump to the screen """
    print(str(e))
    d.scroll_print(text=e, scr_len=30, Error=True)    
