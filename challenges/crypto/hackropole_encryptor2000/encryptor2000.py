import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from base64 import b64encode as b64e

flag = open("flag.txt", "rb").read()

def encrypt(key, ptxt):
	cipher = AES.new(key, AES.MODE_ECB)
	return cipher.encrypt(pad(b64e(ptxt), 16))

if __name__ == "__main__":
	key = os.urandom(16)
	for _ in range(2000):
		try:
			p = input(">>> ").encode()
			c = encrypt(key, p + flag)
			print(c.hex())
		except:
			pass
