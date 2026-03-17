import os
import sys
import random
import string
import subprocess

def randomString(length = 16):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

REGISTERS = [
    "rax", "rbx", "rcx", "rdx", "rsi", "rdi",
    "r8", "r9", "r10", "r11", "r12", "r13", "r14", "r15",
]

try:
    addr = input("Address:  ")
    reg  = input("Register: ")

    addr = int(addr, 16)
    assert reg in REGISTERS

    rnd = randomString(length = 16).encode()
    cmd = [
        "/app/qemu-x86_64",
        "-plugin", f"/app/libexeclog.so,afilter={addr:#x},reg={reg}",
        "-d", "plugin", "/app/aes-distrace",
    ]
    proc = subprocess.Popen(cmd,
                            stdin = subprocess.PIPE,
                            stdout = subprocess.PIPE,
                            stderr = subprocess.PIPE)

    print(f"New challenge: {rnd.decode()}", file = sys.stderr)
    outs, errs = proc.communicate(input = rnd)

    for x in errs.decode().splitlines():
        print(x.strip())

    for x in outs.decode().splitlines():
        print(x.strip())

    r = input(">>> ").encode()
    if r == rnd:
        print(open("flag.txt").read())
    else:
        print("Nope.")

except:
    print("Error: Please check your inputs.")
    exit(0)
