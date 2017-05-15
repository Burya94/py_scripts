#!/usr/bin/python3
import sys
import os
import json


def json_to_data():
    machines_info = "C:/Users/artem_buria/.vagrant.d/data/machine-index/index"
    with open(machines_info) as data:
        jdat = json.loads(data.read())
    return jdat

def machines_act(action):
    json_data = json_to_data()
    for j in json_data['machines']:
        if json_data['machines'][j]['state'] == 'running' :
            machine = json_data['machines'][j]['name']
            print(machine + " is running right now. It will be {} soon.".format(action), end='\n')
            os.chdir(json_data['machines'][j]['vagrantfile_path'])
            os.system("vagrant {}".format(action))
            print(machine + " is stopped now", end='\n')

def main ():
    if len(sys.argv) == 1 or len(sys.argv) > 2:
        print("""
                WARNING!!!\n
         You must cpecify one and only one argument, it may be:\n
         destroy - to destroy all running machines;\n
         halt - to halt all running machines; """)
        sys.exit()
    elif sys.argv[1] == 'destroy':
        machines_act('destroy')
    elif sys.argv[1] == 'halt':
        machines_act('halt')

if __name__=="__main__":
    main()
