# -*- coding: utf-8 -*-
"""
Created on Sun Dec 22 18:14:01 2019

@author: c.camilli
"""

#Manual inputs
PART_1_DECK_SIZE = 10007
PART_1_CARD_TO_TRACK = 2019
PART_2_DECK_SIZE = 119315717514047
PART_2_N_SHUFFLES = 101741582076661
PART_2_POSITION_TO_TRACK = 2020

import numpy as np

def parse_file(filename):
    with open(filename) as file:
        f = [el.rstrip('\n') for el in file.readlines()]
    return f

class Shuffler():    
    def __init__(self, instructions, deck_size):
        self.deck = np.arange(deck_size)
        self.instructions = instructions
        
    def shuffle(self):
        for instr in self.instructions:
            self.process_instruction(instr)
            
    def process_instruction(self, instr):
        if instr.startswith('deal into'):
            self.deck = np.flip(self.deck)
        elif instr.startswith('cut'):
            ct = int(instr.split(' ')[-1])
            self.deck = np.roll(self.deck, -ct)
        elif instr.startswith('deal with'):
            incr = int(instr.split(' ')[-1])
            n = len(self.deck)
            cp = np.zeros(n)
            for i, el in enumerate(self.deck):
                cp[(i*incr)%n] = el
            self.deck = cp
            
    def get_index_of(self, n):
        for i, el in enumerate(self.deck):
            if el == n:
                return i


f = parse_file('..//inputs//22.in')
            
s = Shuffler(f, PART_1_DECK_SIZE)
s.shuffle()
ans1 = s.get_index_of(PART_1_CARD_TO_TRACK)
print("Answer for part 1 is", ans1)

class SmarterShuffler(Shuffler):   
    def __init__(self, instructions, deck_size):
        self.instructions = instructions
        #one round of shuffling maps index ix to (offset + ix*spaces)%deck_size
        self.deck_size = deck_size
        self.offset = 0
        self.spaces = 1          
    
    def process_instruction(self, instr):
        if instr.startswith('deal into'):
            self.offset = self.deck_size - self.offset - 1
            self.spaces = (self.deck_size - self.spaces)
            #self.reverse = not self.reverse
        elif instr.startswith('cut'):
            ct = -int(instr.split(' ')[-1])
            self.offset = (self.offset + ct)%self.deck_size
        elif instr.startswith('deal with'):
            incr = int(instr.split(' ')[-1])
            self.offset = (self.offset*incr)%self.deck_size
            self.spaces = (self.spaces*incr)%self.deck_size
            
    def find_card_at(self, index_num, num_shuffles):
        #knowing the position of one card after num_shuffles (we take the fixed point
        #of the shuffling transformation) and the distance between 
        #adjacent elements on the shuffled deck (step), we can easily compute 
        #the value of the card at index_num.
        
        self.shuffle()
        step = self.find_step_after(num_shuffles)
        fixed_point = self.find_fixed_point()
        return (fixed_point + (index_num - fixed_point)*step)%self.deck_size 
            
    def find_step_after(self, n_shuffles):
        #inverting self.spaces to get the difference between adjacent elements
        #on shuffled deck
        
        return SmarterShuffler.modinv(pow(self.spaces,n_shuffles,self.deck_size),
                                      self.deck_size)
 
    def find_fixed_point(self):
        #solving the equation (offset + ix*spaces)%deck_size = ix
        
        return (-self.offset * SmarterShuffler.modinv(self.spaces-1,
                                                       self.deck_size))%self.deck_size    

    @staticmethod
    def modinv(a, n):
        t, t_new = 0, 1
        r, r_new = n, a
        while r_new != 0:
            qt = r // r_new
            t, t_new = t_new, t - qt * t_new
            r, r_new = r_new, r % r_new
        if t < 0:
            t += n
        return t
            
    
s = SmarterShuffler(f, PART_2_DECK_SIZE)
ans2 = s.find_card_at(PART_2_POSITION_TO_TRACK, PART_2_N_SHUFFLES)
print("Answer for part 2 is", ans2)