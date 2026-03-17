from sage.all import *
import os
import random

FLAG = os.getenv("FLAG", "CWTE{fake}")
recette = ["pain", "ananas", "croissant", "pain au chocolat"]

def getPrime(S):
    return random_prime(2 ** S - 1, False, 2 ** (S - 1))

S = 512
e = getPrime(S)

def ot(x, sk):
    p, q = sk
    y1 = GF(p)(x).sqrt() * random.choice([1, -1])
    y2 = GF(q)(x).sqrt() * random.choice([1, -1])
    return CRT([int(y1), int(y2)], [p, q])

def bake(mess):
    m = int.from_bytes(mess.encode())
    p, q, r = getPrime(S), getPrime(S), getPrime(S)
    o, n = r * q, p * q
    c = pow(m, e, o)
    return (c, e, n), (p, q)

if __name__ == "__main__":

    try:
        print("Welcome to the boulangerie, show me that you known the viennoiseries and I'll give you the drapeau")

        for i in range(64):
            print("What about this ?")
            a = random.choice(recette)

            pk, sk = bake(a)
            print("Et voila :", pk)

            b = int(input("Alors ? "))
            print("Pour you :", ot(b, sk))

            r = input("Alors alors ??? ")
            if r != a:
                print("You need to learn more about the langue of Moliere...")
                exit()

        print(FLAG)
    except:
        exit()
