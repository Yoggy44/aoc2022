import functools, time, copy
import numpy as np

class Maze():
    def __init__(self, f, part):
        self.f = f
        self.part = part
        with open('21/'+f+'.txt') as fi:
            input_string = fi.read()
        #lines = input_string.split("\n")
        self.monkeys = list(map(lambda x: [x[0] , x[1].split(" ")],map(lambda x: x.split(": "), input_string.split("\n"))))
        self.resolved=dict()
        self.unresolved=dict()
        self.dependancy=dict()

    def check(self, mn, mv):
#        if mn == 'root': self.display("check begin")
        if mv[0] in self.resolved :
            mv[0] = self.resolved[mv[0]]
        if mv[2] in self.resolved :
            mv[2] = self.resolved[mv[2]]
        if type(mv[0]) == int and type(mv[2]) == int :
            self.unresolved.pop(mn, "")
            mv = eval(str(mv[0])+mv[1].replace('/', '//')+str(mv[2]))
            self.resolved[mn] = mv
            return True
#        if mn == 'root': self.display("Check end")
        return False

    def recsolve(self, monkeyname):
        deplist = self.dependancy.pop(monkeyname, [])
        while(len(deplist) > 0):
            mn = deplist.pop()
            mv = self.unresolved[mn]
            if self.check(mn, mv): 
                self.recsolve(mn)

    def solve(self, part2 = False):
        for m in self.monkeys:
            if part2 and m[0] == 'humn' : m[0] = 'yann'
            if len(m[1]) > 1:
                if self.check(m[0], m[1]):
                    self.recsolve(m[0])
                else:
                    if type(m[1][0]) == str:
                        if m[1][0] not in self.dependancy: 
                            self.dependancy[m[1][0]] = [m[0]]
                        else:
                            self.dependancy[m[1][0]].append(m[0])
                    if type(m[1][2]) == str:
                        if m[1][2] not in self.dependancy: 
                            self.dependancy[m[1][2]] = [m[0]]
                        else:
                            self.dependancy[m[1][2]].append(m[0])
                    self.unresolved[m[0]] = m[1]
            else:
                self.resolved[m[0]] = int(m[1][0])
                self.recsolve(m[0])
#            if m[0] == 'root': self.display("After root init")

        if part2:
            self.revunres = dict()
            self.dependancy = dict()
            mn = 'root'
            self.unresolved[mn][1] = '='
            found = False
            while(mn != 'humn'):
                mv = self.unresolved.pop(mn)
                #print("analyse", mn, "=",mv)
                if mv[1] == '=':
                    if type(mv[0])==int: 
                        mn, mv = (mv[2], mv[0])
                    else:
                        mn, mv = (mv[0], mv[2])
                elif mv[1] == '+':
                    if type(mv[0])==int:
                        mn, mv = (mv[2], self.resolved[mn] - mv[0])
                    else:
                        mn, mv = (mv[0], self.resolved[mn] - mv[2])
                elif mv[1] == '-':
                    if type(mv[0])==int:
                        mn, mv = (mv[2], mv[0] - self.resolved[mn])
                    else:
                        mn, mv = (mv[0], mv[2] + self.resolved[mn])
                elif mv[1] == '*':
                    if type(mv[0])==int:
                        mn, mv = (mv[2], self.resolved[mn] // mv[0])
                    else:
                        mn, mv = (mv[0], self.resolved[mn] // mv[2])
                elif mv[1] == '/':
                    if type(mv[0])==int:
                        mn, mv = (mv[2], mv[0] // self.resolved[mn])
                    else:
                        mn, mv = (mv[0], mv[2] * self.resolved[mn])
                #print(mn, "=", mv)
                self.resolved[mn] = mv


        self.soluce = self.resolved.pop('root', "Perdu") if not part2 else self.resolved.pop('humn', 'perdu')
        #self.display()
        print (self.f, self.part, self.soluce)

    def display(self, prefix=""):
        print(prefix)
        print (" Unrseolved", self.unresolved)
        print (" dependancy", self.dependancy)
        print (" resolved", self.resolved)


m = Maze('inputest', "part 1")
m.solve()

m = Maze('input', "part 1")
m.solve()

m = Maze('inputest', "part 2")
m.solve(True)

m = Maze('input', "part 2")
m.solve(True)

