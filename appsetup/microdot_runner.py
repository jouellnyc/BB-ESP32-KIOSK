""" Inital Setup """
import uos
import machine

setup_file='/appsetup/setup_complete.txt'
wifi_file='/hardware/wifi_config.py'
team_file='/bbapp/team_id.py'

def write_wifi_creds(ssid, pswd):
    try:
        fh=open(wifi_file,'w')
        fh.write(f"SSID='{ssid}'\n")
        fh.write(f"PSWD='{pswd}'")
        fh.close()
    except Exception as e:
        return f'Cannot open {wifi_file} {str(e)}'
    else:
        return 0

def write_setup_file():
    try:
        fh=open(setup_file,'w')
    except Exception as e:
        return f'Cannot open {setup_file} {str(e)}' 
    else:
        return 0

def write_team_id(team_id):
    try:
        fh=open(team_file,'w')
        fh.write(f"team_id={team_id}\n")
        fh.close()
    except Exception as e:
        return f'Cannot open {team_id} {str(e)}'
    else:
        return 0

def get_team_data():
    import ujson
    with open("/bbapp/team_ids.py") as f:
        all_teams = f.read()
        all_team_ids = ujson.loads(all_teams)['teams']
        sorted_teams = sorted(all_team_ids, key=lambda d: d['name'])
    return ''.join([ '<option value="' + str(x['id']) + '">' + x['name'] + '</option>' for x in sorted_teams ])

option_list = get_team_data()

index_page='''<!doctype html>
              <html>
              <head>
              <title> Setup for BB APP</title>
              </head>
              <body>
              
              Welcome to Setup for the BB APP <BR>
              
              Please enter your SSID and password below:
              
              <form action="/setup/" method="POST" enctype="application/x-www-form-urlencoded">
              <br>
              SSID     <input type="text" name="ssid" >
              <P>
              Password <input type="text" name="password" enctype="application/x-www-form-urlencoded">
              
              
              <P>
              
               Please select Your Favorite Team: <P>
               
              <select name="team_id" id="team">
'''  + option_list + '''         
              </select>
              
              <br>
              <P>
              
              <input type="submit" value="Submit" style="height:50px; width:200px" />
                            
              <br>
              </form>
              </body>
              </HTML>
'''


setup_reply_page='''<!doctype html>
                  <HTML>
                  <head>
                      <title>  Wifi Setup Complete, Please Reboot </title>
                  </head>
                  
                  <body>
                      Wifi Setup Complete!
                      
                      Please Click Reboot button and then: <P>
                      
                      <OL>
                      <LI>Wait 60 seconds for the device to show your Team Score
                      <LI>Remember to put this device back on the original Wifi Network
                      </OL>
                      
                      This web page will NOT refresh!
                      
                      <P>
                      
                      <form action="/reboot/" method="GET">
                      <input type="submit" value="Reboot" style="height:50px; width:200px; font-size:30px">
                      </form>


                  </body>
                  </HTML>
                '''

from .microdot import Microdot
app = Microdot()


@app.route('/')
def index(request):
    return index_page, 200, {'Content-Type': 'text/html'}


@app.route('/setup/', methods=['POST'])
def setup(req):
    if req.method == 'POST':

        ssid     = req.form.get('ssid')
        password = req.form.get('password')
        team_id  = req.form.get('team_id')

        if ssid and password:
            pass
        else:
            return 'Please send Password and SSID', 200, {'Content-Type': 'text/html'}

        result = write_wifi_creds(ssid, password)
        if result == 0:
            pass
        else:
            return '<HTML><TITLE>Error</TITLE>' + result + '</HTML>', 200, {'Content-Type': 'text/html'}

        result =  write_team_id(team_id)
        if result == 0:
            pass
        else:
            return '<HTML><TITLE>Error</TITLE>' + result + '</HTML>', 200, {'Content-Type': 'text/html'}

        result = write_setup_file()
        if result == 0:
            return setup_reply_page, 200, {'Content-Type': 'text/html'}
        else:
            return '<HTML><TITLE>Error</TITLE>' + result + '</HTML>', 200, {'Content-Type': 'text/html'}
            

@app.route('/reboot/', methods=['GET'])
def reboot(req):
    machine.reset()
    
""" Start Microdot """
print("MicroDot Starting")
app.run(host='0.0.0.0', port=80)

