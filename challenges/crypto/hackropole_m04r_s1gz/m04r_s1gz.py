#!/usr/bin/python3 -u

from Crypto.PublicKey import RSA
import secrets
import signal
import sys

class SecureSigner():
    def __init__(self):
        self.key = RSA.generate(2048)
        self.e, self.n, self.d = self.key.e, self.key.n, self.key.d

    def sign(self, m):
        return pow(m, self.d, self.n)

    def verify(self, m, sig):
        return pow(sig, self.e, self.n) == m

if __name__ == '__main__':
    s = SecureSigner()

    print("Can you beat us and forge a signature in less than 60 seconds?")
    signal.alarm(60)

    try:
        print(f"Here are your parameters:")
        print(f" - modulus n: {s.n}")
        print(f" - public exponent e: {s.e}")

        while True:
            try:
                m = int(input("Please enter a number to sign (or anything else to stop): "))
            except ValueError:
                break
            sig = s.sign(m)
            print(f"Signature: {sig}")
        
        challenge = secrets.randbelow(2 ** 24)
        print(f"Here is your challenge: {challenge}")
        
        signature = input("Enter the signature of the challenge: ")
        try:
            sig = int(signature, 10)
        except ValueError:
            print("Wrong signature format!")
            sys.exit(-1)
        
        if s.verify(challenge, sig):
            with open("flag.txt") as f:
                flag = f.read()
                signal.alarm(0)
                print(f"Here is your flag, fellow signer: {flag}")
        else:
            print("Try again :(")
            sys.exit(-1)
    except:
        sys.exit(-1)
