#!/bin/env python3
import socket
import requests
import os
import sys


DESCRIPTION_FILE = './description.txt'
SERVER_ADDR = ''

def connect_to_server():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 9999
    client.connect((host, port))
    msg = client.recv(1024)
    client.close()
    print(msg)

def download(server_addr):
    #print "download description"
    r = requests.get(server_addr)
    #print r.status_code
    with open(DESCRIPTION_FILE, 'wb') as data:
        data.write(r.content)


def parse_description():
    print("parsing description file")
    dict = {}
    with open(DESCRIPTION_FILE, 'r') as data:
        content = data.readlines()
    for x in range(0, len(content), 2):
        dict[content[x].strip()] = content[x + 1].strip()
    return dict

def allocate_space(disk_space):
    print(disk_space)
    st = os.stat('D:')
    print(st)


def invoke_api():
    pass

def extract():
    pass

def generate_local_description():
    pass

def stop_script():
    pass

def ok_response_send():
    pass

def main():
    #download(SERVER_ADDR)
    parse_description()
    allocate_space(parse_description()['disk space'])


if __name__ == "__main__":
    main()