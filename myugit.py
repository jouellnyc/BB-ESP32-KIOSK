"""
Based on https://github.com/turfptax/ugit/
"""
import os
import urequests
import json
import hashlib
import binascii
import machine
import time
import network

global internal_tree

user = "jouellnyc"
repository = "BB-ESP32-KIOSK"
token = ""

giturl = "https://github.com/{user}/{repository}"
call_trees_url = f"https://api.github.com/repos/{user}/{repository}/git/trees/main?recursive=1"
raw = f"https://raw.githubusercontent.com/{user}/{repository}/master/"
ignore_files = [
    "hardware/wifi_config.py",
    "hardware/config.py",
    "bbapp/team_id.py",
    "appsetup/setup_complete.txt",
]
ignore_dirs = ['images']
myugit_log='myugit.log'
def pull(f_path, raw_url):
    print(f"pulling {f_path} from github")
    # files = os.listdir()
    headers = {"User-Agent": "ugit-turfptax"}
    # ^^^ Github Requires user-agent header otherwise 403
    if len(token) > 0:
        headers["authorization"] = "bearer %s" % token
    r = urequests.get(raw_url, headers=headers)
    try:
        new_file = open(f_path, "w")
        new_file.write(r.content.decode("utf-8"))
        new_file.close()
    except:
        print("decode fail try adding non-code files to .gitignore")
        try:
            new_file.close()
        except:
            print("tried to close new_file to save memory durring raw file decode")


def pull_all(tree=call_trees_url, raw=raw):
    log = []
    os.chdir("/")
    tree = pull_git_tree()
    for i in tree["tree"]:
        print(i['path'])
        #Skip the files in ignore_files
        if i["path"] in ignore_files:
            print(f"ignoring {i['path']} due to ignore_files")           
            continue
        if any(x in i['path'] for x in ignore_dirs):
            print(f"ignoring {i['path']} due to ignore_dirs")
            continue
            #Skip Directories
        if i["type"] == "tree":
            continue
        try:
            pull(i["path"], raw + i["path"])
            log.append(i["path"] + " updated")
        except:
            log.append(i["path"] + " failed to pull")
    logfile = open(myugit_log, "w")
    logfile.write(str(log))
    logfile.close()
    time.sleep(10)
    print("resetting machine in 10: machine.reset()")
    machine.reset()
    
def pull_git_tree(tree_url=call_trees_url, raw=raw):
    headers = {"User-Agent": "ugit-turfptax"}
    # ^^^ Github Requires user-agent header otherwise 403
    if len(token) > 0:
        headers["authorization"] = "bearer %s" % token
    r = urequests.get(tree_url, headers=headers)
    tree = json.loads(r.content.decode("utf-8"))
    return tree
