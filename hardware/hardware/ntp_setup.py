""" NTP - Setup
    We set the local time via ntp because we do not trust the device to store time
    ntpsettime does not support timezones, it defaults to UTC
    We calculate the non-UTC local time (NULT) in bb_app_runner using 'timezone'
    We submit *that* date to MLB API to get the game day date in UTC(z)
    We *that* ('game_datetime': '2023-04-06T17:10:00Z') to NULT to display the upcoming game time """


#EDT
timezone = -4
tz_name  = 'et'
clockmode = 12

def utc_to_local(_time):
    
    import time
    _w=_time.replace(':','-').replace('T','-').replace('Z','').split('-')
    _w.append('0')
    _w.append('0')
    _w = [ int(x) for x in _w ]
    _w=tuple(_w)
    utc_time = time.mktime(_w)


    # Constants
    DAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
    # Get MicroPython UTC epoch time in seconds.
    utc_time = time.mktime(_w)
    # Offset UTC by timezone using 3600 seconds per hour.
    local_time = utc_time + 3600 * timezone
    # Get local time's datetime tuple.
    yy, mo, dd, hh, mm, ss, wkd, yrd = [d for d in time.localtime(local_time)]
    # Set the RTC to local time.  (I don't think the uP docs are exactly right about this.)

    if hh >= 13:
        am_pm = 'p'
        hh    = hh - 12
    elif hh == 0:
        hh = 12
    else:
        am_pm = 'a'
            
    then_time = '%2.2d-%2.2d %1.1d:%2.2d' % (mo, dd, hh, mm, ) + am_pm
    return then_time

def main():
    
    import time
    import ntptime
    print("Local time before synchronization：%s" % str(time.localtime()))
    """ Thing can hang for a really long time if DNS is not working """
    """ https://github.com/micropython/micropython/issues/7137      """
    ntptime.host = "time.google.com"

    ntp_count=0
    while True:
        try:
            # This sets the RTC to UTC.
            ntptime.settime()
        except OSError as e:
            if 'ETIMEDOUT' in str(e):
                print('NTP timeout, retrying')
                ntp_count+=1
                print(f"NTP retry count {ntp_count}")
                time.sleep(1)
                if ntp_count > 4:
                    print("Fatal NTP Error")
                    import machine
                    machine.reset()
        else:
            print("Set Time to UTC")
            print("Local time after synchronization：%s" % str(time.localtime()))
            break
    
if __name__ == "__main__":
    
    main()    
    