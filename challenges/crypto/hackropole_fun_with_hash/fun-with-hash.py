#!/usr/bin/env python3

from hashlib import md5, sha1, sha256
from datetime import datetime

print("Try to login on my super safe computer! Be fast, you have at most 30 minutes.")

now = str(datetime.now())
print(now)

try:
	m = bytes.fromhex(input())
except:
	print("Access denied!")
	exit(1)

t = sha256(now.encode()).hexdigest()
if t.encode() not in m:
	print("Access denied!")
	exit(1)

if not md5(m).hexdigest().endswith("fc5c25"):
	print("Access denied!")
	exit(1)

if not sha1(m).hexdigest().endswith("fc5c25"):
	print("Access denied!")
	exit(1)

print("Welcome! Here is your flag:")
print(open("flag.txt").read())
