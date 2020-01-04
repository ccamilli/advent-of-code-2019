# -*- coding: utf-8 -*-
"""
@author: Caio Camilli
"""

def parse_input(filename):
    with open(filename) as file:
        ls = [line.strip('\n').split(',') for line in file.readlines()]
    return ls

wires = parse_input('..\\inputs\\3.in')

class Vertice:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    @classmethod
    def from_instructions(cls, instr):
        if instr[0] == 'R':
            return cls(int(instr[1:]), 0)
        elif instr[0] == 'D':
            return cls(0, -int(instr[1:]))
        elif instr[0] == 'U':
            return cls(0, int(instr[1:]))
        else:
            return cls(-int(instr[1:]), 0)
        
    def __add__(self, other):
        return Vertice(self.x + other.x, self.y + other.y)
    
    def __repr__(self):
        return f"Vertice: ({self.x}, {self.y})"
    
    @staticmethod
    def manhattan_distance(v1, v2):
        return abs(v1.x - v2.x) + abs(v1.y - v2.y)
    
    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)
    
    def __hash__(self):
        return id(self)
    

class Line:
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2
        if v1.y == v2.y:
            self.type = 'horizontal'
            self.level = v1.y
            if v1.x > v2.x:
                self.start = v2.x
                self.end = v1.x
            else:
                self.start = v1.x
                self.end = v2.x
        else:
            self.type = 'vertical'
            self.level = v1.x
            if v1.y > v2.y:
                self.start = v2.y
                self.end = v1.y
            else:
                self.start = v1.y
                self.end = v2.y
        
    def test_crossing(self, other):
        if self.type == 'horizontal':
            return Line.check_crossings(self, other)
        else:
            return Line.check_crossings(other, self)
            
    @staticmethod
    def check_crossings(first, other):
        if first.type != 'horizontal' or other.type != 'vertical':
            return None
        if first.level < other.end and first.level > other.start:
            if other.level < first.end and other.level > first.start:
                return Vertice(other.level, first.level)
            else:
                return None
        else:
            return None
        
    def contains(self, v):
        if self.type == 'horizontal':
            return self.level == v.y and self.start < v.x and self.end > v.x
        else:
            return self.level == v.x and self.start < v.y and self.end > v.y
                
    def __repr__(self):
        return f"{self.type} line, level={self.level}, start={self.start}, end={self.end}"
    
    def __len__(self):
        return self.end - self.start

class Wire:
    def __init__(self, instr):
        self._instr = instr
        self._lines = []
        self._vertices = [Vertice(0, 0)]
        self._get_lines_and_vertices()
        
    def _get_lines_and_vertices(self):
        cur = Vertice(0, 0)
        for instruction in self._instr:
            new = cur + Vertice.from_instructions(instruction)
            self._vertices.append(new)
            self._lines.append(Line(cur, new))
            cur = new
    
    def get_crossings(self, other):
        cs = []
        for line1 in self._lines:
            for line2 in other._lines:
                a = line1.test_crossing(line2)
                if a is not None:
                    cs.append(a)
        return cs
    
    def get_length_until(self, v):
        vs = [el for el in self._lines if el.contains(v)]
        vf = vs[0].v1
        v0 = self._vertices[0]
        d = 0
        for vcur in self._vertices:
            d += Vertice.manhattan_distance(v0, vcur)
            v0 = vcur
            if v0 == vf:
                break
        return d + Vertice.manhattan_distance(vf, v)
               
    def __repr__(self):
        l = [w.__repr__() for w in self._lines]
        return l.__repr__()
                    
    
ws = [Wire(a) for a in wires]
crossings = ws[0].get_crossings(ws[1])
ds = {a:Vertice.manhattan_distance(a, Vertice(0, 0)) for a in crossings}
ans1 = min(ds.values())
print("Answer for part 1 is", ans1)

ds2 = {a:(ws[0].get_length_until(a) + ws[1].get_length_until(a)) for a in crossings}
ans2 = min(ds2.values())
print("Answer for part 2 is", ans2)

                    