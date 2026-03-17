#!/usr/bin/env python3

import socket
import zlib
import os
import sys

if len(sys.argv) != 4:
    print("Usage : client.py file ip port")
    exit()

try:
    file = open(sys.argv[1], "br")
except:
    print("File probleme")
    exit()

try:
    ip = sys.argv[2]
    port = int(sys.argv[3])

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
except:
    print("Network probleme")
    exit()

try:
    len_file = os.stat(sys.argv[1]).st_size

    assert len_file < 10000000

    len_file_str = str(len_file)

    sock.sendall(str(len(len_file_str)).encode()) # longeur de la longeur
    sock.sendall(len_file_str.encode()) # longeur

    for i in range((len_file // 2048) + 1):
        data = file.read(2048)
        sock.sendall(data)

except:
    print("File sending probleme")
    exit()

state = sock.recv(1).decode()

if state == "Y":
    print("file has been received by server ...")
    state = sock.recv(1).decode()

    if state == "Y":
        print("valid message response is generating ...")

        state = sock.recv(1).decode()

        if state == "Y":
            print("some signal appear ...")

            nb_len = sock.recv(1).decode()

            len_file = sock.recv(int(nb_len)).decode()

            output_file = open("output.f32", "wb+")

            blocks = []
            recvd = 0
            while recvd < int(len_file):
                recvbuf = sock.recv(int(len_file))
                recvd += len(recvbuf)
                blocks.append(recvbuf)

            sock.send(b"Y")

            for block in blocks:
                output_file.write(block)

            output_file.close()

        else:
            print("but signal does not appear /!\\")
    else:
        print("file is not analysed as a valid message /!\\")
else:
    print("file has not been received by server /!\\")
    
sock.close()
