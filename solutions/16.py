# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 12:58:15 2019

@author: c.camilli
"""

import os
from copy import deepcopy
os.chdir("..\\inputs")

def parse_input(filename):
    with open(filename) as file:
        l = [int(el) for line in file.readlines() for el in line.rstrip('\n')]
    return l

seq = parse_input('16.in')

#%%
#PART 1
def apply_fft(seq, niters):
    n = len(seq)
    base_pattern = [0, 1, 0, -1]
    for _ in range(niters):
        out = []        
        for i in range(n):
            cumul = 0
            repeats = n//(4*(i+1)) + 1
            pat = [el for el in base_pattern for k in range(i+1)]
            pat = pat * repeats
            pat = pat[1:(n+1)]
            for j in range(n):
                cumul += seq[j] * pat[j]
            if cumul < 0:
                cumul *= -1
            out.append(cumul%10)
        seq = out
    return out

ans = apply_fft(seq, 100)
ans1 = ""
for el in ans[:8]:
    ans1 += str(el)
    
print("Answer for part 1 is", ans1)
#%%
#PART 2
def apply_fft_with_offset(seq, niters):
    seq = seq * 10000
    offset = ''
    for i in seq[:7]:
        offset += str(i)
    offset = int(offset)
    seq_cut = deepcopy(seq[(offset):])
    for i in range(niters):
        ans = []
        cumul = 0
        for j in range(len(seq_cut)):
            sl = seq_cut[-(j+1)]
            cumul += sl
            if cumul < 0:  
                ans.append(cumul*(-1)%10)
            else:
                ans.append(cumul%10)    
        seq_cut = ans
        seq_cut.reverse()
    return seq_cut

ans = apply_fft_with_offset(seq, 100)
ans2 = ""
for el in ans[:8]:
    ans2 += str(el)
print("Answer for part 2 is", ans2)
#%%
        
    
            
            
    
            