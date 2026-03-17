from pwn import *
import numpy as np
import base64

HOST, PORT = "localhost", 4000

io = remote(HOST, PORT)

hello_signal = np.fromfile("signal.iq", dtype = np.complex64)

encoded_signal = base64.b64encode(hello_signal.tobytes())

io.recvuntil(b"> ")
io.sendline(encoded_signal)
print(io.recvline())

io.close()
