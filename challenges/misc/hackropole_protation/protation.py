from random import randint

N = 8

rol = lambda val, r_bits, max_bits:						  \
  (val << r_bits%max_bits) & (2**max_bits-1) |			  \
  ((val & (2**max_bits-1)) >> (max_bits-(r_bits%max_bits)))

def check(N, S):
	rotations = [ randint(0, N - 1) for _ in range(2 ** N - 1) ]
	SS = [ rol(S[i], rotations[i], N) for i in range(2 ** N - 1) ]
	values = [0]
	tmp = 0
	for i in range(2 ** N - 1):
		tmp ^= SS[i]
		values.append(tmp)
	return len(set(values)) == 2 ** N

if __name__== "__main__":

	try:
		assert bin(N).count('1') == 1, "Error: N must be a power of 2."

		print("Enter your solution (as hex)")
		s = bytes.fromhex(input(">>> "))
		assert len(s) == 2 ** N - 1 and check(N, s)

		flag = open("flag.txt").read()
		print(f"Congrats!! Here is the flag: {flag}")

	except:
		print("Not Good.")
		exit(1)