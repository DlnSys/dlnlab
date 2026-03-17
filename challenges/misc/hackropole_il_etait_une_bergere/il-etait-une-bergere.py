# Python regular imports
from Crypto.Random.random import randrange

# Public files (challenge specific)
from machine import Machine

def test(code,e):
    c = Machine(code, e)
    c.runCode()
    if c.error:
        print("[!] Error!")
        exit()

    sqrt = c.R0
    if (e < sqrt ** 2) or (sqrt + 1) ** 2 <= e:
        print(f"[!] Error! {e} {sqrt}")
        exit()

if __name__ == "__main__":
    try:
        print("Enter your bytecode in hexadecimal:")
        code = input(">>> ")

        print("[+] Testing correctness...")
        test(code, 2 ** 4095)
        for _ in range(32):
            e = randrange(2 ** 4096)
            test(code, e)

        print("[+] Correct, congrats! Congrats! Here is the flag:")
        print(open("flag.txt").read().strip())

    except:
        print("Please check your inputs.")
