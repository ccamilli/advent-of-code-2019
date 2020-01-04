# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 06:24:45 2019

@author: Caio Camilli
"""

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

you_chain = []
santa_chain = []

v = 'YOU'
while v in orbits:
    you_chain.append(v)
    v = orbits[v]
    
v = 'SAN'
while v in orbits:
    santa_chain.append(v)
    v = orbits[v]
    
i=-1
while you_chain[i] == santa_chain[i]:
    i-=1
    
ans2 = len(you_chain) + len(santa_chain) + 2*i
print ("Answer for part 2 is", ans2)

