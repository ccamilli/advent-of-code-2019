# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 06:24:45 2019

@author: Caio Camilli
"""

#No manual inputs required for part 1

#Manual inputs required for part 2 (not sure they will vary though)
FROM_OBJECT = 'YOU'
TO_OBJECT = 'SAN'


def parse_input(filename):
    with open(filename) as file:
        ls = [el.rstrip('\n') for el in file.readlines()]
    return ls

ls = parse_input('..\\inputs\\6.in')

orbits = {el.split(')')[1]:el.split(')')[0] for el in ls}
bodies = orbits.keys()
ans1 = 0
for b in bodies:
    while b in orbits:
        ans1 += 1
        b = orbits[b]

print("Answer for part 1 is", ans1)

from_chain = []
to_chain = []

v = FROM_OBJECT
while v in orbits:
    from_chain.append(v)
    v = orbits[v]
    
v = TO_OBJECT
while v in orbits:
    to_chain.append(v)
    v = orbits[v]
    
i=-1
while from_chain[i] == to_chain[i]:
    i-=1
    
ans2 = len(from_chain) + len(to_chain) + 2*i
print ("Answer for part 2 is", ans2)

