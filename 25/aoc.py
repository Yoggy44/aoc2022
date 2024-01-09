import functools, time, copy
import numpy as np

class Maze():
    def __init__(self, f, part):
        self.f = f
        self.part = part
        with open('25/'+f+'.txt') as fi:
            input_string = fi.read()
        self.snafu = input_string.split("\n")

    def decod(self, d, s2d=True):
        if s2d:
            match d:
                case "=": return -2
                case "-": return -1
                case _ : return int(d)
        else:
            match d:
                case "0": return "="
                case "1": return "-"
                case _ : return str(int(d)-2)
    def base5(self, v):
        if (v+2) < 5: return self.decod(str(v+2), False)
        return self.base5((v+2)//5) + self.decod(str((v+2)%5), False)

    def snafu2dec(self, s):
        return functools.reduce(lambda r,d: r + pow(5,len(s)-d[0]-1)*self.decod(d[1]), enumerate(list(s)), 0)

    def solve(self, part2 = False):
        start_time = time.time()
        self.soluce = self.base5(functools.reduce(lambda c, r: c+self.snafu2dec(r), self.snafu, 0))
        print (self.f, self.part,"soluce in s",int(1000*(time.time() - start_time))/1000,"=", self.soluce)

    def display(self, prefix="\n"):
        print("")
#        print("\n".join(map(lambda li: "".join(l for l in li), carte)))


m = Maze('inputest', "part 1")
m.solve()

m = Maze('input', "part 1")
m.solve()

#m = Maze('inputest', "part 2")
#m.solve(True)

#m = Maze('input', "part 2")
#m.solve(True)
