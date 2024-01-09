import functools, time
import numpy as np

class Maze():
    def __init__(self, f, ground = False):
        self.o = "o"
        self.air = "."
        self.rock = "#"
        self.source = "+"
        self.out = (-1, -1)

        with open('14/'+f+'.txt') as f:
            input_string = f.read()
        lines = input_string.split("\n")
        self.minx = self.maxx = 500
        self.miny = self.maxy = 0
        rocks=[]
        for l in lines:
            coord = l.split(" ")
            r = []
            for i in range((len(coord)+1)//2):
                x,y=coord[i*2].split(",")
                r.append((int(x),int(y)))
                if int(x) < self.minx: self.minx = int(x)
                if int(x) > self.maxx: self.maxx = int(x)
                if int(y) < self.miny: self.miny = int(y)
                if int(y) > self.maxy: self.maxy = int(y)
            rocks.append(r)
        if ground:
            self.maxy += 2
            self.minx = min(self.minx, 500-(self.maxy-self.miny+1))
            self.maxx = max(self.maxx, 500+(self.maxy-self.miny+1))
        self.grid = [[self.air for _ in range(self.maxx-self.minx+1)] for _ in range(self.maxy-self.miny+1)]
        if ground:
            self.grid[-1] = [self.rock for _ in self.grid[0]]
        sx, sy =  self.shiftcoord((500,0))
        self.grid[sy][sx] = self.source
        for r in rocks:
            x,y = self.shiftcoord(r.pop(0))
            self.grid[y][x] = self.rock
            while (r != []):
                xy = self.shiftcoord(r.pop(0))
                signx = 1 if xy[0]>=x else -1
                signy = 1 if xy[1]>=y else -1
                for i in range(x, xy[0]+signx, signx):
                    for j in range(y, xy[1]+signy, signy):
                        self.grid[j][i] = self.rock
                x, y = xy
        self.display()
        print(" ")

    def solve(self, part):
        s = 0
        forever = False
        while (not forever):
            s += 1
            x,y = self.shiftcoord((500,0))
            rest = False
            while(not rest and not forever):
                xy = self.nextmove(x, y)
                if xy == self.shiftcoord((500,0)):
                    forever = True
                if xy == (x, y):
                    rest = True
                    self.grid[y][x] = self.o
                if xy == self.out:
                    forever = True
                    s -= 1
                x, y = xy
        self.display()
        print (part, s)

    def nextmove(self, x, y):
        if y == len(self.grid)-1: return self.out
        if self.grid[y+1][x] == self.air: return (x, y+1)
        if x == 0: return self.out
        if self.grid[y+1][x-1] == self.air: return (x-1, y+1)
        if x == len(self.grid[0])-1: return self.out
        if self.grid[y+1][x+1] == self.air: return (x+1, y+1)
        return (x, y)

    def shiftcoord(self, xy):
        x,y = xy
        return (x-self.minx, y-self.miny)

    def display(self):
        print("\n".join(map(lambda li: "".join(l for l in li), self.grid)))

m = Maze('inputest')
m.solve("part 1")

m = Maze('input')
m.solve("part 1")

m = Maze('inputest', True)
m.solve("part 2")

m = Maze('input', True)
m.solve("part 2")

