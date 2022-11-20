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
        import mlbapp.network_setup

        """ NTP SETUP """
        import mlbapp.ntp_setup
        mlbapp.ntp_setup.main()

        """ Run MLB APP """
        import mlbapp.mlb_app_runner2


    else:

        import appsetup.setup.py