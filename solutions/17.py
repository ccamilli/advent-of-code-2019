# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 11:53:16 2019

@author: c.camilli
"""

import numpy as np

def parse_input(path):
    with open(path) as file:
        l = [int(v.rstrip('\n')) for v in file.read().split(',')]
    return l

code = parse_input('..\\inputs\\17.in')
#%%

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
        
    
    def run_fbl(self, verbose=False):
        self._verbose = verbose
        op, modes = self._solve_op_and_modes()
        while op not in [99, 4]:
            op, modes = self._run_instructions_and_update(op, modes)
        if op == 4:
            op, modes = self._run_instructions_and_update(op, modes)
        return (op == 99), self._output
#%%
def get_grid(code):
    robot = IntCode(code + [0]*100000, [])
    grid, line = [], []
    for out in robot.run():
        if out != 10:
            line.append(chr(out))
        else:
            grid.append(line)
            line = []
    return grid[:-1]
    
grid = get_grid(code)
    

def get_intersections(grid):
    inters = []
    for i, line in enumerate(grid):
        for j, el in enumerate(line):
            if grid[i][j]!='#':
                continue
            neigh = 0
            neighbors = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
            for el in neighbors:
                x, y = el
                try:
                    char = grid[x][y]
                except IndexError:
                    continue
                if char == '#':
                    neigh += 1
            if neigh > 3:
                inters.append((j, i))
    return inters
                
def get_alignment_params(inters):
    cumul = 0
    for inter in inters:
        x, y = inter
        cumul += x*y
    return cumul

ans1 = get_alignment_params(get_intersections(grid))

print("Answer for part 1 is", ans1)
#%%
def convert_grid(grid):
    a = np.zeros(shape=(len(grid), len(grid[0])))
    for i, line in enumerate(grid):
        for j, el in enumerate(line):
            a[i][j] = ord(el)
    return a

num_grid = convert_grid(grid)
#%%
class Robot():
    def __init__(self, grid):
        self.grid = grid
        self.directions = {'^':0, '>':1, 'v':2, '<':3}
        self.position, self.direction = self.find_starting_point()
        self.visited = set()
        self.path = []
        
    def find_starting_point(self):
        grid = self.grid
        for i, line in enumerate(grid):
            for j, el in enumerate(line):
                if el not in ['.', '#']:
                    return (i, j), self.directions[el]
                
    
    def explore_scaffold(self):
        while self.find_valid_neighbor() is not None:
            self.align_robot()
            self.advance()
        return self.path
    
    def is_scaffold(self, pos):
        y, x = pos
        try:
            return self.grid[y][x] == '#'
        except IndexError:
            return False
    
    def advance(self):
        counter = 1
        dels = {2:(+1, 0), 3:(0, -1), 0:(-1, 0), 1:(0, +1)}
        y0, x0 = self.position
        dy, dx = dels[self.direction]
        new_position = (y0+dy, x0+dx)
        while self.is_scaffold(new_position):
            self.position = new_position
            self.visited.add(self.position)
            counter += 1
            new_position = (y0+counter*dy, x0+counter*dx)
        counter -= 1
        self.path.append(str(counter))
        
                
    def align_robot(self):
        neighbor_direction = self.find_valid_neighbor()
        if neighbor_direction == (self.direction + 1)%4:
            self.path.append('R')
        elif neighbor_direction == (self.direction - 1)%4:
            self.path.append('L')       
        self.direction = neighbor_direction
        
    
    def find_valid_neighbor(self):
        y, x = self.position
        neighbors = {(y+1, x):2, (y, x-1):3, (y-1, x):0, (y, x+1):1}
        for neighbor, v in neighbors.items():
            try:
                if neighbor in self.visited: continue
                j, i = neighbor
                if self.grid[j][i] == '#':
                    return v
            except IndexError:
                continue
            
def convert_to_ascii(seq):
    l = [(ord(el)) for el in seq]
    l.extend([10])
    return l
#%%
#Brute force algorithm, several optimizations can be done but are not really necessary
def compress_path(path):
    n = len(path)
    dict_patterns = {}
    lengths = [10, 8, 6, 4]
    for length in lengths:
        for i in range(0, (n-length+1), 2):
            temp = ','.join(path[i:(i+length)])
            if temp in dict_patterns:
                count, ix, _ = dict_patterns[temp]
                ix.append(i)
                dict_patterns[temp] = (count+1, ix, length)
            else:
                dict_patterns[temp] = (1, [i], length)
    patt = {k:v for k, v in dict_patterns.items() if len(k) <= 20}
    for candidateA, vA in patt.items():
        cA, ixA, lenA = vA
        ixA = [(int(ix), lenA, 'A') for ix in ixA]
        for candidateB, vB in patt.items():
            cB, ixB, lenB = vB
            ixB = [(int(ix), lenB, 'B') for ix in ixB]
            for candidateC, vC in patt.items():
                cC, ixC, lenC = vC
                ixC = [(int(ix), lenC, 'C') for ix in ixC]
                all_ix = ixA + ixB + ixC
                all_ix.sort(key=lambda x: x[0])
                ok, cumul, indexes = True, 0, []
                for k, v, x in all_ix:
                    if k!=cumul:
                        ok = False
                        break
                    else:
                        cumul += int(v)
                        indexes.append(x)
                if ok:
                    return [','.join(indexes), candidateA, candidateB, candidateC] 
        
converted_routine = [el for p in compress_path(Robot(grid).explore_scaffold())
                     for el in convert_to_ascii(p)] + convert_to_ascii('n')

code[0] = 2
robot = IntCode(code + [0]*100000, [])
gen = robot.run()
i = 0  
try:
    while True:
        out = next(gen)
        while out == 'Please provide input':
            robot._input.append(converted_routine[i])
            i+=1
            out = next(gen)
except StopIteration:
    print("Answer for part 2 is", out)

    
        