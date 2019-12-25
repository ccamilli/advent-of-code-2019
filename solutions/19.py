# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 15:50:17 2019

@author: c.camilli
"""

import os
from copy import deepcopy
import numpy as np
import math
os.chdir("..\\inputs")

def parse_input(path):
    with open(path) as file:
        l = [int(v.rstrip('\n')) for v in file.read().split(',')]
    return l

code = parse_input('19.in')
#%%

class IntCode():
    def __init__(self, code, inputs):
        self._state = deepcopy(code)
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
grid = {}
extended_code = code + [0]*1000
affected = 0

def give_inputs_and_parse_output(x, y, computer):
    gen = computer.run()
    next(gen)
    computer._input.append(x)
    next(gen)
    computer._input.append(y)
    return next(gen)

def render_grid(grid):
    renderer = np.zeros((50, 50))
    for cell in grid:
        if grid[cell] == 1:
            renderer[cell[0]][cell[1]] = 1
    return renderer

#%% 
for x in range(50):
    for y in range(50):
        computer = IntCode(extended_code, [])
        out = give_inputs_and_parse_output(x, y, computer)
        if out == 1:
            affected += 1
        grid[(y, x)] = out
        
print("Answer for part 1 is", affected)

#%%
#put a high number here to approximate beam equation
#beam equation can be written as lb < x/y < ub
denom = 1e9

def find_lower_bound(denom):
    bound = 0
    power = math.ceil(np.log2(denom))
    while power >= 0:
        computer = IntCode(extended_code, [])
        fact = 2**power
        if give_inputs_and_parse_output(bound + fact, denom, computer) == 0:
            bound += fact
        power -= 1
    return bound/denom

def find_upper_bound(denom):
    bound = find_lower_bound(denom)*denom
    power = math.ceil(np.log2(denom))
    while power >= 0:
        computer = IntCode(extended_code, [])
        fact = 2**power
        if give_inputs_and_parse_output(bound + fact, denom, computer) == 1:
            bound += fact
        power -= 1
    return bound/denom
      
lb = find_lower_bound(denom)
ub = find_upper_bound(denom)
#%%
def guess(v):
    delta = v-1
    y = int(delta*(1+lb)/(ub-lb))
    x = int(ub*y - delta)
    return x, y

def test_constraints(x, y):
    return (x/y > lb) and (x/y < ub)

def test_upper_constraint(x, y):
    return (x/y) < ub

def test_lower_constraint(x, y):
    return (x/y) > lb

def solve(v):
    delta = v-1
    x, y = guess(v)
    while not (test_constraints(x+delta, y) and test_constraints(x, y+delta)):
        while not (test_lower_constraint(x, y+delta)):
            x += 1
        while not (test_upper_constraint(x+delta, y)):
            y += 1
    return (x, y)
    
x, y = solve(100)
ans2 = 10000*x + y
print("Answer for part 2 is", ans2)  
