import functools, time

class Maze():
    def __init__(self, f):
        with open('12/'+f+'.txt') as f:
            input_string = f.read()
        lines = input_string.split("\n")
        self.h=len(lines)
        self.w=len(lines[0])
        self.carte=[[-1 for x in range(self.w)] for y in range(self.h)]
        self.cartecost=[[-1 for x in range(self.w)] for y in range(self.h)]
        self.xend = self.yend = 0
        self.start = []
        for li in range(self.h):
            for l in range(self.w):
                self.carte[li][l]=ord(lines[li][l])-ord('a') if lines[li][l] not in ('S', 'E') else 0 if lines[li][l] =='S' else 25
                if lines[li][l] in ['S','a'] :
                    self.start.append((l, li))
                    self.cartecost[li][l] = 0
                elif lines[li][l] == 'E': self.xend, self.yend = l, li

    def solve(self, part):
        for xstart,ystart in self.start:
            self.etudie((xstart,ystart), 0)
        print(part, self.cartecost[self.yend][self.xend])
        
    def etudie(self, xy, actualcount):
        #self.display(self.cartecost)
        if xy == (self.xend, self.yend):
            print("Une soluce trouvee a", actualcount)
            return
        h = self.carte[xy[1]][xy[0]]
        for direction in range(4):
            dx,dy = dir(direction)
            # PAS Hors puzzle ET
            # PAS passage interdit (trop haut) ET
            # PAS passage sur un point avec un parcours existant mieux disant
            if (0 <= xy[0]+dx < self.w and 0 <= xy[1]+dy < self.h) and (self.carte[xy[1]+dy][xy[0]+dx] <= self.carte[xy[1]][xy[0]]+1) and (actualcount+1 < self.cartecost[xy[1]+dy][xy[0]+dx] or self.cartecost[xy[1]+dy][xy[0]+dx] == -1) :
                #print("parcours ok",(xy[0]+dx,xy[1]+dy), "vaut", actualcount+1 )
                self.cartecost[xy[1]+dy][xy[0]+dx] = actualcount+1
                self.etudie((xy[0]+dx, xy[1]+dy), actualcount+1)

    def display(self, carte):
        print("\n".join((map(lambda li: "".join([chr(ord('a')+l) for l in li]), carte))))

def dir(d):
    match d:
        case 0: return -1, 0
        case 1: return  0, 1
        case 2: return  1, 0
        case _: return  0,-1

m = Maze('inputest')
m.solve("part 1")
time.sleep(4)
m = Maze('input')
m.solve("part 2")