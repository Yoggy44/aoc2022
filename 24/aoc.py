import functools, time, copy
import numpy as np

class Maze():
    def __init__(self, f, part):
        self.f = f
        self.part = part
        with open('24/'+f+'.txt') as fi:
            input_string = fi.read()
        lines = input_string.split("\n")
        self.haut = len(lines)
        self.large = len(lines[0])
        self.blz = {"<":[[False for _ in range(self.haut)] for _ in range(self.large)],
                ">":[[False for _ in range(self.haut)] for _ in range(self.large)],
                "^":[[False for _ in range(self.large)] for _ in range(self.haut)],
                "v":[[False for _ in range(self.large)] for _ in range(self.haut)]}
        l=functools.reduce(lambda r, c: self.init(c), functools.reduce(lambda cxy, xy: cxy+list(xy), map(lambda y: map(lambda x: (x[1], x[0], y[0]), enumerate(y[1])), enumerate(lines)), []), [])
        self.begin = (lines[0].find("."), 0)
        self.end = (lines[-1].find("."), len(lines)-1)
        self.pospos = set()
        self.pospos.add(self.begin)
        #self.display()

    def distance(self, a):
        b = self.end
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def init(self, c):
        if c[0] in ('.', '#'): return None
        self.blz[c[0]][c[1] if c[0] in ('<', '>') else c[2]][c[2] if c[0] in ('<', '>') else c[1]] = True 
        return None

    def isblz(self, x, y):
        for b in ("<", ">"):
            if self.blz[b][x][y]: return True
        for b in ("^", "v"):
            if self.blz[b][y][x]: return True
        return False

    def possible(self, pos):
        ret = []
        if pos in (self.begin, self.end) or not self.isblz(pos[0], pos[1]):
            ret.append(pos)
        if pos[1] > self.begin[1] and pos[1] < self.end[1] and pos[0] < self.large-2 and not self.isblz(pos[0]+1, pos[1]):
            ret.append((pos[0]+1, pos[1]))
        if pos[1] > self.begin[1] and pos[1] < self.end[1] and pos[0] > 1 and not self.isblz(pos[0]-1, pos[1]):
            ret.append((pos[0]-1, pos[1]))
        if (pos[0] == self.end[0] and pos[1] == self.end[1]-1) or (pos[1] < self.haut-2 and not self.isblz(pos[0], pos[1]+1)):
            ret.append((pos[0], pos[1]+1))
        if (pos[0]==self.begin[0] and pos[1]==self.begin[1]+1) or (pos[1] > 1 and not self.isblz(pos[0], pos[1]-1)):
            ret.append((pos[0], pos[1]-1))
        for p in ret: self.newpos.add(p)

    def solve(self, part2 = False):
        start_time = time.time()
        round=0
        self.pospos = set()
        self.pospos.add(self.begin)
        while self.end not in self.pospos:
            round += 1
            self.blz["<"].insert(-1, self.blz["<"].pop(1))
            self.blz[">"].insert(1, self.blz[">"].pop(-2))
            self.blz["^"].insert(-1, self.blz["^"].pop(1))
            self.blz["v"].insert(1, self.blz["v"].pop(-2))
            self.newpos = set()
            functools.reduce(lambda c,r: self.possible(r), self.pospos, None)
            self.pospos = self.newpos
            # if round == 18:
            #     self.display()
            #     print ("/r"+str(round)+"-p"+str(len(self.pospos))+"-t"+str((int((time.time()-start_time)*1000)/1000)), self.pospos, end="\n")

        if part2:
            self.pospos = set()
            self.pospos.add(self.end)
            while self.begin not in self.pospos:
                round += 1
                self.blz["<"].insert(-1, self.blz["<"].pop(1))
                self.blz[">"].insert(1, self.blz[">"].pop(-2))
                self.blz["^"].insert(-1, self.blz["^"].pop(1))
                self.blz["v"].insert(1, self.blz["v"].pop(-2))
                self.newpos = set()
                functools.reduce(lambda c,r: self.possible(r), self.pospos, None)
                self.pospos = self.newpos
                #self.display()
                print ("/r"+str(round)+"-p"+str(len(self.pospos))+"-t"+str((int((time.time()-start_time)*1000)/1000)), end="\n")
            self.pospos = set()
            self.pospos.add(self.begin)
            while self.end not in self.pospos:
                round += 1
                self.blz["<"].insert(-1, self.blz["<"].pop(1))
                self.blz[">"].insert(1, self.blz[">"].pop(-2))
                self.blz["^"].insert(-1, self.blz["^"].pop(1))
                self.blz["v"].insert(1, self.blz["v"].pop(-2))
                self.newpos = set()
                functools.reduce(lambda c,r: self.possible(r), self.pospos, None)
                self.pospos = self.newpos
        self.soluce = round 
        print (self.f, self.part,"soluce in s",int(1000*(time.time() - start_time))/1000,"=", self.soluce)

    def display(self, prefix="\n"):
        print("\n"+prefix)
        for j in range(self.haut):
            for i in range(self.large) :
                print("#" if (i in (0, self.large-1) or j in (0, self.haut-1)) and (i,j) not in (self.begin, self.end) else "E" if (i,j) in self.pospos else ".", end="")
            print("  ", end="")
            for b in ('<', '>', '^', 'v'):
                for i in range(self.large):
                    print("#" if (i in (0, self.large-1) or j in (0, self.haut-1)) else b if self.blz[b][i if b in ('<', '>') else j][j if b in ('<', '>') else i] else ".", end="")
                print("  ", end="")
            print("")
#        print("\n".join(map(lambda li: "".join(l for l in li), carte)))

m = Maze('inputest', "part 1")
m.solve()

m = Maze('input', "part 1")
m.solve()
#205 Too low

m = Maze('inputest', "part 2")
m.solve(True)

m = Maze('input', "part 2")
m.solve(True)
#504 Too low