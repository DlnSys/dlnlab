import random
from solution import solve # You do not have this file

L = [
	(    10,  4), (    10,  4), (    10,  4),
	(   100,  6), (   100,  6), (   100,  6),
	(   500,  8), (   500,  8), (   500,  8),
	(  1000, 11), (  1000, 11), (  1000, 11),
	( 10000, 16), ( 10000, 16), ( 10000, 16),
	( 20000, 20), ( 20000, 20), ( 20000, 20),
	( 50000, 21),
	(100000, 22),
]

print("We randomize arrays A of integers. For each of them, find the subarray A[i:j] with maximal sum.")

try:
	for n, N in L:
		seed = random.randrange(2 ** 32)
		print(f"{(seed, n, N) = }")

		random.seed(seed)
		A = [ random.randrange(-n, n) for _ in range(2 ** N) ]

		# You do not have the code for the "solve" function
		# The challenge is to write it
		m, x, y = solve(A)

		i = int(input(">>> i = "))
		j = int(input(">>> j = "))

		if sum(A[i:j]) != m:
			print(f"Nope! Maximal value was {m} = sum(A[{x}:{y}])")
			break
	else:
		print(open("flag.txt").read())
except:
	print("Please check your inputs.")
