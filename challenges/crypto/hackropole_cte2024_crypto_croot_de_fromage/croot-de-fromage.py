import os
from mpmath import mp, root

class StreamCipher:
    def __init__(self):
        self.N = 1024
        mp.dps = self.N
        while True:
            k = int.from_bytes(os.urandom(32))
            r = root(k, 3)
            if int(r) ** 3 != k:
                self.s = r - int(r)
                break

    def keystream(self):
        b, r = mp.mpf(2), 0
        for e in range(1, self.N + 1):
            c = int(self.s * b ** e)
            r = b * r + c
            self.s -= c * b ** -e
        return int(r)

    def encrypt(self, ptxt: bytes):
        assert len(ptxt) * 8 <= self.N, f"Error: plaintext is too long ({len(ptxt)} bytes)."
        return int.to_bytes(self.keystream() ^ int.from_bytes(ptxt), self.N // 8)

flag = open("flag.txt", "rb").read()
assert len(flag) == 64 and flag.startswith(b"CTE24{") and flag.endswith(b"}")

E = StreamCipher()
print(E.encrypt(flag).hex())
