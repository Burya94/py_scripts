#!/bin/env python3

import yaml
import subprocess
import sys



src = sys.argv[1]


f = open(src)
keys = yaml.load(f)
f.close()
new_env = {}
new_env['puppet::aws::credentials'] = {}

def decrypt_encrypt(aws_key):
    decrypted_aws = subprocess.check_output(['bash', 'decrypt.sh', aws_key.strip()])
    new_encrypted_aws = subprocess.check_output(['bash', 'encrypt.sh', decrypted_aws.strip().decode('ascii')])
    return new_encrypted_aws.decode('ascii').partition('OR')[0].strip()[8:]


for acc in keys['puppet::aws::credentials'].keys():
    aws_key = keys['puppet::aws::credentials'][acc]['aws_access_key_id']
    new_env['puppet::aws::credentials'][acc] = {}
    new_env['puppet::aws::credentials'][acc]['aws_region'] = 'us-east-1'
    new_env['puppet::aws::credentials'][acc]['aws_access_key_id'] = decrypt_encrypt(aws_key)
    secret_key =  keys['puppet::aws::credentials'][acc]['aws_secret_access_key']
    new_env['puppet::aws::credentials'][acc]['aws_secret_access_key'] = decrypt_encrypt(secret_key)

with open('./new_env.yaml', 'w') as yamlf:
    yaml.dump(new_env, yamlf, default_flow_style=False)





