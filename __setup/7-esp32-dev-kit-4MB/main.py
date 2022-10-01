import os

def file_or_dir_exists(filename):
    try:
        os.stat(filename)
    except OSError:
        return False
    else:
        return True
        
if file_or_dir_exists('/appsetup/setup_complete.txt'):        

    """ NETWORK SETUP """
    import mlbapp.network_setup

    """ NTP SETUP """
    #import mlbapp.ntp_setup

    """ Run MLB APP """
    import mlbapp.mlb_app_runner.py

else:
    import appsetup.setup.py








