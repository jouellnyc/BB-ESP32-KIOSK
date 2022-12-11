""" Send as much as possible to the screen as early as possible   """
""" If no error on the screen, likely it is a hw / screen problem """

from hardware.err_to_screen import errr

try:
    
    import os

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
            import hardware.network_setup

            """ NTP SETUP """
            import hardware.ntp_setup
            hardware.ntp_setup.main()

            """ Run MLB APP """
            import mlbapp.mlb_app_runner


        else:

            import appsetup.setup

except Exception as e:
    
    from hardware.err_to_screen import print_err
    print_err(e)
    