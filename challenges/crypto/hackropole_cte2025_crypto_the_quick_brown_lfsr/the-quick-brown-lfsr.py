import os
from random import randint
from secret import flag

# pip install wonderwords dahuffman
from dahuffman import HuffmanCodec
from wonderwords import RandomSentence

SIZE = 256
TAPS = 0x8000000000000000000000000000000000000000000000000000000000000001

class LFSR:
    """
    Simple LFSR that generates a random bit sequence
    """

    def __init__(self):
        self.state = randint(0, (1 << SIZE) - 1)

    def __next__(self) -> int:
        new_bit = (self.state & TAPS).bit_count() & 1
        out_bit = self.state & 1

        self.state >>= 1
        self.state |= new_bit << (SIZE - 1)

        return out_bit

    def __iter__(self):
        return self


class PRNG:
    """
    Uses the LFSR to generate random bytes
    """

    def __init__(self):
        self.drbg = LFSR()

    def __next__(self) -> int:
        r = 0
        for _ in range(8):
            r <<= 1
            r |= next(self.drbg)
        return r

    def __iter__(self):
        return self


def encrypt(message: str) -> tuple[HuffmanCodec, bytes]:
    """
    Uses a PRNG as a stream cipher to encrypt a message,
    Huffman-encoded for efficiency.
    """
    codec = HuffmanCodec.from_data(message)
    encoded = codec.encode(message)

    prng = PRNG()
    c = []
    for m, r in zip(encoded, prng):
        c.append(m ^ r)
    return codec, bytes(c)


if __name__ == '__main__':
    # We generate random sentences until we get enough length,
    # then we hide the flag inside and encrypt it.

    s = RandomSentence()
    message_length = 69420
    message = ""
    while len(message) < message_length:
        message += s.sentence() + ' '

    flag_index = randint(0, message_length)
    message = message[:flag_index] + flag + message[flag_index:]

    codec, ciphertext = encrypt(message)
    codec.save('output.codec')
    with open('output.txt', 'wb') as f:
        f.write(ciphertext)
