#!/usr/bin/env python3

# Regular imports
import sys
import os.path
from random import randrange

# Challenge specific files
from minimum_distance import minimumDistanceOnCube # You do not have this file

class point:
    def __init__(self, P):
        self.coordinates = P

    def distance(self, P):
        if len(P.coordinates) != len(self.coordinates):
            return
        dist = 0
        for i, j in zip(self.coordinates, P.coordinates):
            dist += (i - j) ** 2
        return dist

    def __str__(self):
        return f"[{', '.join(str(x) for x in self.coordinates)}]"

class Cube:
    def __init__(self, length):
        self.length = length

    def randomPointOnSurface(self):
        j = randrange(3)
        l = []
        for i in range(3):
            if i == j:
                l += [ randrange(2) * self.length ]
            else:
                l += [ randrange(self.length) ]
        return point(l)

    def minimumDistance(self, P, Q):
        # You do not have the code for the "minimumDistanceOnCube" function.
        # The challenge is to write it.
        # The function minimumDistanceOnCube returns the square of the distance
        # between P and Q. For instance:
        #  * the minimal distance between P(0, 1, 2) and Q(0, 0, 0) is 5.
        #  * the minimal distance between P(0, 2, 14) and Q(32, 28, 11) is 3789.
        return minimumDistanceOnCube(self.length, P, Q)

if __name__=="__main__":
    try:
        c = Cube(32)
        for _ in range(1000):
            Alice = c.randomPointOnSurface()
            Bob   = c.randomPointOnSurface()
            print(f"Alice = {Alice}")
            print(f"Bob   = {Bob}")
            distance = int(input("Distance: "))
            if distance != c.minimumDistance(Alice, Bob):
                print("Nope!")
                exit(1)

        print("Congrats! Here is the flag:")
        print(open("flag.txt").read().strip())

    except:
        print("Please check your inputs.")
