# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 10:45:41 2019

@author: c.camilli
"""

import os
import operator
from numpy import arctan, degrees

os.chdir("..\\inputs")

def parse_input(filename):
    with open(filename) as file:
        data = [v.rstrip('\n') for v in file.readlines()]
        return data
    
f = parse_input("10.in")
#%%
def gcd(a, b):
    while b!=0:
        t = b
        b = a%b
        a = t
    return a
#%%
class Problem():
    def __init__(self, grid):
        self.grid = grid
        self.max_height = len(grid)
        self.max_width = len(grid[0])
        self.asteroids = self.initialize_asteroids()
        self.checked = {}
        
    def initialize_asteroids(self):
        d = {}
        for j, line in enumerate(self.grid):
            for i, char in enumerate(line):
                if char == '#':
                    d[(i, j)] = 0
        return d
                
    def detect_asteroids(self):
        asteroids = self.asteroids.keys()
        for a in asteroids:
            for b in asteroids:
                if a!=b:
                    self.check_visibility(a, b)
                    
    def check_visibility(self, a, b):
        if a not in self.asteroids or b not in self.asteroids or a==b:
            return
        
        check_hash = self.generate_check_hash(a, b)
        
        if check_hash in self.checked:
            pass
        
        else:           
            del_x = (b[0] - a[0])
            del_y = (b[1] - a[1])
            
            greatest_divisor = (gcd(del_x, del_y))
            
            if greatest_divisor in [-1, 1]:
                self.asteroids[a] += 1
                self.asteroids[b] += 1
                self.checked[check_hash] = True
            
            else:   
                d_x = del_x//greatest_divisor
                d_y = del_y//greatest_divisor
                
                #checking collisions in the line between a and b
                if greatest_divisor < 0:
                    vals = range(-1, greatest_divisor, -1)
                else:
                    vals = range(1, greatest_divisor, 1)
                    
                collision = True
                
                for k in vals:
                    p = (a[0] + k*d_x, a[1] + k*d_y)
                    if p in self.asteroids:
                        collision = False
                    
                if collision:
                    self.asteroids[a] += 1
                    self.asteroids[b] += 1
                    
                self.checked[check_hash] = collision
                        
        return self.checked[check_hash]
            
    def generate_check_hash(self, a, b):
        left, right = sorted([a, b])
        return f"{left[0]}.{left[1]} - {right[0]}.{right[1]}"
    
    def is_in_grid(self, a):
        return (a[0] >= 0 and a[0] < self._max_width) and (a[1] >= 0 and a[1] < self.max_height)
    
    def vaporise_everything(self, source_asteroid, count):
        angles = {}
        vaporized = []
        for a in self.asteroids.keys():
            if a!=source_asteroid:
                angle = self.calculate_angle(source_asteroid, a)
                if angle in angles:
                    angles[angle].append(a)
                else:
                    angles[angle] = [a]
        
        order = sorted(angles.keys())
        
        for angle in order:
            angles[angle] = sorted(angles[angle],
                  key=lambda x: self.calculate_distance_from(source_asteroid, x),
                  reverse=True)
            
        
        while len(vaporized) < (len(self.asteroids.keys()) - 1):
            for angle in order:
                if angles[angle] != []:
                    vaporized.append(angles[angle].pop())
                    
        return vaporized[count-1]
            
    def calculate_distance_from(self, from_asteroid, to_asteroid):
        return (to_asteroid[0] - from_asteroid[0])**2 + (to_asteroid[1] - from_asteroid[1])**2
                
    def calculate_angle(self, from_asteroid, to_asteroid):
        del_y = from_asteroid[1] - to_asteroid[1]
        del_x = to_asteroid[0] - from_asteroid[0]
        if del_x == 0:
            if del_y >= 0:
                return 0.0
            else:
                return 180.0
        else:
            if del_x > 0:
                return 90.0 - degrees(arctan(del_y/del_x))
            else:
                return 270.0 - degrees(arctan(del_y/del_x))
            
    
    
#%%
#PART 1
p = Problem(f)
p.detect_asteroids()
ans1 = max(p.asteroids.items(), key = operator.itemgetter(1))
print("Answer for part 1 is", ans1[1])
#%%
#PART 2
ans2 = p.vaporise_everything(ans1[0], 200)
ans2 = 100*ans2[0] + ans2[1]
print("Answer for part 2 is", ans2)
    
    
        
        
        
            