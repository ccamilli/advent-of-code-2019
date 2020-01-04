# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 08:36:42 2019

@author: c.camilli
"""

import numpy as np
from PIL import Image
import sys
import curses

np.set_printoptions(threshold=sys.maxsize)

def parse_input(path):
    with open(path) as file:
        l = [int(v.rstrip('\n')) for v in file.read().split(',')]
    return l

code = parse_input('..\\inputs\\13.in')
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
    
    
class Game():
    def __init__(self, computer):
        self.computer = computer
        self.symbols = {0:' ', 1:'W', 2:'#', 3:'_', 4:'O'}
        self.score = 0
        self.ball = ()
        self.pad = ()
        
    def run_game(self):
        outs = []
        inputs, j = 0, 0
        gen = self.computer.run()
        #ws = curses.initscr()
        #curses.curs_set(0)
        #w = curses.newwin(40, 40, 0, 0)
        #self.w = w
        #w.keypad(1)
        #w.timeout(0.5)
        #w.nodelay(1)
        #key = curses.KEY_LEFT
        #automatic_movements = {0:0, 1:curses.KEY_RIGHT, -1:curses.KEY_LEFT}
        try:
            while True:
                el = next(gen)
                while el != "Please provide input":
                    #self.render_grid() 
                    outs.append(el)
                    if (j-inputs)%3 == 2:
                        coord = (outs[j-inputs-2], outs[j-inputs-1])
                        if coord == (-1, 0):
                            self.score = el
                            #w.addstr(1, 0, f"Score: {el}")
                            #print(f"Current score is {el}")
                        else:
                            #self.w.addch(3+outs[j-inputs-1],
                            #             outs[j-inputs-2], self.symbols[el])
                            if el == 3:
                                self.pad = coord
                            elif el == 4:
                                self.ball = coord
                                
                    el = next(gen)
                    j+=1           
                #next_key = w.getch()
                #key = automatic_movements[np.sign(self.ball[0] - self.pad[0])] if next_key == -1 else next_key
                            
                #if key == curses.KEY_RIGHT:
                #    inp = 1
                #elif key == curses.KEY_LEFT:
                #    inp = -1
                #else:
                #    inp = 0
                j+=1
                inputs += 1                   
                self.computer._input.append(np.sign(self.ball[0] - self.pad[0]))
        except StopIteration:
            return self.score
            #print(f"Final score is {self.score}")
            
        
#%%
extend = [0]*100000
s = IntCode(code + extend, [])
outs = []
i=0
for j, el in enumerate(s.run()):
    if el == 2 and j%3==2:
        i+=1
ans1 = i
print("Answer for part 1 is", ans1)

#%%
extend = [0]*100000
code[0] = 2
outs = []
s = IntCode(code + extend, [])
g = Game(s)
ans2 = g.run_game()
print("Answer for part 2 is", ans2)
