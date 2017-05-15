#!/usr/bin/python3
import socket
import sys


dest = str(sys.argv[1])
def main():
    try:
        for port in range(1, 1025):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((dest, port))
            if result == 0:
                print("Port{}   Open".format(port))
            sock.close()
    except socket.error:
        print("Could not connect to server..exiting")
        sys.exit()

if __name__ == "__main__":
	main()
