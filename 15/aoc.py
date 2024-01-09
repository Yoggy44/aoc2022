import functools, time, copy
import numpy as np

class Maze():
    def __init__(self, f, y, width=0):
        with open('15/'+f+'.txt') as f:
            input_string = f.read()
        lines = input_string.split("\n")
        self.y = y
        self.width = width
        self.sensors = []
        self.beaconX = set()
        for l in lines:
            el = l.split(" ") 
            s = {"pos": (int(el[2][2:-1]), int(el[3][2:-1])), "beaconpos": ((int(el[8][2:-1]), int(el[9][2:]))), "range": self.dist((int(el[2][2:-1]), int(el[3][2:-1])),((int(el[8][2:-1]), int(el[9][2:]))))}
            if s["beaconpos"][1] == y: self.beaconX.add(s["beaconpos"][0])
            self.sensors.append(s)
        self.soluce = ""

    def solve(self, part):
        if self.width == 0 :
            noposition = set()
            for s in self.sensors:
                dy = abs(s["pos"][1]-self.y)
                if dy <= s["range"]:
                    for x in range(s["pos"][0]-s["range"]+dy,s["pos"][0]+s["range"]-dy+1):
                        if x not in self.beaconX: noposition.add(x)
            self.soluce = len(noposition)
        else:
            x = y = 0
            found = False
            while (not found):
                found = True
                for s in self.sensors:
                    if self.dist((x,y), s["pos"])<= s["range"]:
                        found = False
                        x = s["pos"][0]+s["range"]-abs(s["pos"][1]-y)
                        break
                if found:
                    self.soluce=x*4000000+y
                else:
                    x+=1
                    if x>self.width:
                        x,y=0,y+1
                
        print (part, self.soluce)

    def dist(self, xy1, xy2):
        return abs(xy1[0]-xy2[0])+abs(xy1[1]-xy2[1])

    def display(self):
        print("Sensors", self.sensors)

m = Maze('inputest', 10)
m.solve("part 1")

m = Maze('input', 2000000)
m.solve("part 1")

m = Maze('inputest', 0, 20)
m.solve("part 2")

m = Maze('input', 0, 4000000)
m.solve("part 2")

