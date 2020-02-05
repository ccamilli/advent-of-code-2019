# -*- coding: utf-8 -*-
"""
Created on Tue Dec 24 12:56:29 2019

@author: c.camilli
"""

#Manual inputs
PART_2_MINUTES_PASSED = 200

import numpy as np

def parse_file(filename):
    with open(filename) as f:
        l = [el for line in f.readlines() for el in line.rstrip('\n')]
    return np.array([1 if el == '#' else 0 for el in l]).reshape((5, 5))

l = parse_file('..//inputs//24.in')

def hash_l(l):
    hsh = 0
    flat = l.reshape(1, -1)
    for i, el in enumerate(flat[0]):
        hsh += el*(2**i)
    return int(hsh)

def simul(l):
    seen_states = {hash_l(l)}   
    while True:
        cp = l.copy()
        for iline, line in enumerate(l):
            for icol, element in enumerate(line):
                neighbors = [(iline-1, icol), (iline+1, icol),
                             (iline, icol-1), (iline, icol+1)]
                valid_neighbors = [el for el in neighbors if el[0]>=0 and el[0]<=4
                                   and el[1]>=0 and el[1]<=4]
                nbugs = 0
                for el in valid_neighbors:
                    nbugs += l[el]
                if element == 1 and nbugs != 1:
                    cp[(iline, icol)] = 0
                elif element == 0 and nbugs in [1, 2]:
                    cp[(iline, icol)] = 1

        hsh = hash_l(cp)
        if hsh in seen_states:
            print("Answer for part 1 is", hsh)
            break
        else:
            seen_states.add(hsh)
            l = cp.copy()
    return

simul(l)

class RecursiveGridSystem():
    
    def __init__(self, initial_grid, nlevels):
        self.state = np.zeros((2*nlevels, 5, 5))
        self.state[nlevels//2] = initial_grid.copy()
        self.initial_state = nlevels//2
        self.nlevels = nlevels
        
    def count_bugs_in_neighborhood(self, iz, iy, ix):
        total_bugs = 0
        natural_neighbors = [(iz, iy-1, ix), (iz, iy+1, ix),
                             (iz, iy, ix-1), (iz, iy, ix+1)]
        for el in natural_neighbors:
            z, y, x = el
            if y == -1:
                total_bugs += self.state[iz-1, 1, 2]
            elif x == -1:
                total_bugs += self.state[iz-1, 2, 1]
            elif y == 5:
                total_bugs += self.state[iz-1, 3, 2]
            elif x == 5:
                total_bugs += self.state[iz-1, 2, 3]
            elif (y, x) != (2, 2):
                total_bugs += self.state[el]
            elif (iy, ix) == (1, 2):
                total_bugs += self.state[iz+1, 0, :].sum()
            elif (iy, ix) == (3, 2):
                total_bugs += self.state[iz+1, 4, :].sum()
            elif (iy, ix) == (2, 1):
                total_bugs += self.state[iz+1, :, 0].sum()
            elif (iy, ix) == (2, 3):
                total_bugs += self.state[iz+1, :, 4].sum()

        return int(total_bugs)
        
        
    def simulate_one_step(self):
        new_state = self.state.copy()
        for z in range(1, self.nlevels):
            for y in range(5):
                for x in range(5):
                    if (y, x) == (2, 2):
                        continue
                    nbugs = self.count_bugs_in_neighborhood(z, y, x)
                    element = self.state[z, y, x]
                    if element == 1 and nbugs != 1:
                        new_state[z, y, x] = 0
                    elif element == 0 and nbugs in [1, 2]:
                        new_state[z, y, x] = 1
        self.state = new_state.copy()
        
    def simulate_n_steps(self, n):
        for i in range(n):
            self.simulate_one_step()
            
    def count_bugs(self):
        return np.sum(self.state)
            
nlevels = PART_2_MINUTES_PASSED * 2
system = RecursiveGridSystem(l, nlevels)

system.simulate_n_steps(PART_2_MINUTES_PASSED)
print("Answer for part 2 is", int(system.count_bugs()))

        
        
                
            
    