flag = open("flag.txt").read()
assert len(flag) == 64

x = "".join([
    flag[-8::-8],
    flag[-7::-8],
    flag[-6::-8],
    flag[-5::-8],
    flag[-4::-8],
    flag[-3::-8],
    flag[-2::-8],
    flag[-1::-8],
])
print(x[1::2] + x[0::2])
