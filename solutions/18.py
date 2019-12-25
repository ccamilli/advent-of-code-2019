# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 15:54:29 2019

@author: c.camilli
"""
import os
import string
import numpy as np
os.chdir('..\\inputs')

lower = string.ascii_lowercase
upper = string.ascii_uppercase

def parse_input(filename):
    with open(filename) as file:
        grid = [[c for c in line.rstrip('\n')] for line in file.readlines()]
    return grid

def find_keys(grid):
    keys = {}
    for i, line in enumerate(grid):
        for j, el in enumerate(line):
            if el.startswith('@') or el in lower:
                keys[el] = (i, j)
    return keys

def bfs_search(maze, from_point):
    coord = keys[from_point]
    frontier = [(coord, set())]
    visited = set()
    dist = 1
    while len(frontier) > 0:
        current, frontier = frontier, []
        for element in current:
            point, deps = element           
            visited.add(point)
            i, j = point
            neighbors = [el for el in [(i+1, j), (i-1, j),
                                       (i, j+1), (i, j-1)]
                         if maze[el[0]][el[1]] != '#' and el not in visited]
            for neigh in neighbors:
                fresh_deps = deps.copy()
                if maze[neigh[0]][neigh[1]] in upper:
                    fresh_deps = fresh_deps | {maze[neigh[0]][neigh[1]].lower()}
                if maze[neigh[0]][neigh[1]] in lower:
                    all_info[(from_point, maze[neigh[0]][neigh[1]])] = (dist, fresh_deps)   
                frontier.append((neigh, fresh_deps))
        dist+=1
        
def shortest_path_to_collect(start, to_collect):
    if len(to_collect) == 0:
        return 0
   
    key = (start, frozenset(to_collect))   
    if key in checked:
        return checked[key]
    
    dist = np.inf
    
    for r in to_collect:
        if not all_info[('@', r)][1].isdisjoint(to_collect):
            continue       
        n_dist = all_info[(start, r)][0] + shortest_path_to_collect(r,
                                                                     to_collect - {r})
        dist = min(dist, n_dist)
        
    checked[key] = dist       
    return dist

grid = parse_input('18.in')            
keys = find_keys(grid)

all_info = {}

for k in keys:
    bfs_search(grid, k)

checked = {}

ans1 = shortest_path_to_collect('@', {k for k in keys if k!='@'})

print("Answer for part 1 is", ans1)
#%%
entrance = keys['@']
updated_grid =  grid.copy()
i, j = entrance
updated_grid[i][j] = '#'
updated_grid[i-1][j] = '#'
updated_grid[i+1][j] = '#'
updated_grid[i][j-1] = '#'
updated_grid[i][j+1] = '#'
updated_grid[i-1][j-1] = '@1'
updated_grid[i-1][j+1] = '@2'
updated_grid[i+1][j-1] = '@3'
updated_grid[i+1][j+1] = '@4'
#%%
keys = find_keys(updated_grid)
all_info = {}

for key in keys:
    bfs_search(updated_grid, key)

def attribute_robot():
    keys_to_robot = {}
    search = [key for key in keys if not key.startswith('@')]
    robots = ['@1', '@2', '@3', '@4']
    for key in search:
        for robot in robots:
            if (robot, key) in all_info:
                keys_to_robot[key] = robot
    return keys_to_robot
            
keys_to_robot = attribute_robot()

checked = {}

def multi_robot_shortest_path(from_position, to_collect):
    if len(to_collect) == 0:
        return 0
    
    state = (frozenset(from_position), frozenset(to_collect))
    
    if state in checked:
        return checked[state]
    
    dist = np.inf
  
    for r in to_collect:
        matching_robot = keys_to_robot[r]
        
        if not all_info[(matching_robot, r)][1].isdisjoint(to_collect):
            continue
        
        new_position = from_position.copy()
        robot_index = int(matching_robot[1]) - 1
        
        delta = all_info[(from_position[robot_index], r)][0]
        
        new_position[robot_index] = r
        
        n_dist = delta + multi_robot_shortest_path(
            new_position, to_collect - {r})
        
        dist = min(dist, n_dist)
        
    checked[state] = dist
    return dist

ans2 = multi_robot_shortest_path(['@1', '@2', '@3', '@4'],
                                 {k for k in keys if not k.startswith('@')})
        
print("Answer for part 2 is", ans2)    

            
            
            
        

        