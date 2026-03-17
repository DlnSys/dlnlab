import sys
from pwn import remote, b64e

if len(sys.argv) != 4:
    print(f"Usage: {sys.argv[0]} <host> <port> <binary>")
    exit(1)

io = remote(sys.argv[1], int(sys.argv[2]))
content = open(sys.argv[3], 'rb').read()
io.sendline(b64e(content).encode()) 
print(io.recvall().strip().decode())
io.close()
