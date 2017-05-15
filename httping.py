#!/usr/bin/python3
import sys
import os
import socket
from urllib.parse import urlparse


URL = sys.argv[1]

def ping():
	name = urlparse(URL)
	ip = socket.gethostbyname(name.netloc)
	p = os.system("ping " + ip)


def main():
    try:
    	ping()
    except KeyboardInterrupt:
    	exit()

if __name__ == "__main__":
	main()
