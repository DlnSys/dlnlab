import sys
from Crypto.Cipher import AES
from Crypto.Util.strxor import strxor

N = 64

class Hash:
	def __init__(self):
		self.h = b"\x00" * 4

	def update(self, data):
		assert len(data) % 4 == 0 # TODO
		for i in range(0, len(data), 4):
			block = data[i:i+4] * 4
			h = self.h * 4
			self.h = strxor(strxor(h, block), AES.new(h, AES.MODE_ECB).encrypt(block))[:4]
		return self

	def digest(self):
		return self.h

S = set()
for i in range(4, 4 * (N + 1), 4):
	try:
		m = input(">>> Message #{:d}: ".format(i // 4))
		m = bytes.fromhex(m)
		assert len(m) == i

		H = Hash()
		S.add(H.update(m).digest())

	except:
		print("Error input.")
		exit(1)

if len(S) <= 6:
	print("Congratulations!! Here is your flag:")
	print(open("flag.txt", "r").read().strip())
elif len(S) < 12:
	print("Almost there!")
elif len(S) < 36:
	print("Keep it up!")
elif len(S) < 64:
	print("This is a good start, try again")
else:
	print("Nope!")
