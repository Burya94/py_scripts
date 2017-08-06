#!/bin/env python3

import bz2
import os
import hashlib


CHUNK_DIR = "."    #dir where chunks are stored
ARCH_DIR = "archived_chunks" # dir for archivated chunks
CKS_DIR = "checksum" # dir for checksum files

#func for archivin with bz2
def archive_chunks(chunks):
    if ARCH_DIR not in os.listdir(os.getcwd()):
        os.mkdir(ARCH_DIR)
    for chunk in chunks:
        with open(chunk, 'rb') as data:
            content = data.read()
            compresed_content = bz2.compress(content)
        with open('{}/{}.bz2'.format(ARCH_DIR, chunk), 'wb') as flow:
            flow.write(compresed_content)
    return os.listdir(ARCH_DIR)

#func for checksum files with sha-256.
#mb it's better to use faster algorithm(md5, xxHash-fastest)
def count_checksum(archives):
    if CKS_DIR not in os.listdir(os.getcwd()):
        os.mkdir(CKS_DIR)
    for file in archives:
        checksum_md5 = hashlib.md5()
        with open('{}/{}'.format(ARCH_DIR, file), 'rb') as data:
            for chunk in iter(lambda: data.read(4096), b""):
                checksum_md5.update(chunk)
        with open('{}/{}_checksum'.format(CKS_DIR, file.split('.bz2')[0]), 'w') as flow:
            flow.write(checksum_md5.hexdigest())

def main():
    archive_chunks(os.listdir(CHUNK_DIR))
    archives = [files for files in os.listdir(ARCH_DIR) if '.bz2' in files]
    count_checksum(archives)

if __name__ == "__main__":
    main()