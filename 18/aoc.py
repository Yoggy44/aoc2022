import functools, time, copy
import numpy as np

class Maze():
    def __init__(self, f, part):
        self.f = f
        self.part = part
        with open('18/'+f+'.txt') as fi:
            input_string = fi.read()
        self.droplets = [list(map(lambda x: int(x), j.split(","))) for j in input_string.split("\n")]
        self.partition = dict()

    def solve(self):
        self.commonfaces = 0
        for d in self.droplets:
            dist = self.dist(d)
            if dist not in self.partition.keys():
                self.partition[dist] = [d]
            else:
                self.partition[dist].append(d)
            for dir in range(6):
                d1 = self.xyzindir(d, dir)
                dist1 = self.dist(d1)
                if dist1 in self.partition.keys():
                    #print(d,"cherche", d1, "in",self.partition[dist1])
                    if d1 in self.partition[dist1]:
                        #print("Found", d1)
                        self.commonfaces += 1
        self.soluce = len(self.droplets)*6-2*self.commonfaces
        print (self.f, self.part, self.soluce)

    def solve2(self):
        self.commonfaces = 0
        self.minx, self.miny, self.minz, self.maxx, self.maxy, self.maxz = 100, 100, 100, -1, -1, -1
        for d in self.droplets:
            if d[0] > self.maxx : self.maxx = d[0]
            if d[0] < self.minx : self.minx = d[0]
            if d[1] > self.maxy : self.maxy = d[1]
            if d[1] < self.miny : self.miny = d[1]
            if d[2] > self.maxz : self.maxz = d[2]
            if d[2] < self.minz : self.minz = d[2]
            dist = self.dist(d)
            if dist not in self.partition.keys():
                self.partition[dist] = [d]
            else:
                self.partition[dist].append(d)
        self.maxx += 1
        self.maxy += 1
        self.maxz += 1
        self.minx -= 1
        self.miny -= 1
        self.minz -= 1
        # Parcours recursif  de l'air dans cet espace avec droplet
        self.visited = []
        print (self.minx, self.maxx, self.miny, self.maxy, self.minz, self.maxz)
        to_explore = [[self.minx, self.miny, self.minz]]
        while (len(to_explore) > 0):
            d = to_explore.pop(0)
            for dir in range(6):
                d1 = self.xyzindir(d, dir)
                dist1 = self.dist(d1)
                if self.inside(d1) and d1 not in self.visited:
                    if dist1 in self.partition.keys() and d1 in self.partition[dist1]:
                        #print("contact:", d, dir)
                        self.commonfaces += 1
                    else:
                        self.visited.append(d1)
                        to_explore.append(d1)

        self.soluce = self.commonfaces
        print (self.f, self.part, self.soluce)

    def inside(self, d):
        return self.maxx >= d[0] >= self.minx and self.maxy >= d[1] >= self.miny and self.maxz >= d[2] >= self.minz

    def dist(self, d):
        return abs(d[0])+abs(d[1])+abs(d[2])

    def xyzindir(self,d,dir):
        dx = (dir%2)*2 - 1 if dir < 2 else 0
        dy = (dir%2)*2 - 1 if 4>dir>=2 else 0
        dz = (dir%2)*2 - 1 if dir >= 4 else 0
        return [d[0]+dx, d[1]+dy, d[2]+dz]

    def display(self, limit=0):
        print (self.droplets)


m = Maze('inputest', "part 1")
m.solve()

m = Maze('input', "part 1")
m.solve()

m = Maze('inputest', "part 1")
m.solve2()

m = Maze('input', "part 2")
m.solve2()

