import functools, time, copy
import numpy as np

class Maze():
    def __init__(self, f, ground = False):
        with open('16/'+f+'.txt') as f:
            input_string = f.read()
        lines = input_string.split("\n")
        self.valves = dict()
        self.currentrate = 0
        self.currentvalve = "AA"
        self.targetvalves = [] # Remaining Valves with rate > 0
        self.waiting = 0
        self.valve2open = False
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
        self.bruteforce(self.targetvalves, dict())
        #self.display()
        print (part, self.soluce)

    def bruteforce(self, source, target):
        if len(source) == 0 :
            return
        for v in source:
            s1 = copy.copy(source)
            s1.remove(v)
            prevkey = "AA" if len(target) == 0 else list(target.keys())[-1]
            prev = {"left": 30, "pressure": 0} if len(target) == 0 else target[prevkey]
            left = max(0,(prev["left"])-1-self.dist(v, prevkey))
            pressure = prev["pressure"] + left*self.valves[v]["rate"]
            if pressure > self.soluce:
                #print ("new soluce", self.soluce, target.keys(), target)
                self.soluce = pressure
            t1 = {v:{"left": left,
                     "pressure": pressure}}
            #print(s1, target+[v])
            if left > 0 and (self.remainingrates(s1)*left + pressure >= self.soluce):
                self.bruteforce(s1, dict(target,**t1))
        return

    def remainingrates(self, s):
        return functools.reduce(lambda c,x: c+self.valves[x]["rate"], s, 0)

    def computepressure(self, valveorder):
        p = functools.reduce(lambda c,x: {"prev": x,
                                          "t": c["t"]+[{"duration": max(0, c["left"]-1-self.dist(c["prev"],x)),
                                                        "rate": self.valves[x]["rate"]}],
                                          "left":c["left"]-1-self.dist(c["prev"],x)},
                             valveorder,
                             {"prev": "AA", "t": [], "left":30})
        r= functools.reduce(lambda d,y: d+y["duration"]*y["rate"] ,p["t"], 0)
        return r

    # def solve1(self, part): #Wrong answer
    #     soluce = 0
    #     for m in range(30):
    #         soluce += self.currentrate 
    #         self.action(30-m)
    #     self.display()
    #     print (part, soluce)

    # def action(self, minleft):
    #     print ("Action minute", 30-minleft+1)
    #     if self.waiting > 0:
    #         print (" Moving for ", self.waiting, "minutes toward", self.currentvalve , "with current rate", self.currentrate)
    #         self.waiting -= 1
    #         return
    #     if self.valve2open:
    #         print (" Opening valve", self.currentvalve , "with current rate", self.currentrate)
    #         self.currentrate += self.valves[self.currentvalve]["rate"]
    #         self.valve2open = False
    #         self.targetvalves.pop(self.targetvalves.index(self.currentvalve))
    #         return
    #     #move to valve + chnage self.waiting  + currentvalve + valv2open = True
    #     optvalvedist = 0
    #     optvalvename = ""
    #     for v in self.targetvalves:
    #         # TODO : Check if best choice
    #         if self.valves[v]["rate"]-self.dist(self.currentvalve, v) > optvalvedist and minleft > self.dist(self.currentvalve, v):
    #             optvalvedist = self.valves[v]["rate"]-self.dist(self.currentvalve, v)
    #             optvalvename = v
    #     if optvalvedist > 0 :
    #         print (" Choosing to move during ", self.dist(self.currentvalve, optvalvename) , "minutes toward", optvalvename, "with current rate", self.currentrate)
    #         self.waiting = self.dist(self.currentvalve, optvalvename)-1
    #         self.valve2open = True
    #         self.currentvalve = optvalvename

    def display(self):
        print(self.valves)

m = Maze('inputest')
m.solve("part 1")

m = Maze('input')
m.solve("part 1")

# m = Maze('inputest', True)
# m.solve("part 2")

# m = Maze('input', True)
# m.solve("part 2")

