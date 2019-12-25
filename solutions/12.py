# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 14:02:36 2019

@author: c.camilli
"""

import os
import numpy as np
import math

os.chdir("..\\inputs")

def parse_line(l):
    return tuple([int(el.split('=')[1]) for el in l[1:-1].split(',')])

def parse_file(filename):
    with open(filename) as file:
        return [parse_line(el.rstrip('\n')) for el in file.readlines()]
    

class Asteroid():
    def __init__(self, p0):
        self.pos = p0
        self.v = (0, 0, 0)
        
    def update_position(self):
        x, y, z = self.pos
        vx, vy, vz = self.v
        self.pos = (x+vx, y+vy, z+vz)
        
    def get_kinetic_energy(self):
        return np.sum(np.abs(self.pos)) * np.sum(np.abs(self.v))
    
    def hash_state(self, coord):
        p = self.pos[coord]
        v = self.v[coord]
        return f'.{p}-{v}.'
        
        
        
class Simulation():
    def __init__(self, asteroids):
        self.asteroids = asteroids
        self.history = {}
        
    def update_all_velocities(self):
        n = len(self.asteroids)
        i, j = 0, 1
        while i<n:
            j = i+1
            while j<n:
                self.calculate_interaction(i, j)
                j+=1
            i+=1
                
    def update_all_positions(self):
        for asteroid in self.asteroids:
            asteroid.update_position()
                
                
    def calculate_interaction(self, i, j):
        x1, y1, z1 = self.asteroids[i].pos
        x2, y2, z2 = self.asteroids[j].pos
        vx1, vy1, vz1 = self.asteroids[i].v
        vx2, vy2, vz2 = self.asteroids[j].v
        ux, uy, uz = np.sign([x2-x1, y2-y1, z2-z1])
        self.asteroids[i].v = (vx1+ux, vy1+uy, vz1+uz)
        self.asteroids[j].v = (vx2-ux, vy2-uy, vz2-uz)
        
    def simulate(self, coord, nturns=1000000):
        for i in range(nturns):
            self.update_all_velocities()
            self.update_all_positions()
            state = self.hash_state(coord)
            if state in self.history:
                return i
            else:
                self.history[state] = 1

    def total_kinetic_energy(self):
        en = 0
        for asteroid in self.asteroids:
            en += asteroid.get_kinetic_energy()   
        return en
    
    def hash_state(self, coord):
        p_hash = ''
        for asteroid in self.asteroids:
            p_hash += asteroid.hash_state(coord)
        return p_hash
        
        
def gcd(a, b):
    return abs(a*b) // math.gcd(a, b)
        
s = Simulation([Asteroid(el) for el in parse_file('12.in')])
#%%       

#PART 1
s.simulate(0, nturns=1000)
ans1 = s.total_kinetic_energy()
print("Answer for part 1 is", ans1)

#%%

#PART 2
s = Simulation([Asteroid(el) for el in parse_file('12.in')])
ans2 = gcd(gcd(s.simulate(0), s.simulate(1)), s.simulate(2))
print("Answer for part 2 is", ans2)
    
    
    
    
    
    
    
    
    