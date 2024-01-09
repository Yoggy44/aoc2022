import functools, time, copy
import numpy as np

class Maze():
    def __init__(self, f, minutes = 30, nb = 1):
        with open('16/'+f+'.txt') as f:
            input_string = f.read()
        lines = input_string.split("\n")
        self.minutes = minutes
        self.nb = nb
        self.valves = dict()
        self.targetvalves = [] # Remaining Valves with rate > 0
        self.valvedist = [[-1 for _ in range(len(lines))] for _ in range(len(lines))]
        self.soluce = 0
        for index,l in enumerate(lines):
            el = l.split(" ")
            name, rate, tunnels = (el[1], int(el[4][5:-1]), list(map(lambda x: x.split(",")[0], el[9:])))
            self.valves[name]={"index":index, "rate": rate, "tunnels": tunnels}
            if rate > 0:
                p = 0
                for i in range(len(self.targetvalves)):
                    if rate >= self.valves[self.targetvalves[i]]["rate"]:
                        p = i
                        break
                self.targetvalves.insert(p, name)
        for v1 in self.valves.values():
            for v2 in v1["tunnels"]:
                self.valvedist[min(v1["index"], self.valves[v2]["index"])][max(v1["index"], self.valves[v2]["index"])]=1
        finished = False
        while(not finished):
            finished = True
            maxlen = len(self.valvedist)+1
            for i in range(len(self.valvedist)-1):
                for j in range (i+1, len(self.valvedist)):
                    if self.valvedist[i][j] == -1:
                        newdist = maxlen
                        for k in range(len(self.valvedist)):
                            if k not in (i,j):
                                l1, l2 = self.disti(i,k), self.disti(j,k)
                                if l1 >0 and l2 > 0:
                                    newdist = min(newdist, l1+l2)
                        if newdist < maxlen:
                            self.valvedist[i][j] = newdist
                        else:
                            finished = False
        #print("\n".join(map(lambda li: "".join("." if l == -1 else str(l) for l in li), self.valvedist)))

    def disti(self, i1, i2):
        return self.valvedist[min(i1, i2)][max(i1, i2)]
    def dist(self, v1, v2):
        return self.disti(self.valves[v1]["index"], self.valves[v2]["index"])

    def solve(self, part):
        self.bruteforce(self.targetvalves, [dict() for _ in range(self.nb)])
        #self.display()
        print (part, self.soluce)

    def bruteforce(self, source, targets):
        if len(source) == 0: return
        for v in source:
            s1 = copy.copy(source)
            s1.remove(v)
            maxleft = 0
            turnleft = 0
            oldpressure = 0
            maxpressure = 0
            found = False
            for n in range(self.nb):
                prevkey = "AA" if len(targets[n]) == 0 else list(targets[n].keys())[-1]
                prev = {"left": self.minutes, "pressure": 0} if len(targets[n]) == 0 else targets[n][prevkey]
                left = max(0,(prev["left"])-1-self.dist(v, prevkey))
                oldpressure += prev["pressure"]
                pressure = left*self.valves[v]["rate"]
                if left > maxleft: maxleft = left
                if pressure >= maxpressure:
                    found = True
                    maxpressure = pressure
                    turnleft = left
                    turn = n
                    turnprev = prev
                    turnprevkey = prevkey
            if not found:
                return
            turnpressure = turnprev["pressure"] + maxpressure
            totalpressure = oldpressure + turnleft*self.valves[v]["rate"]
            if totalpressure > self.soluce:
                #print("newsoluce", self.soluce, list(map(lambda x: list(x.keys()), targets)))
                self.soluce = totalpressure
            t1 = {v:{"left": turnleft,
                     "pressure": turnpressure}}
            if maxleft > 0 and (self.remainingrates(s1)*maxleft + totalpressure >= self.soluce):
                t = copy.copy(targets)
                t[turn] = dict(targets[turn],**t1)
                self.bruteforce(s1, t)
        return

    def remainingrates(self, s):
        return functools.reduce(lambda c,x: c+self.valves[x]["rate"], s, 0)

    def display(self):
        print(self.valves)

m = Maze('inputest')
m.solve("part 1")

m = Maze('input')
m.solve("part 1")

m = Maze('inputest', 26, 2)
m.solve("part 2")

m = Maze('input', 26, 2)
m.solve("part 2")

