# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 14:15:55 2019

@author: Caio Camilli
"""

import os
import numpy as np
from PIL import Image
os.chdir("..\\inputs")

def parse_input(path):
    with open(path) as file:
        l = [int(d) for v in file.readlines() for d in v.strip('\n')]
    return l

inp = parse_input("8.in")
#%%
##PART 1
arr = np.array(inp).reshape(100, -1)
layer = arr[np.argmax(np.count_nonzero(arr, axis=1))]
unique, counts = np.unique(layer, return_counts = True)
d = dict(zip(unique, counts))
ans1 = d[1]*d[2]
print("Answer for part 1 is", ans1)
#%%
##PART 2
image_data = np.apply_along_axis(lambda x: x[x!=2][0], 0, arr.reshape(100, 6, 25))
image_data = 255 - 255*np.array(image_data, dtype=np.uint8).reshape(6, 25)
img = Image.fromarray(image_data, 'L').resize([2500, 600])
img.save('..\\outputs\\ans8.png')
print("Check outputs\\ans8.png to answer part 2")
img.show()