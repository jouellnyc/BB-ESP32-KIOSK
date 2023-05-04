""" NTP - Setup
    We set the local time via ntp because we do not trust the device to store time
    ntpsettime does not support timezones, it defaults to UTC
    We calculate the non-UTC local date (NULD) in bb_app_runner using 'timezone' to find out what 'today' is
    We submit *that* date to MLB API to find the games for today and there start times (in UTC (z) )
    We convert *that* ('game_datetime': '2023-04-06T17:10:00Z') to NULT to display the upcoming game time """

#EDT
timezone = -4
tz_name  = 'et'


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
    yy, mo, dd, hh, mm, ss, wkd, yrd = list(time.localtime(local_time))
    # Set the RTC to local time.  (I don't think the uP docs are exactly right about this.)

    if hh >= 13:
        am_pm = 'p'
        hh    = hh - 12
    elif hh == 12:
        #JJO noon should be pm
        am_pm = 'p'
    else:
        am_pm = 'a'
    print('hh', hh)
    return '%2.2d-%2.2d %1.1d:%2.2d' % (mo, dd, hh, mm, ) + am_pm

def main():
    
    import time
    import ntptime
    print(f"Local time before synchronization：{str(time.localtime())}")
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
            print(f"Local time after synchronization：{str(time.localtime())}")
            break
    
if __name__ == "__main__":
    
    main()    
    