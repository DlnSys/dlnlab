import sys
from hashlib import sha256
sys.set_int_max_str_digits(31337)
try:
    a, b, c, x, y = [ int(input(f"{x} = ")) for x in "abcxy" ]
    assert a > 0
    assert a == 487 * c
    assert 159 * a == 485 * b
    assert x ** 2 == a + b
    assert y * (3 * y - 1) == 2 * b
    h = sha256(str(a).encode()).hexdigest()
    print(f"FCSC{{{h}}}")
except:
    print("Nope!")
