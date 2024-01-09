import functools, time, copy
import numpy as np

class Maze():
    def __init__(self, f, part):
        self.f = f
        self.part = part
        with open('20/'+f+'.txt') as fi:
            input_string = fi.read()
        lines = input_string.split("\n")
        self.l = [{'val': int(x), 'pos': i} for i,x in enumerate(lines)]
        self.l1 = [x for x in self.l]
        self.zero = self.l[lines.index("0")]
        self.long = len(self.l)
        #self.display()
        
    def solve(self, deckey=1, tour=1):
        for t in range(tour):
            for j in range(self.long):
                val = deckey*self.l[j]["val"]
                pos = self.l1.index(self.l[j])
                if val%self.long:
                    offset = -1 if val<0 and pos+val<0 else 1 if val>0 and pos+val >= self.long else 0
                    newpos=(pos+val)%(self.long-1)
                    self.l1.insert(newpos, self.l1.pop(pos))

        self.soluce=0
        z = self.l1.index(self.zero)
        for fol in (1000, 2000, 3000):
            val = self.l1[(z+fol)%self.long]["val"]*deckey
            #print (fol,val)
            self.soluce += val

        print (self.f, self.part, self.soluce)

    def display(self):
        print (functools.reduce(lambda c,l: c+str(l["val"])+",", self.l1, ""))


m = Maze('inputest', "part 1")
m.solve()

m = Maze('input', "part 1")
m.solve()
#14262 too high

m = Maze('inputest', "part 2")
m.solve(811589153,10)

m = Maze('input', "part 2")
m.solve(811589153,10)

