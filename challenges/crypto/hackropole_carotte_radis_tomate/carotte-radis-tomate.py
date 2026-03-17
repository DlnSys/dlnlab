import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

key = os.urandom(32)
print("carotte = ", int.from_bytes(key) % 17488856370348678479)
print("radis   = ", int.from_bytes(key) % 16548497022403653709)
print("tomate  = ", int.from_bytes(key) % 17646308379662286151)
print("pomme   = ", int.from_bytes(key) % 14933475126425703583)
print("banane  = ", int.from_bytes(key) % 17256641469715966189)

flag = open("flag.txt", "rb").read()
E = AES.new(key, AES.MODE_ECB)
enc = E.encrypt(pad(flag, 16))
print(f"enc = {enc.hex()}")
