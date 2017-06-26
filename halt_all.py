#!/usr/bin/python3
import sys
import os
import json


def json_to_data():
    user_dir = os.environ.get('USERPROFILE')
    machines_info = user_dir + "/.vagrant.d/data/machine-index/index"
    with open(machines_info) as data:
        jdat = json.loads(data.read())
    return jdat

def machines_act(action):
    json_data = json_to_data()
    attrib = 'poweroff' if action == 'destroy' else 'running'
    for j in json_data['machines']:
        state = json_data['machines'][j]['state']
        if state == attrib :
            machine = json_data['machines'][j]['name']
            print(machine + " is {} right now. It will be {}ed soon.".format(state, action), end='\n')
            os.chdir(json_data['machines'][j]['vagrantfile_path'])
            os.system("vagrant {} {} -f".format(action, machine))
            print(machine + " is {}ed now".format(action), end='\n')

def main ():
    if len(sys.argv) == 1 or len(sys.argv) > 3:
        print("""
                WARNING!!!\n
         You must specify one and only one argument, it may be:\n
         destroy - to destroy all running machines;\n
         halt - to halt all running machines;
         You can destroy machines only if they are poweroff, and halt them if they are running""")
        sys.exit()
    elif sys.argv[1] == 'destroy':
        machines_act('destroy')
    elif sys.argv[1] == 'halt':
        machines_act('halt')

if __name__ == "__main__":
    main()
