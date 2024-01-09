import functools, time, copy
import numpy as np

class Maze():
    def __init__(self, f, it):
        with open('17/'+f+'.txt') as fi:
            input_string = fi.read()
        self.jet = input_string
        self.vide = "."
        self.rock = "#"
        self.blocks = []
        self.initblocks()
        self.height = 0
        self.chamber=[]
        self.soluce = 0
        self.it = it
        self.lastbx = -1

    def initblocks(self):
        b = { "height": 1, "<": [(0,0)], ">": [(3,0)], "v": [(0,0), (1, 0), (2,0), (3,0)], self.rock: [(0,0), (1, 0), (2,0), (3,0)]}
        self.blocks.append(b)
        b = { "height": 3, "<": [(1,0), (0,1), (1,2)], ">": [(1,0), (2,1), (1,2)], "v": [(0,1), (1,0), (2,1)], self.rock: [(0,1), (1,0), (2,1), (1,2), (1,1)]}
        self.blocks.append(b)
        b = { "height": 3, "<": [(0,0), (2,1), (2,2)], ">": [(2,0), (2,1), (2,2)], "v": [(0,0), (1,0), (2,0)], self.rock: [(0,0), (1,0), (2,0), (2,1), (2,2)]}
        self.blocks.append(b)
        b = { "height": 4, "<": [(0,0), (0,1), (0,2), (0,3)], ">": [(0,0), (0,1), (0,2), (0,3)], "v": [(0,0)], self.rock: [(0,0), (0,1), (0,2), (0,3)]}
        self.blocks.append(b)
        b = { "height": 2, "<": [(0,0), (0,1)], ">": [(1,0), (1,1)], "v": [(0,0), (1,0)], self.rock: [(0,0), (1,0), (0,1), (1,1)]}
        self.blocks.append(b)

    def comp(self, t1, t2):
        return "".join("".join(l) for l in t1) == "".join("".join(l) for l in t2)

    def solve(self, part):
        self.jb = 0
        recursh = recursfb  = 0
        recurslen = 1
        recurs = False
        fb0 = [[-1,0,-2,[]] for _ in range(len(self.jet))]
        for fb in range (self.it):
            self.newblock(fb)
            if not recurs and fb % len(self.blocks) == 0:
                if fb0[self.jb][0] == -1:
                    fb0[self.jb] = [fb, self.height, self.lastbx, self.chamber[-8:]]
                else:
                    if fb0[self.jb][2] == self.lastbx and self.comp(fb0[self.jb][3], self.chamber[-8:]) :
                        recurs = True
                        recursindic = self.jb
                        recursfb = fb0[recursindic][0]
                        recurslen = fb - recursfb
                        recursh = self.height - fb0[recursindic][1]
                        #print(" recurs found, fb", fb, "recursindic", recursindic, "recursfb", recursfb, "recurslen", recurslen, "recursh", recursh)
                        #print(" Will stop at", ((self.it-1 - recursfb) % recurslen) + recursfb + recurslen)
                        end = ((self.it-1 - recursfb) % recurslen) + recursfb + recurslen
                        print ("\n For", self.it, " end at", end)
                        print(" with jb=",self.jb, "fb0[jb] = ", fb0[self.jb])
                    else:
                        fb0[self.jb] = [fb, self.height, self.lastbx, self.chamber[-8:]]
            if recurs and fb == end:
                print (" estimated end: recursh (",recursh,") * self.it-1-recursfb (",recursfb,") // recurslen(",recurslen,") = ",(self.it-1-recursfb) // recurslen,") -1 + height (",self.height ,") =", recursh*(((self.it-1-recursfb) // recurslen)-1)+self.height)
                self.display(9)
                break
        #print("real top")
        #self.display(10)
        self.soluce = 0*recursh*(((self.it-1-recursfb) // recurslen)-1)+self.height
        #print ("real soluce for",self.it, "is", self.soluce)
        self.soluce = recursh*(((self.it-1-recursfb) // recurslen)-1) + self.height
        print (part, self.soluce)

    def newblock(self, fb):
        #new blocks
        b = self.blocks[fb%len(self.blocks)]
        self.chamber += [self.vide*7 for _ in range(self.height+b["height"]+3-len(self.chamber))]
        bx, by = (2, self.height+3)
        stop = False
        while (not stop):
            #jet
            j = self.jet[self.jb]
            dj = 1 if j == ">" else -1
            for mv in b[j]:
                tx = bx+mv[0]+dj
                ty = by+mv[1]
                if tx < 0 or tx > 6 or not self.chamber[ty][tx] == self.vide:
                    dj = 0
                    break
            bx += dj
            #fall
            if by == 0: stop = True
            else:           
                for mv in b["v"]:
                    if not self.chamber[by+mv[1]-1][bx+mv[0]] == self.vide:
                        stop = True
                        break
                if not stop : by -= 1
            self.jb = (1+self.jb)%len(self.jet)
        for d in b[self.rock]:
            nl = list(self.chamber[by+d[1]])
            nl[bx+d[0]] = self.rock
            self.chamber[by+d[1]] = "".join(nl)
        self.lastbx = bx
        self.height = max(self.height, by+b["height"])

    def display(self, limit=0):
        print (functools.reduce(lambda c,l: "|"+l+"|\n"+c, self.chamber[-limit:self.height], "")+"+-------+\n")


m = Maze('inputest', 2022)
m.solve("part 1")

m = Maze('input', 2022)
m.solve("part 1")

m = Maze('inputest', 1000000000000)
m.solve("part 2")

m = Maze('input', 1000000000000)
m.solve("part 2")

