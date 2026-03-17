#!/usr/bin/env python3

# Install using pip:
#    pip install pwntools --break-system-packages
from pwn import *

'''
To use this template, execute the script with python3:
$ python3 template.py

If you want to run it with a different server and port, use
$ python3 template.py HOST=localhost PORT=4000

If you want to debug and see the data going exchanged, add "DEBUG":
$ python3 template.py DEBUG
'''

# Define the remote connexion details: server address and port
HOST = args.HOST or "chall.fcsc.fr"
PORT = args.PORT or 2053

# Connect to the remote server
# The variable "io" will be used to send and receive text to the remove server
io = remote(HOST, PORT)

# Receive 'Welcome to this introduction to pwntools!'
# We don't need to save it to a variable as there is no need to process this line
io.recvline()

# Receive "First, send me 'GO' after the '>>>' of the next line"
io.recvline()

# Then, we write "GO" after reading ">>> "
io.sendlineafter(b">>> ", b"Go!")

# Then, there are 2 lines containing some instructions.
# We don't need to save them.
io.recvlines(2)

# Now we need to extract a value from this line.
# It is of the form:
# 	"then I will write a number: add XXXX to it, then write the result back to me!",
# where XXXX is the value we need to extract.
val = io.recvline().strip().decode()
val = int(val[32:-41])

# Now, we need to read lines until b"===" (we read bytes, not strings)
io.recvuntil(b"===")

# Next, we receive a number, and we store it in x.
io.recvuntil(b"Here is a number: ")
x = io.recvline()

# It is currently stored in a variable of type "bytes".
# So we convert it first to a string.
x = x.decode().strip()

# And then to an integer.
x = int(x)

# Log what we have read (there is also `log.info()`, `log.error()`, etc.).
log.success(f"Read number: {x = }")

# We add val
x = x + val

# Convert the result to a byte string
x = str(x).encode()

# And finally send it back after reading ">>> "
io.sendlineafter(b">>> ", x)

# Receive the flag!
io.recvline()
flag = io.recvline().strip().decode()

# If needed, we can keep the connexion opened using io.interactive()
# Otherwise, we close the connexion
io.close()

# Print the flag
print(flag)
