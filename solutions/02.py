# -*- coding: utf-8 -*-
"""
@author: Caio Camilli
"""

with open('..\\inputs\\2.in') as file:
    l = [int(el) for lis in [line.rstrip('\n').split(',') for line in file] for el in lis]

class Simulation():
    def __init__(self, inp, verbose=False):
        self._state = inp.copy()
        self._header = 0
        self._hOps = {1:lambda x, y: x+y, 2:lambda x, y: x*y, 99:'halt'}
        self._verbose = verbose
        
    def _solve_op(self):
        try:
            return self._hOps[self._fetch(0)]
        except KeyError:
            raise ValueError('Something went wrong, saw', self._fetch(0))
            
    def _do_op(self, op):
        return op(self._fetch2(1), self._fetch2(2))
                       
    def _fetch(self, offset):
        return self._state[self._header + offset]
    
    def _fetch2(self, offset):
        return self._state[self._state[self._header + offset]]
    
    def _log(self, msg):
        if not self._verbose:
            pass
        else:
            print(msg)

    def _run_instructions_and_update(self, op):
        self._log(f"Operation code is {self._fetch(0)}")
        self._log(f"Update {self._fetch(3)} with value {self._do_op(op)}")
        self._state[self._fetch(3)] = self._do_op(op)
        self._header += 4
        self._log(f"Header set to {self._header}")
        return self._solve_op()
        
    def run(self):
        op = self._solve_op()
        while op != 'halt':
            op = self._run_instructions_and_update(op)
        return self._state
            
l[1], l[2] = 12, 2

ans1 = Simulation(l).run()[0]

print("Answer for part 1 is", ans1)

def update_nouns_verbs(l, n, v):
    l[1], l[2] = n, v
    return l

n, kill = 0, False

while (n < 100 and kill is False):
    v = 0
    while (v < 100 and kill is False):
        out = Simulation(update_nouns_verbs(l, n, v)).run()[0]
        if out == 19690720:
            kill = True
            ans2 = 100*n + v
        v += 1
    n += 1      
    
print("Answer for part 2 is", ans2)