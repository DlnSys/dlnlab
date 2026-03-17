import os
from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

def gen_curve(bits = 40, k = 4):
    assert bits*k >= 160, "Error: p**k must be at least 160 bits."
    p = random_prime(2 ** (bits + 1) - 1, lbound = 2 ** bits)
    R = Zmod(p**k)
    while True:
        a, b = R.random_element(), R.random_element()
        d = 4 * a ** 3 + 27 * b ** 2
        if d.is_unit():
            print("ici")
            E  = EllipticCurve(R, [a, b])
            E_ = EllipticCurve(GF(p), [a, b])
            if E_.order().is_prime():
                return E

def gen_random_point(E):
    R = E.base_ring()
    a, b = E.a4(), E.a6()
    while True:
        x = R.random_element()
        t = x ** 3 + a * x + b
        if is_square(t):
            y = choice([-1, 1]) * sqrt(t)
            return E([x, y])

def gen_pair(E):
    N = E.base_ring().characteristic()
    s = ZZ.random_element(N)
    P = gen_random_point(E)
    return P, s

def encrypt(s):
    k = sha256(str(s).encode()).digest()
    iv = os.urandom(16)
    flag = open("flag.txt", "rb").read().strip()
    c = AES.new(k, AES.MODE_CBC, iv).encrypt(pad(flag, 16))
    return iv, c

E = gen_curve()
print(f"E = {E}")

P, s = gen_pair(E)
print(f"P   = {P}")
print(f"s*P = {s * P}")

iv, c = encrypt(s)
print(f"iv = {iv.hex()}")
print(f"c  = {c.hex()}")
