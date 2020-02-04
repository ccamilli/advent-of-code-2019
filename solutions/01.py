# -*- coding: utf-8 -*-
"""
@author: Caio Camilli
"""

from functools import reduce

with open("..\\inputs\\1.in") as file:
    l = [float(line.rstrip('\n')) for line in file]

ans1 = int(reduce(lambda x, y: x+y, map(lambda x: (x//3 - 2), l)))

print("Answer for part 1 is", ans1)

def recursive_fuel(m, acc):
    incr = (m//3 - 2)
    if incr <= 0:
        return acc
    else:
        return recursive_fuel(incr, acc + incr)
    
ans2 = int(reduce(lambda x, y: x+y, map(lambda x: recursive_fuel(x, 0), l)))
    
print("Answer for part 2 is", ans2)