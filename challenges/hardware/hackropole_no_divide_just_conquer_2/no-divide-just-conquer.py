# Python regular imports
import gmpy2
from Crypto.Random.random import randrange

# Public files (challenge specific)
from machine import Machine
from machine_restricted import RestrictedMachine, SuperRestrictedMachine

def testKey(p, q, iq, dp, dq, e, d, N, size):
    if N != p * q:
        print(f"[!] Error! {N} is not {p * q}")
        return False

    if not gmpy2.is_prime(p):
        print(f"[!] Error! (p) {p}")
        return False

    if not gmpy2.is_prime(q):
        print(f"[!] Error! (q) {q}")
        return False

    if gmpy2.mod(q * iq, p) != 1:
        print("[!] Error! (iq)")
        return False

    if N.bit_length() != size:
        print(f"[!] Error! (N) {N}")
        return False

    m = randrange(N)
    if m != gmpy2.powmod(m, e * d, N):
        print("[!] Error!")
        return False

    if 0 != gmpy2.mod(m - gmpy2.powmod(m, e * dp, p), p):
        print("[!] Error!")
        return False

    if 0 != gmpy2.mod(m - gmpy2.powmod(m, e * dq, q), q):
        print("[!] Error!")
        return False

    return True

def randomPrimeE():
    size = [2, 4, 16, 256]
    size = size[randrange(4)]
    return gmpy2.next_prime(randrange((1 << size) - 1)) | 1

def correctness(code, machine):
    print("[+] Testing correctness...")

    primes = set()
    for _ in range(32):
        e = randomPrimeE()

        size = randrange(512, 1024 + 1, 32)
        print(f"{size = }, {e = }")
        c = machine(code, e, 1 << (size - 1))
        c.runCode()
        if c.error:
            print("[!] Error!")
            exit()

        if e != c.RB:
            print("[!] Error! (e)")
            exit()

        p  = c.R6
        q  = c.R7
        iq = c.R8
        dp = c.R9
        dq = c.RA
        d  = c.exponent
        N  = c.module
        primes.add(p)
        primes.add(q)

        if not testKey(p, q, iq, dp, dq, e, d, N, size):
            exit()

    if len(primes) != 1 << 6:
        exit()

    print("[+] Correct!")

def easy(code):
    correctness(code, Machine)
    flag_easy = open("flag_easy.txt").read().strip()
    print(f"[+] Congrats! Here is the easy flag: {flag_easy}")

def medium(code):
    correctness(code, RestrictedMachine)
    flag_medium = open("flag_medium.txt").read().strip()
    print(f"[+] Congrats! Here is the medium flag: {flag_medium}")

def hard(code):
    correctness(code, SuperRestrictedMachine)
    flag_hard = open("flag_hard.txt").read().strip()
    print(f"[+] Congrats! Here is the hard flag: {flag_hard}")

if __name__ == "__main__":
    try:
        print("Enter your bytecode in hexadecimal:")
        code = input(">>> ")

        while True:
            print("Which flag do you want to grab?")
            print("  0. Quit.")
            print("  1. Easy flag   - learn to implement RSA Key Generation.")
            print("  2. Medium flag - RSA Key Generation without access to Extended Euclidean Algorithm.")
            print("  3. Hard flag   - RSA Key Generation without Extended Euclidean Algorithm, on constrained device.")
            choice = int(input(">>> "))

            if   choice == 0: exit()
            elif choice == 1: easy(code)
            elif choice == 2: medium(code)
            elif choice == 3: hard(code)

    except:
        print("Please check your inputs.")
