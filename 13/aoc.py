import functools, time
import numpy as np

class Maze():
    def __init__(self, f):
        with open('13/'+f+'.txt') as f:
            input_string = f.read()
        lines = input_string.split("\n\n")
        self.lines = [tuple(map(lambda x: eval(x), l.split('\n'))) for l in lines]

    def solve(self, part):
        s = functools.reduce(lambda som, x: som+self.compare(1+x[0], x[1][0], x[1][1], 0), enumerate(self.lines), 0)
        print (part, s)

    def solve2(self, part):
        s2 = functools.reduce(lambda som, x: som+self.compare(1, x[1][0], [[2]],0)+self.compare(1, x[1][1], [[2]], 0), enumerate(self.lines), 1)
        s6 = functools.reduce(lambda som, x: som+self.compare(1, x[1][0], [[6]],0)+self.compare(1, x[1][1], [[6]], 0), enumerate(self.lines), 2)
        print (part, s2*s6)

    def compare(self, index, left, right, rec):
        if np.isscalar(left) and np.isscalar(right): return index if left < right else 0 if left > right else -1
        if np.isscalar(left): return self.compare(index, [left],right, rec+1)
        if np.isscalar(right): return self.compare(index, left,[right], rec+1)
        for i in range(len(left)):
            if i>=len(right): return 0
            c = self.compare(index, left[i], right[i], rec+1)
            if c >=0 : return c
        if len(right)>len(left): return index
        return -1

    def display(self, carte):
        print("\n".join((map(lambda li: "".join([chr(ord('a')+l) for l in li]), carte))))

m = Maze('inputest')
m.solve("part 1")
m = Maze('inputest')
m.solve2("part 2")

time.sleep(4)
m = Maze('input')
m.solve("part 1")
time.sleep(4)
m = Maze('input')
m.solve2("part 2")