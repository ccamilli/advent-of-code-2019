# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 08:30:06 2019

@author: c.camilli
"""

#Manual inputs
FUEL_TO_PRODUCE = 1
ORE_UNITS_AVAILABLE = 1000000000000

import math
import numpy as np

def parse_input(filename):
    with open(filename) as file:
        l = [el.rstrip('\n') for el in file.readlines()]
        
    pairs = [el.split('=>') for el in l]     
    adj_list, kv = {}, {}

    for k, v in pairs:
        k = [el.strip(' ') for el in k.strip(' ').split(',')]
        v = v.strip(' ')
        tuples_k = [tuple(el.split(' ')) for el in k]
        tuple_v = tuple(v.split(' '))
        kv[tuple_v[1]] = tuple_v
        adj_list[tuple_v] = tuples_k
                
    return adj_list, kv


def get_levels(adj_list, kv):
    levels = {'FUEL':0}
    j, cur_level = 1, set(['FUEL'])
    while len(cur_level) > 0:
        next_level = set()
        for el in cur_level:
            links = adj_list[kv[el]]
            for v, k in links:
                if k!='ORE':
                    levels[k] = j
                    next_level.add(k)
        j+=1
        cur_level = next_level
        
    levels_1 = {}
    for k, v in levels.items():
        if v not in levels_1:
            levels_1[v] = [k]
        else:
            levels_1[v].append(k)
        
    return levels_1

def get_requirements(adj_list, kv, level_list, fuel_req):
    j = 0
    req = {'FUEL':fuel_req}
    excess = {}
    while j in level_list:
        els = level_list[j]
        for el in els:
            produced, acr = kv[el]
            for reactor in adj_list[(produced, acr)]:
                produced = int(produced)
                input_value = int(reactor[0])*math.ceil(req[el]/produced)
                if reactor[1] not in req:
                    req[reactor[1]] = input_value
                else:
                    req[reactor[1]] += input_value            
        j+=1
    return req

def binary_search(adj_list, kv, level_list, goal):
    first_guess = goal//get_requirements(adj_list, kv, level_list, 1)['ORE']
    factor = int(np.log2(first_guess)) + 10
    ans = 0
    while factor >=0:
        num = 2**factor
        ore_req = get_requirements(adj_list, kv, level_list, ans + num)['ORE']
        if ore_req <= goal:
            ans += num
        factor -=1
    return ans


#PART 1
adj_list, kv = parse_input("..\\inputs\\14.in")
level_list = get_levels(adj_list, kv)
a = get_requirements(adj_list, kv, level_list, FUEL_TO_PRODUCE)
ans1 = a['ORE']
print("Answer for part 1 is", ans1)


#PART 2
ans2 = binary_search(adj_list, kv, level_list, ORE_UNITS_AVAILABLE)
print("Answer for part 2 is", ans2)







