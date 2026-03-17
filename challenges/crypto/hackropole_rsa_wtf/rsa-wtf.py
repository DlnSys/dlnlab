import os
import json
from Crypto.Util.number import GCD, getPrime
from Crypto.Random.random import getrandbits
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad

class RSA_WTF:
    def __init__(self):
        while True:
            try:
                self.k = getrandbits(666)
                self.p = getPrime(512)
                self.q = getPrime(512)
                self.dp = pow(self.k, -1, self.p - 1)
                self.dq = pow(self.k, -1, self.q - 1)
                break
            except:
                pass

    def encrypt(self, m):
        iv = os.urandom(16)
        k = SHA256.new(str(self.k).encode()).digest()
        E  = AES.new(k, AES.MODE_CBC, iv = iv)
        c = E.encrypt(pad(m, 16))
        return (iv.hex(), c.hex(), self.p, self.q, self.dp, self.dq)

flag = open("flag.txt", "rb").read()
assert len(flag) % 8 == 0

out = []
for i in range(0, len(flag), 8):
    bl = flag[i:i + 8]
    out.append(RSA_WTF().encrypt(bl))

print(json.dumps(out, indent = 4))
