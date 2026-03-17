# Python regular imports
import gmpy2
from random import randrange
from Crypto.Util.number import getPrime

# Public files (challenge specific)
from machine import Machine
from machine_faulted import FaultedMachine
from assembly import assembly

def RSAKeyGen(nbits, e):
    N = 2
    while N.bit_length() != nbits:
        p = getPrime(nbits // 2)
        q = getPrime(nbits // 2)
        N = p * q
    d = gmpy2.invert(e, (p - 1) * (q - 1))
    return N, d

def authenticate(c, M, N, d):
    c.R5 = d
    c.R6 = M
    c.exponent = 2
    c.module = N

    c.runCode()
    if c.error:
        return 0, c.nbInstruction

    return c.R2, c.nbInstruction

def verifyAuthentication(s, M, N, e):
    return M == gmpy2.powmod(s, e, N)

if __name__ == "__main__":
    nbits = 1024
    e = 65537
    N, d = RSAKeyGen(nbits, e)
    print(f"{N = }")

    code = open("RSA.asm").read().splitlines()
    code = assembly(code)

    for i in range(nbits):
        print("Enter the index of the instruction you want to fault")
        fault = [ int(input(">>> ")) ]
        machine = FaultedMachine(code, fault)
        M = randrange(N)
        s, n = authenticate(machine, M, N, d)
        print(f"{i:5d} {fault[0]:5d} {n:5d} {verifyAuthentication(s, M, N, e)}")
