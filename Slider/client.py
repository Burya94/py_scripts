#!/usr/bin/python

import socket
import urllib
import os
import sys
import datetime
import bz2
import hashlibs


WORKING_DIR = '.'
DESCRIPTION_FILE = WORKING_DIR + 'description.txt'
SERVER_ADDR = 'http://192.168.0.106/slider/'
ARCH_LOC = '.'
MD5_LOC = '.'
CHUNKS_DIR = '.'
description = {}



def connect_to_server():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 9999
    client.connect((host, port))
    msg = client.recv(1024)
    client.close()
    print(msg)


def download_description():
	urllib.urlretrieve(SERVER_ADDR + 'description.txt', DESCRIPTION_FILE)


def parse_description():
    print("parsing description file")
    with open(DESCRIPTION_FILE, 'r') as data:
        content = data.readlines()
    for x in range(0, len(content)):
        description[x] = content[x].strip()


def allocate_space(disk_space):
    st = os.statvfs('/')#os.stat #du = st.st_blocks * st.st_blksize
    free_space_kb = st.f_bavail * st.f_frsize / 1024 
    is_enough_space = True if free_space_kb > int(disk_space) else False
    return is_enough_space


def donwload_chunks(chunk):
    urllib.urlretrieve(SERVER_ADDR + '{}.md5'.format(chunk), MD5_LOC + '{}.md5'.format(chunk))
    urllib.urlretrieve(SERVER_ADDR + '{}.bz2'.format(chunk), ARCH_LOC + '{}.bz2'.format(chunk))
	

def repeat_download(current_md5, chunk):
	os.remove(MD5_LOC + '{}.md5'.format(chunk))
	os.remove(ARCH_LOC + '{}.bz2'.format(chunk))
	donwload_chunks(chunk)
	

def extract(chunk):
	with open(chunk, 'rb') as archive:
		content = archive.read()
		decomperess_data = bz2.decomperess(content)
	with open('{}/{}'.format(CHUNKS_DIR, chunk.split('.')[0]), 'wb') as part:
		part.write(decomperess_data)


def md5_generate(chunk):
    checksum_md5 = hashlib.md5()
    with open('{}/{}'.format(ARCH_LOC, '{}.bz2'.format(chunk)), 'rb') as data:
            for chunk_part in iter(lambda: data.read(4096), b""):
                checksum_md5.update(chunk_part)
        current_md5 = '{}/{}'.format(MD5_LOC, '{}.md5'.format(chunk))
        with open(current_md5, 'r') as md5:
        	if checksum_md5.hexdigest() != md5.readlines():
        		return False
            else:
            	return True
    

def generate_local_description():
    pass


def stop_script(error):
    print("It seems you have the next error:\n\
    	{0}-[ERROR]--{1}".format(datetime.datetime.now(), error))
    sys.exit()


def main():
    download_description()
    parse_description()
    if allocate_space(description[0]):
    	for number in range(description[1]):
    		chunk_name_prefix = '{}-{}'.format(chunk_name, number)
    	    donwload_chunks(chunk_name_prefix)
    	    count = 0
    	    while count < 5:
    	    	check_sum = md5_generate(chunk_name_prefix)
    	    	if check_sum:
    	    		break
    	    	elif not check_sum and count == 4:
    	    		stop_script('Attempted to download chunk 5 times with no succeed.')
    	    	else:
    	    		repeat_download(chunk_name_prefix)
    	    		count += 1
    	    extract(chunk_name_prefix)
    	    generate_local_description()


    else:
    	stop_script("Not enough space.")


if __name__ == "__main__":
    main()