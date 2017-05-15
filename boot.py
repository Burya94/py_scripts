import sys
import os
import json


def main ():
    if len(sys.argv) > 1 and ".json"  in sys.argv[1]:
        file_name = sys.argv[1]
        with open(sys.argv[1]) as data:
            jdat = json.loads(data.read())
        for node in jdat:
            os.system("knife bootstrap {} -x {} -P {} -N {} --sudo --run-list \'role[{}]\' ".format(node['fqdn'], node['user'], node['passw'], node['name'], node['role']))
    else:
        print("Specify json file!!Please!")
        sys.exit()

if __name__=="__main__":
    main()
