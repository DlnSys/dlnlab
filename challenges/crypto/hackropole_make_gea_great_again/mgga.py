#!/usr/bin/env python3
from collections import deque

def bytes_to_bitlist(bs):
    res = []
    for b in bs:
        for i in range(8):
            res.append((b >> i) & 1)
    return res

### F stores the 7-variable Boolean function whose ANF is:
#    x0 * x2 * x5 * x6 ^ x0 * x3 * x5 * x6 ^ x0 * x1 * x5 * x6 ^ x1 * x2 * x5 * x6 ^
#    x0 * x2 * x3 * x6 ^ x1 * x3 * x4 * x6 ^ x1 * x3 * x5 * x6 ^
#    x0 * x2 * x4 ^ x0 * x2 * x3 ^ x0 * x1 * x3 ^ x0 * x2 * x6 ^
#    x0 * x1 * x4 ^ x0 * x1 * x6 ^ x1 * x2 * x6 ^ x2 * x5 * x6 ^
#    x0 * x3 * x5 ^ x1 * x4 * x6 ^ x1 * x2 * x5 ^
#    x0 * x3 ^ x0 * x5 ^ x1 * x3 ^ x1 * x5 ^
#    x1 * x6 ^ x0 * x2 ^ x2 * x3 ^ x2 * x5 ^
#    x2 * x6 ^ x4 * x5 ^ x5 * x6 ^
#    x1 ^ x2 ^ x3 ^ x5
F = [
    0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1,
    0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1,
    1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1,
    0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1,
    0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1,
    0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0,
    1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1
]

class LFSR:
    def __init__(self, n, feedback):
        assert(len(feedback) > 0)
        self.n = n
        self.feedback = feedback
        self.R = deque(self.n * [0], self.n)
        self.clk = 0
    
    def __str__(self):
        return '{:016x}'.format(sum([v * 2 ** i for i, v in enumerate(self.R)]))

    def reset(self):
        for i in range(self.n):
            self.R[i] = 0
    
    def load(self, IN):
        while IN:
            self.clock(IN.pop())
        if all([b == 0 for b in self.R]):
            self.R[-1] = 1
    
    def clock(self, inp = 0):
        fb = self.R[-1] ^ inp
        # shift
        self.R.pop()
        self.R.appendleft(0)
        # feedback
        if fb == 1:
            for i in self.feedback:
                self.R[i] ^= fb
        # clock
        self.clk += 1

class S:
    def __init__(self):
        self.R   = deque(64 * [0], 64)
        self.clk = 0
    
    def __str__(self):
        return '{:016x}'.format(sum([v * 2 ** i for i, v in enumerate(self.R)]))

    def reset(self):
        for i in range(64):
            self.R[i] = 0
    
    def load(self, iv, dir, key):   
        IN  = []
        IN += bytes_to_bitlist(iv)
        IN += [dir & 1]
        IN += bytes_to_bitlist(key)
        IN += [ 0 ] * 128
        for b in IN:
            self.clock(b)
    
    def clock(self, inp):
        self.R[63] ^= self.f() ^ inp
        self.R.rotate()
        self.clk += 1
    
    def f(self):
        R = self.R
        return F[ R[60] | R[51] << 1 | R[41] << 2 | R[25] << 3 | R[21] << 4 | R[8] << 5 | R[0] << 6 ]

class MGGA:
    reg_size = [31, 32, 33]
    
    def __init__(self, fb):
        self.S = S()
        self.A = LFSR(31, fb[0])
        self.B = LFSR(32, fb[1])
        self.C = LFSR(33, fb[2])

    def __str__(self):
        s = ''
        s += self.S.__str__() + '\n'
        s += self.A.__str__() + '\n'
        s += self.B.__str__() + '\n'
        s += self.C.__str__() + '\n'
        return s

    def load(self, iv, dir, key):
        self.S.reset()
        self.A.reset()
        self.B.reset()
        self.C.reset()
        self.S.load(iv, dir, key)
        s = list(self.S.R)
        self.A.load(s[:])
        self.B.load(s[21:] + s[:21])
        self.C.load(s[42:] + s[:42])

    def gen(self, bl):
        Z = []
        for i in range(bl):
            A = self.A.R
            B = self.B.R
            C = self.C.R
            z  = F[ A[ 8] | B[ 4] << 1 | C[ 0] << 2 | A[ 9] << 3 | B[ 2] << 4 | C[32] << 5 | A[23] << 6 ]
            z ^= F[ B[19] | C[ 2] << 1 | A[17] << 2 | B[30] << 3 | C[13] << 4 | A[28] << 5 | B[26] << 6 ]
            z ^= F[ C[22] | A[30] << 1 | B[31] << 2 | C[29] << 3 | A[ 5] << 4 | B[10] << 5 | C[28] << 6 ]
            Z.append(z)
            self.A.clock()
            self.B.clock()
            self.C.clock()
        return Z

    def genByte(self):
        Z = self.gen(8)
        return sum(x * 2 ** i for i, x in enumerate(Z)).to_bytes(1, 'little')
