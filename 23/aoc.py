import functools, time, copy
import numpy as np

class Maze():
    def __init__(self, f, part):
        self.f = f
        self.part = part
        with open('23/'+f+'.txt') as fi:
            input_string = fi.read()
        lines = input_string.split("\n")
        self.elves = []
        for y,l in enumerate(lines):
            s = 0
            while l.find("#",s) >= 0:
                self.elves.append((l.find("#", s), y))
                s = l.find("#", s) + 1
        self.dirs = ['N', 'S', 'W', 'E']
        #self.display()

    def posindir(self, pos, dir, all = False):
        if   dir == 'N': return [(pos[0] + d, pos[1] - 1) for d in (-1,0,1)] if all else (pos[0], pos[1] - 1)
        elif dir == 'S': return [(pos[0] + d, pos[1] + 1) for d in (-1,0,1)] if all else (pos[0], pos[1] + 1)
        elif dir == 'W': return [(pos[0] - 1, pos[1] + d) for d in (-1,0,1)] if all else (pos[0] - 1, pos[1])
        elif dir == 'E': return [(pos[0] + 1, pos[1] + d) for d in (-1,0,1)] if all else (pos[0] + 1, pos[1])
        else: print("ERROR : dir unknown")

    def isPinElves(self, p, cache):
        if p in cache: return cache[p]
        r = p in self.elves
        cache[p] = r
        return r

    def propose(self, elf):
        # Don't move if no elves around
        cache = dict()
        prop = False
        for p in self.posindir(elf, 'N', True)+self.posindir(elf, 'S', True)+[self.posindir(elf, 'E', False), self.posindir(elf, 'W', False)]:
            if self.isPinElves(p, cache) :
                prop = True
                break
        if not prop: return () # Todo
        # Choose which first acceptable proposal
        for d in self.dirs:
            prop = self.posindir(elf, d, False)
            for p in self.posindir(elf, d, True):
                if self.isPinElves(p, cache):
                    prop = None
                    break
            if not prop == None:
                return prop
        # Don't move if no acceptable proposal
        return None

    def solve(self, part2 = False):
        start_time = time.time()
        #self.display(f'{self.pos}{self.dir}')
        self.movingelves = [i for i in range(len(self.elves))]
        self.stillelves = []
        nr = 10 if not part2 else -1
        round = 0
        still = False
        while not still and round != nr:
            rstart_time = time.time()
            round += 1
            props = dict()
            # Calculate proposals
            nse=set()
            l=functools.reduce(lambda r, p: r if p[1] == None else [r[0], r[1], r[0].add(p[0])] if p[1] == () else [r[0], r[1], r[1].setdefault(p[1],[]).append(p[0])], map(lambda en: [en, self.propose(self.elves[en])], self.movingelves), [set(),dict()])
            nse, props = (l[0], l[1]) 
            # for i in self.movingelves:
            #     p = self.propose(self.elves[i])
            #     if p != None and p != ():
            #         if p in props: props[p].append(i)
            #         else: props[p] = [i]
            #     elif p == ():
            #         nse.add(i)
            for i in nse:
                self.stillelves.append(self.movingelves.pop(self.movingelves.index(i)))
            # determine if no moves
            if len(props) == 0:
                still = True
            else:
            # apply possible proposals
                nme=set()
                for p in props:
                    if len(props[p]) == 1:
                        self.elves[props[p][0]] = p
                        for e in self.stillelves:
                            if (self.elves[e][0]-p[0])*(self.elves[e][0]-p[0]) + (self.elves[e][1]-p[1])*(self.elves[e][1]-p[1]) < 3:
                                nme.add(e)
                for i in nme:
                    self.movingelves.append(self.stillelves.pop(self.stillelves.index(i)))
            self.dirs.append(self.dirs.pop(0))
            print("."+str(int(1000*(time.time() - rstart_time)))+"("+str(len(self.movingelves))+","+str(len(self.stillelves))+")", end='')
            #self.display("after round " + str(round))

        r = functools.reduce(lambda r,e: (min(r[0], e[0]), min(r[1], e[1]), max(r[2], e[0]), max(r[3], e[1])), self.elves, (0, 0, 0, 0))
        self.soluce = (r[3]-r[1]+1)*(r[2]-r[0]+1)-len(self.elves) if not part2 else round
        print("Found")
        print (self.f, self.part,"rect", r, "nb-elves", len(self.elves), "soluce in s",int(1000*(time.time() - start_time))/1000,"=", self.soluce)

    def display(self, prefix=""):
        r = functools.reduce(lambda r,e: (min(r[0], e[0]), min(r[1], e[1]), max(r[2], e[0]), max(r[3], e[1])), self.elves, (0, 0, 0, 0))
        carte=[['.' for x in range(r[2]-r[0]+1)] for x in range(r[3]-r[1]+1)]
        #print(r, len(carte[0]), len(carte))
        for idx, e in enumerate(self.elves):
            carte[e[1]-r[1]][e[0]-r[0]] = "#" if idx not in self.stillelves else "@"
        print(prefix)
        print("\n".join(map(lambda li: "".join(l for l in li), carte)))
        print(self.dirs)

m = Maze('inputest', "part 1")
m.solve()

m = Maze('input', "part 1")
m.solve()

m = Maze('inputest', "part 2")
m.solve(True)

m = Maze('input', "part 2")
m.solve(True)
