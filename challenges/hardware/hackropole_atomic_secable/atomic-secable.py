# Python regular imports
import time
from random import randrange
from ecdsa.ellipticcurve import Point, CurveFp
from ecdsa.curves import Curve

# Public files (challenge specific)
from machine import Machine
from machine_faulted import FaultedMachine
from assembly import assembly

# secp192k1
e = 0x23d2fde9fee99ad2f19d160d15156796ccde4a8152d09ac7
p = 0xfffffffffffffffffffffffffffffffffffffffeffffee37
n = 0xfffffffffffffffffffffffe26f2fc170f69466a74defd8d
a = 0
b = 3
Gx = 0xdb4ff10ec057e9ae26b07d0280b7f4341da5d1b1eae06c7d
Gy = 0x9b2f2f6d9c5628a7844163d015be86344082aa88d95e2f9d
curve = CurveFp(p, a, b)
G = Point(curve, Gx, Gy, n)


def keygen():
    d = randrange(n)
    P = d * G
    return d, P

def on_curve(x, y):
    return 0 == (pow(x, 3, p) + a * x + b - pow(y, 2, p)) % p

def sign(machine, d, e):
    machine.reset()
    machine.runCode()
    if machine.error:
        return 0, 0

    k = machine.exponent
    r = machine.R0 % n
    if k:
        s = (pow(k, -1, n) * (e + r * d))% n
        if on_curve(machine.R0, machine.R1):
            return r, s
    return 0, 0

if __name__ == "__main__":
    try:
        # Key generation
        d, P = keygen()
        print(f"Public key {P.x()}")

        # Get user input
        print("Enter the number of signatures you want")
        nbSignature = eval(input(">>> "))
        if nbSignature >= (1<<16) or nbSignature < 0:
            exit()
        print("Enter your list of faulted instructions (for instance xx yy zz):")
        L = input(">>> ")
        faults = [ int(x) for x in L.split() ]

        # Initialize
        code = open("ecdsa_keygen.asm").read().splitlines()
        code = assembly(code)
        machine = FaultedMachine(code, faults)
        for i in range(nbSignature):
            r, s = sign(machine, d, e)
            print(f"{i:5d} {r:#050x} {s:#050x}")

        # Check key recovery
        print("What was the signing key?")
        potential_d = int(input(">>> "))
        if d == potential_d:
            flag = open("flag.txt").read().strip()
            print(f"[+] Congrats! Here is the flag: {flag}")
        else:
            print("Nope!")
    except:
        print("Please check your inputs.")
