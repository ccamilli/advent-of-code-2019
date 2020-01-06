# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 10:17:56 2019

@author: c.camilli
"""

import numpy as np
from PIL import Image

def parse_input(path):
    with open(path) as file:
        l = [int(v.rstrip('\n')) for v in file.read().split(',')]
    return l

code = parse_input('..\\inputs\\11.in')
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
            else:
                op, modes = self._run_instructions_and_update(op, modes)
        
class Robot():
    def __init__(self, start_color):
        self.grid = {(0, 0):(0, start_color)}
        self.pos = (0, 0)
        self.facing = 0
        
    def update_orientation(self, direction):
        if direction == 0:
            self.facing = (self.facing - 1)%4
        else:
            self.facing = (self.facing + 1)%4
            
    def advance(self):
        x, y = self.pos
        if self.facing == 0:
            self.pos = (x, y+1)
        elif self.facing == 1:
            self.pos = (x+1, y)
        elif self.facing == 2:
            self.pos = (x, y-1)
        else:
            self.pos = (x-1, y)
            
    
    def get_input_instructions(self):
        if self.pos not in self.grid:
            self.grid[self.pos] = (0, '.')            
        if self.grid[self.pos][1] == '.':
            return 0
        else:
            return 1
        
    def paint_grid(self, color):
        times, char = self.grid[self.pos]
        if color == 0:
            self.grid[self.pos] = (times+1, '.')
        else:
            self.grid[self.pos] = (times+1, '#')
                     
    def run(self, code):
        code = code + [0]*100000
        inp = self.get_input_instructions()
        brain = IntCode(code, [inp])
        outputs = []
        for i, output in enumerate(brain.run(verbose=False)):
            outputs.append(output)
            if i%2 != 0:
                color, direction = outputs[i-1], outputs[i]
                self.paint_grid(color)
                self.update_orientation(direction)
                self.advance()
                brain._input.append(self.get_input_instructions())
                
    def render_grid(self):
        min_x, max_x = min(r.grid.keys(), key=lambda x: x[0])[0], max(r.grid.keys(), key=lambda x: x[0])[0]
        min_y, max_y =  min(r.grid.keys(), key=lambda x: x[1])[1], max(r.grid.keys(), key=lambda x: x[1])[1]
        width, height = (max_x - min_x), (max_y - min_y)
        grid = np.zeros((height+1, width+1))
        for k, v in self.grid.items():
            if v[1] == '#':
                grid[-k[1]][k[0]] = 1
        return grid
                
#%%
r = Robot(start_color = '.')
r.run(code)
ans1 = len(r.grid)
print("Answer for part 1 is", ans1)
#%%
r = Robot(start_color = '#')
r.run(code)
answer = r.render_grid()
im = Image.fromarray(np.array(255*(1-answer), dtype=np.uint8), 'L').resize((860, 120))
im.save("..\\outputs\\ans11.png")
im.show()
print("Check outputs\\ans11.png for part 2 answer")