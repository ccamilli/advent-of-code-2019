# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 14:44:46 2019

@author: c.camilli
"""

from string import ascii_uppercase as upper

def parse_input(filename):
    with open(filename) as file:
        grid = [[c for c in line.rstrip('\n')] for line in file.readlines()]
    return grid

def find_letters(maze):
    letters = {}
    for iy, line in enumerate(maze):
        for ix, el in enumerate(line):
            if el in upper:
                letters[(iy, ix)] = el
    return letters

def find_portals(letters, maze):
    out_y = [0, len(maze)-2]
    out_x = [0, len(maze[0])-2]
    portals = {}
    for k, v1 in letters.items():
        iy, ix = k
        if (iy in out_y or ix in out_x):
            level = 'outer'
        else:
            level = 'inner'
        if (iy, ix+1) in letters:
            v2 = letters[(iy, ix+1)]
            try:
                if maze[iy][ix-1] == '.':
                    portals[(iy, ix)] = ((v1+v2), (iy, ix-1), level)
                else:
                    portals[(iy, ix+1)] = ((v1+v2), (iy, ix+2), level)
            except IndexError:
                portals[(iy, ix+1)] = ((v1+v2), (iy, ix+2), level)
        elif(iy+1, ix) in letters:
            v2 = letters[(iy+1, ix)]
            try:
                if maze[iy-1][ix] == '.':
                    portals[(iy, ix)] = ((v1+v2), (iy-1, ix), level)
                else:
                    portals[(iy+1, ix)] = ((v1+v2), (iy+2, ix), level)
            except IndexError:
                portals[(iy+1, ix)] = ((v1+v2), (iy+2, ix), level)
    return portals

def find_entrance_and_exit(portals):
    for k, v in portals.items():
        if v[0] == 'AA':
            entrance = v[1]
        elif v[0] == 'ZZ':
            exit_maze = v[1]
    return entrance, exit_maze

def warp(portals, coord):
    if coord not in portals:
        return (coord, None)
    else:
        door = portals[coord][0]
        if door in ['AA', 'ZZ']:
            return (portals[coord][1], None)
    for k, v in portals.items():
        if k!=coord and v[0] == door:
            return (v[1], v[0])
#%%
        
def adapted_bfs_search(from_point, to_point, maze, portals):
    frontier = [(from_point)]
    visited = set()
    length = 1
    while len(frontier) > 0:
        current_frontier, frontier = frontier, []
        for el in current_frontier:
            crd = el
            visited.add((crd))
            y, x = crd
            neighbors = [warp(portals, coord) for coord in 
                         [(y-1, x), (y+1, x), (y, x-1), (y, x+1)]
                         if maze[coord[0]][coord[1]] not in ['#', ' ']]
            neighbors = [n for n in neighbors 
                         if (n[0])
                         not in visited]
            for neighbor in neighbors:
                coord, _ = neighbor
                frontier.append((coord))
                if coord == to_point:
                    return length
        length += 1
        
            
maze = parse_input('..\\inputs\\20.in')
letters = find_letters(maze)
portals = find_portals(letters, maze)
entrance, exit_maze = find_entrance_and_exit(portals)
#%%
ans1 = adapted_bfs_search(entrance, exit_maze, maze, portals)
print("Answer for part 1 is", ans1)
#%%
def warp_level(portals, coord, level):
    if coord not in portals:
        return (coord, None, level)
    door = portals[coord][0]
    portal_type = portals[coord][2]
    new_level = level+1 if portal_type == 'inner' else level-1
    if door in ['AA', 'ZZ']:
        if level == 0:
            return (portals[coord][1], None, level)
        else:
            return (None, None, level)
    else:
        if new_level < 0:
            return (None, None, level)
        for k, v in portals.items():
            if k!=coord and v[0] == door:
                return (v[1], v[0], new_level)

def adapted_bfs_search_with_levels(from_point, to_point, maze, portals):
    frontier = [(from_point, 0)]
    visited = set()
    length = 1
    while len(frontier) > 0:
        current_frontier, frontier = frontier, []
        for el in current_frontier:
            crd, lvl = el
            visited.add((crd, lvl))
            y, x = crd
            neighbors = [warp_level(portals, coord, lvl) for coord in 
                         [(y-1, x), (y+1, x), (y, x-1), (y, x+1)]
                         if maze[coord[0]][coord[1]] not in ['#', ' ']]
            neighbors = [n for n in neighbors 
                         if (n[0], n[2])
                         not in visited and n[0] is not None]
            for neighbor in neighbors:
                coord, _, n_lvl = neighbor
                frontier.append((coord, n_lvl))
                if coord == to_point and n_lvl == 0:
                    return length
        length += 1

ans2 = adapted_bfs_search_with_levels(entrance, exit_maze, maze, portals)
print("Answer for part 2 is", ans2)