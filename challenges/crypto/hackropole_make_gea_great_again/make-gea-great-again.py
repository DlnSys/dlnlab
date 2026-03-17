print("Let's Make GEA Great Again!")

# Public packages
import os
import json
import galois
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from hashlib import sha256

# Challenge-specific import
from mgga import MGGA

DATA = 2 ** 18

print("Input three feedback polynomials of degree 31, 32 and 33")

pols = []
for i, d in enumerate(MGGA.reg_size):
    print(f"Input primitive polynomial in GF(2)[X] of degree {d} as an integer:")
    pol = int(input(">>> "))

    # The polynomial must be of degree d
    assert pol in range(2 ** d, 2 ** (d + 1)), f"Error: wrong degree ({d = })."

    # Extract exponents
    L = [i for i in range(pol.bit_length()) if (pol >> i) & 1]
    assert L[-1] == d

    # Ensure that the provided polynomial is primitive
    f = galois.Poly.Degrees(L)
    assert f.is_primitive(), "Error: polynomial is not primitive."

    # Keep this polynomial
    pols.append(L[:-1])

# Define MGGA
PRNG = MGGA(pols)

k = os.urandom(8)

data = []
for i in range(DATA):
    if i & 0xff == 0:
        print(f"{i:#04x}/{DATA - 1:#04x}")
    iv = i.to_bytes(4, 'little')
    PRNG.load(iv, 0, k)
    ks = b''.join([PRNG.genByte() for _ in range(8)])
    data.append(ks.hex())

flag = pad(open("flag.txt", "rb").read(), 16)
iv = os.urandom(16)
E = AES.new(sha256(k).digest(), AES.MODE_CBC, iv = iv)
enc = E.encrypt(flag)

print(json.dumps({
    "data": data,
    "flag": {
        "iv": iv.hex(),
        "enc": enc.hex(),
    }
}))
