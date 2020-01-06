# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 11:39:29 2019

@author: c.camilli
"""

import numpy as np
import random

def parse_input(path):
    with open(path) as file:
        l = [int(v.rstrip('\n')) for v in file.read().split(',')]
    return l

code = parse_input('..\\inputs\\15.in')

class IntCode():
    def __init__(self, code, inputs):
        self._state = code.copy()
        self._header, self.ninputs, self._relative_base = 0, 0, 0
        self._hOps = {1:lambda x, y: x+y, 2:lambda x, y: x*y}        
        self._verbose = False
        self._input = inputs
        
    def _solve_op_and_modes(self):
        opcode, modes = self._parse_instr()
        return opcode, [self._parse_modes(el) for el in modes]
            
    def _treat_op_modes(self, op, modes):
        if op in [1, 2]:
            modes[2](3, "update", self._hOps[op](modes[0](1), modes[1](2)))
        elif op == 3:
            modes[0](1, "update", self._input[self.ninputs])
            self._log(f"Wrote {self._input[self.ninputs]} to position {modes[0](1)}")
            self.ninputs += 1
        elif op == 4:
            self._output = modes[0](1)
            self._log(f"Output was set to {modes[0](1)}")
        elif op == 5:
            if modes[0](1) != 0:
                self._header = modes[1](2)
            else:
                self._header += 3
        elif op == 6:
            if modes[0](1) == 0:
                self._header = modes[1](2)
            else:
                self._header += 3
        elif op == 7:
            if modes[0](1) < modes[1](2):
                modes[2](3, "update", 1)
            else:
                modes[2](3, "update", 0)                
        elif op == 8:
            if modes[0](1) == modes[1](2):
                modes[2](3, "update", 1)
            else:
                modes[2](3, "update", 0)               
        elif op == 9:
            self._relative_base += modes[0](1)
                
    def _parse_instr(self):
        v = self._fetch1(0)
        self._log(f"Brute instruction is {v}")
        return v%100, [v//100%10, v//1000%10, v//10000%10]
                       
    def _parse_modes(self, var):
        if var == 0:
            return self._fetch0
        elif var == 1:
            return self._fetch1
        elif var == 2:
            return self._fetch2    
                                                           
    def _fetch0(self, offset, mode='regular', update_arg=0):
        if mode == 'regular':
            return self._state[self._state[self._header + offset]]
        else:
            self._state[self._state[self._header + offset]] = update_arg
    
    def _fetch1(self, offset, mode='regular', update_arg=0):
        if mode == 'regular':
            return self._state[self._header + offset]
        else:
            self._state[self._header + offset] = update_arg
    
    def _fetch2(self, offset, mode='regular', update_arg=0):
        if mode == 'regular':
            return self._state[self._state[self._header + offset] + self._relative_base]
        else:
            self._state[self._state[self._header + offset] + self._relative_base] = update_arg         
    
    def _update(self, op):
        if op in [1, 2, 7, 8]:
            self._header += 4
        elif op in [3, 4, 9]:
            self._header += 2
        self._log(f"Updated header to {self._header}")
    
    def _log(self, msg):
       if not self._verbose:
            pass
       else:
            print(msg)

    def _run_instructions_and_update(self, op, modes):
        self._log(f"Operation code is {self._fetch1(0)}")
        self._treat_op_modes(op, modes)
        self._update(op)
        return self._solve_op_and_modes()
    
    def _extend_memory(self, a):
        if (a<0):
            raise ValueError("Trying to access negative memory")
        else:
            while len(self._state) <= a:
                self._state.append(0)
        
    def run(self, verbose=False):
        self._verbose = verbose
        op, modes = self._solve_op_and_modes()
        while op != 99:
            if op == 4:
                op, modes = self._run_instructions_and_update(op, modes)
                yield self._output
            elif op == 3:
                yield "Please provide input"
                op, modes = self._run_instructions_and_update(op, modes)
            else:
                op, modes = self._run_instructions_and_update(op, modes)
    
class Robot():
    def __init__(self, computer):
        self.computer = computer
        self.grid = {(0, 0):'.'}
        self.position = (0, 0)
        self.last_move = None
        self.symbols = {'W':0, '.':1, 'T':2}
        self.last_update = 0
        
    def get_grid(self):
        positions = self.grid.keys()
        min_x, max_x = min(positions)[0], max(positions)[0]
        min_y, max_y = min(positions, key=lambda x: x[1])[1], max(positions,
                          key = lambda x: x[1])[1]
        offset_x = -min_x if min_x < 0 else 0
        offset_y = -min_y if min_y < 0 else 0
        grid_x, grid_y = max_x + offset_x, max_y + offset_y
        grid = np.empty((grid_y+1, grid_x+1))
        for i in range(grid_y+1):
            for j in range(grid_x+1):
                if (j-offset_x, i-offset_y) not in self.grid:
                    grid[i][j] = 9
                else:
                    grid[i][j] = self.symbols[self.grid[(j-offset_x, i-offset_y)]]
        grid[offset_y][offset_x] = 5
        return grid  
                
    def get_grid_position_from_movement(self, movement):
        if movement == 1:
            return (self.position[0], self.position[1] + 1)
        elif movement == 2:
            return (self.position[0], self.position[1] - 1)
        elif movement == 3:
            return (self.position[0] - 1, self.position[1])
        else:
            return (self.position[0] + 1, self.position[1])
        
    def get_legal_neighbors(self):
        return {self.get_grid_position_from_movement(m):m for m in [1, 2, 3, 4]}
    
    def execute_move(self, movement, output):
        moving_to = self.get_grid_position_from_movement(movement)
        if output == 0:
            self.grid[moving_to] = 'W'
            return 
        elif output == 1:
            self.grid[moving_to] = '.'
        else:
            self.grid[moving_to] = 'T'
        self.last_move = movement
        self.position = moving_to
        
    def decide_next_move(self):
        mirrored_moves = {1:2, 2:1, 3:4, 4:3}
        possibilities = self.get_legal_neighbors()
        #first priority: move not in grid
        priority_1 = [k for k in possibilities.keys() if k not in self.grid]
        if priority_1 != []:
            return possibilities[random.choice(priority_1)]
        #second priority: legal moves without coming back
        priority_2 = [k for k in possibilities.keys() if (self.grid[k]!='W' and 
                      mirrored_moves[possibilities[k]]!= self.last_move)]
        if priority_2 != []:
            return possibilities[random.choice(priority_2)]
        #otherwise just come back
        return mirrored_moves[self.last_move]
        
    def explore(self):
        gen = self.computer.run()
        for i in range(20000):
            next(gen)
            move = self.decide_next_move()
            self.computer._input.append(move)
            output = next(gen)
            self.execute_move(move, output)
             
def recursive_maze_solver(maze, origin, dest, tested):
    if origin == dest:
        return 0
    else:
        x, y = origin
        possibilities = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        valid_possibilities = [el for el in possibilities if 
                               (maze[el[0]][el[1]] in [1, 2] and el not in tested)]
        if valid_possibilities == []:
            return np.inf
        else:
            for el in valid_possibilities:
                tested.add(el)
                return 1 + min([
                recursive_maze_solver(maze, el, dest, tested) 
                for el in valid_possibilities])
                

computer = IntCode(code, [])
r = Robot(computer)
r.explore()   
maze = r.get_grid()
origin = tuple(np.argwhere(maze==5)[0])
destination = tuple(np.argwhere(maze==2)[0])
print("Answer for part 1 is", recursive_maze_solver(maze, origin, destination, set())) 

def spread_oxygen(maze):
    maze_copy = np.array(maze, dtype=np.int16)
    minutes = 0
    frontier = [tuple(np.argwhere(maze==2)[0])]
    while True:
        new_frontier = []
        for el in frontier:
            x, y = el
            neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
            for neighbor in neighbors:
                xn, yn = neighbor
                if maze_copy[xn][yn] not in [0, 2, 9]:
                    maze_copy[xn][yn] = 2
                    new_frontier.append(neighbor)
        frontier = new_frontier 
        if len(frontier) == 0:
            break
        else:
            minutes += 1
    return minutes
    
print("Answer for part 2 is", spread_oxygen(maze))
            
            
            
        
        
        
        
        
        
        
        
        