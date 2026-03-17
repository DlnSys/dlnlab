#!/usr/local/bin/python3.8

from base64 import b64encode
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def sign(sk, m):
	mq, dq = m % sk.q, sk.d % (sk.q - 1)
	mp, dp = m % sk.p, sk.d % (sk.p - 1)
	s1 = pow(mq, dq, sk.q)
	s2 = pow(mp, dp, sk.p)
	h = (sk.u * (s1 - s2)) % sk.q
	s = (s2 + h * sk.p) % sk.n
	return s

if __name__ == "__main__":

	sk = RSA.generate(2048, e = 2**16 + 1)
	print("RSA public key:")
	print(f"n = {sk.n}")
	print(f"e = {sk.e}")

	while True:
		print("What do you want me to sign? (0 to exit)")
		try:
			m = int(input(">>> "))
			if m == 0:
				break
			print(sign(sk, m))
		except:
			break

	print("Now, prove you can decrypt this:")
	flag = open("flag.txt", "rb").read()
	flag_enc = PKCS1_OAEP.new(sk).encrypt(flag)
	print(b64encode(flag_enc).decode())
