# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 11:22:21 2019

@author: Caio Camilli
"""

import os
from copy import deepcopy
from itertools import permutations
os.chdir("..//inputs")

def parse_input(path):
    with open(path) as file:
        l = [int(v.rstrip('\n')) for v in file.read().split(',')]
    return l

code = parse_input('7.in')
#%%
class IntCode():
    def __init__(self, inp, input_instructions, verbose=False):
        self._state = deepcopy(inp)
        self._header = 0
        self._hOps = {1:lambda x, y: x+y, 2:lambda x, y: x*y, 99:'halt'}        
        self._verbose = verbose
        self._input = input_instructions
        self.ninputs = 0
        self._output = 0
        
    def _solve_op_and_modes(self):
        opcode, modes = self._parse_instr()
        return opcode, [self._parse_modes(el) for el in modes]
            
    def _treat_op_modes(self, op, modes):
        if op in [1, 2]:
            self._state[self._fetch(3)] = self._hOps[op](modes[0](1), modes[1](2))
        elif op == 3:
            self._state[self._fetch(1)] = self._input[self.ninputs]          
            self._log(f"Wrote {self._input[self.ninputs]} to position {self._fetch(1)}")
            self.ninputs += 1
        elif op == 4:
            self._output = self._state[self._fetch(1)]
            self._log(f"Output was set to {self._state[self._fetch(1)]}")
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
                self._state[self._fetch(3)] = 1
            else:
                self._state[self._fetch(3)] = 0
        elif op == 8:
            if modes[0](1) == modes[1](2):
                self._state[self._fetch(3)] = 1
            else:
                self._state[self._fetch(3)] = 0
                
    def _parse_instr(self):
        v = self._fetch(0)
        self._log(f"Brute instruction is {v}")
        return v%100, [v//100%10, v//1000%10, v//10000%10]
                       
    def _parse_modes(self, var):
        if var == 1:
            return self._fetch
        else:
            return self._fetch2                                   
                       
    def _fetch(self, offset):
        #self._log(f"Returning input {self._state[self._header + offset]} from offset {offset}")
        return self._state[self._header + offset]
    
    def _fetch2(self, offset):
        #self._log(f"Returning input {self._state[self._state[self._header + offset]]} from position {self._state[self._header + offset]} from offset {offset}")
        return self._state[self._state[self._header + offset]]
    
    def _update(self, op):
        if op in [1, 2, 7, 8]:
            self._header += 4
        elif op in [3, 4]:
            self._header += 2
        else:
            pass
        self._log(f"Updated header to {self._header}")
    
    def _log(self, msg):
       if not self._verbose:
            pass
       else:
            print(msg)

    def _run_instructions_and_update(self, op, modes):
        self._log(f"Operation code is {self._fetch(0)}")
        #self._log(f"Update {self._fetch(3)} with value {self._do_op(op)}")
        self._treat_op_modes(op, modes)
        self._update(op)
        #self._log(f"Header set to {self._header}")
        return self._solve_op_and_modes()
        
    def run(self):
        op, modes = self._solve_op_and_modes()
        while op != 99:
            op, modes = self._run_instructions_and_update(op, modes)
        return self._output
    
    def run_fbl(self):
        op, modes = self._solve_op_and_modes()
        while op not in [99, 4]:
            op, modes = self._run_instructions_and_update(op, modes)
        if op == 4:
            op, modes = self._run_instructions_and_update(op, modes)
        return (op == 99), self._output

        

def gen_phase_settings(values):
    return [list(s) for s in list(permutations(values))]
#%%
    
def amplifier_simul(phases, instr):
    inp = 0
    out = 0
    for phase in phases:
        inp = out
        instructions = deepcopy(instr)
        input_instructions = [phase, inp]
        out = IntCode(instructions, input_instructions).run()
    return out

def feedback_loop_mode(phases, instr):
    inp = 0
    out = 0
    i = 0
    halt = False
    computers = []
    while not halt:
        for j, phase in enumerate(phases):
            if i==0:
                amp = IntCode(deepcopy(instr), [phases[j], inp])
                computers.append(amp)                
            else:
                computers[j]._input.append(out)
            halt, out = computers[j].run_fbl()
            inp = out
        i+=1
    return out
        

results = []
phase_settings = gen_phase_settings([0, 1, 2, 3, 4])

for phases in phase_settings:
    results.append(amplifier_simul(phases, code))

ans1 = max(results)
print("Answer for part 1 is", ans1)
#%%
results = []
phase_settings = gen_phase_settings([5, 6, 7, 8, 9])
for phase in phase_settings:
    results.append(feedback_loop_mode(phase, code))

ans2 = max(results)    
print("Answer for part 2 is", ans2)
