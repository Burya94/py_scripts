#!/usr/bin/python3

import os
import re


def main():
    
    file_name = os.listdir(path='../../Загрузки')
    
    pattern = '^Mr\.Robot.*'

    for i in file_name:
    	if re.match(pattern, i):
    		print(i)

if __name__ == "__main__":
    main()