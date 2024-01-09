import functools, time, copy
import numpy as np

class Maze():
    def __init__(self, f, part):
        self.f = f
        self.part = part
        with open('19/'+f+'.txt') as fi:
            input_string = fi.read()
        lines = input_string.split("\n")
        self.costs=dict()
        self.result=dict()
        for il in range(len(lines)):
            e = lines[il].split(" ")
            self.costs[int(e[1].split(":")[0])] = {"or": {"or":int(e[6]),  "cl":0,"ob":0, "ge":0},
                                                   "cl": {"or":int(e[12]), "cl":0,"ob":0, "ge":0},
                                                   "ob": {"or":int(e[18]), "cl": int(e[21]), "ob":0, "ge":0},
                                                   "ge": {"or":int(e[27]), "cl":0, "ob":int(e[30]), "ge":0},
                                                   "max":{"or":max(int(e[12]), int(e[18]), int(e[27])), "ob":int(e[30]), "cl":int(e[21]), "ge":999}}
        self.soluce = 0
        self.allres = ("or", "cl", "ob", "ge")

    # Optimal for 1 ressource is True if type=geode or 
    def isoptim(self, cost, m, type, res, rob):
        x=rob[type]
        y=res[type]
        t=self.minutes-m
        z=cost["max"].get(type,0)
        return type == 'ge' or x*t+y < t*z

    # Retourne une situation finale (a m+1) à partir d'une situation s et d'un choix c d'achat de robot
    def tour(self, cost, res, rob, c):
        cor = res["or"]-(c=="ge")*cost["ge"]["or"]-(c=="ob")*cost["ob"]["or"]-(c=="cl")*cost["cl"]["or"]-(c=="or")*cost["or"]["or"]
        ccl = res["cl"]-(c=="ob")*cost["ob"]["cl"]
        cob = res["ob"]-(c=="ge")*cost["ge"]["ob"]
        if cor < 0 or ccl < 0 or cob < 0:
            print("ERREUR : cor", cor, "ccl", ccl, "cob", cob)
            end
        ret= ({"or":cor + rob["or"], "cl":ccl + rob["cl"], "ob":cob + rob["ob"], "ge":res["ge"] + rob["ge"]},
              {"or": rob["or"] + (c=="or"), "cl": rob["cl"] + (c=="cl"), "ob": rob["ob"] + (c=="ob"), "ge": rob["ge"] + (c=="ge")})
        #print ("ret tour", ret,"", end="")
        return ret

    def findoptim(self, cost, situation_init):
        result = 0
        prnt=True
        pile = []
        pile.append((1,situation_init[0],situation_init[1],""))
        while pile:
            m, res, rob, choix = pile.pop()
            #if prnt and m==3 and res['or']==1 and res['cl']==res['ob']==res['ge']==0: print("m=",m,"res=",res,"rob=",rob,"c=",choix)
            start=time.time()
            #if prnt: print ("minute", m, "best", result, "taille pile", len(pile), "", end="")
            # On ne continue pas si la production hypothetique d'un robot Ge et les ress associées ne permettent pas d'atteindre le best courant
            t = self.minutes - m +1
            if res["ge"] + rob["ge"]*t + t*(t+1)//2 < result:
                #if prnt: print ("best inatteignable, stop", res,rob,"", end="")
                continue
            # Pas de construction la dernière minute
            if t > 1:
                # On cherche si la construction de chaque robot est possible et nécessaire
                for ty in self.allres:
                    if rob[ty] >= cost["max"][ty]: continue
                    if not choix and all(res[_]-rob[_]>=cost[ty][_] for _ in self.allres): continue
                    if not self.isoptim(cost, m, ty, res, rob): continue
                    if all(res[_] >= cost[ty][_] for _ in self.allres) :
                        newres, newrob = self.tour(cost, res, rob, ty)
                        pile.append((m+1, newres, newrob, ty))
                newres, newrob = self.tour(cost, res, rob, "")
            if res['ge']+rob["ge"]*t>result:
                result = res['ge']+rob["ge"]*t
            if t > 0:
                pile.append((m+1, newres, newrob, ""))
        return result

    def solve(self, part2 = False):
        self.soluce = 0 if not part2 else 1
        self.minutes = 24 if not part2 else 32
        for idx in self.costs.keys():
            if part2 and idx > 3: continue
            result = self.findoptim(self.costs[idx], ({_:0 for _ in self.allres}, {_:_ == "or" for _ in self.allres}))
            #print("ligne",idx,"best-ge", result, "quality", result*idx)
            self.soluce = (self.soluce + result*idx) if not part2 else self.soluce*result
        print (self.f, self.part, self.soluce)

    def display(self):
        print ("TODO")


m = Maze('inputest', "part 1")
m.solve()

m = Maze('input', "part 1")
m.solve()

m = Maze('inputest', "part 2")
m.solve(part2=True)

m = Maze('input', "part 2")
m.solve(part2=True)

