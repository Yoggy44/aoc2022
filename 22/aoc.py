import functools, time, copy
import numpy as np

class Maze():
    def __init__(self, f, part):
        self.f = f
        self.part = part
        with open('22/'+f+'.txt') as fi:
            input_string = fi.read()
        lines = input_string.split("\n")
        self.trajet = lines.pop()
        self.map = lines[:-1]
        self.dir = 0
        self.pos = [self.map[0].index('.'), 0]
        a = len(self.map)
        b = functools.reduce(lambda c,x: max(c,len(x)), self.map, 0)
        while a!=b: 
            d=abs(b-a)
            b=a 
            a=d 
        self.cubesize=d
    #    self.display()
    
    def nextmove(self):
        if self.trajet[0] in ('R','L'):
            idx = 1
        else:
            r = self.trajet.find('R') if 'R' in self.trajet else len(self.trajet)
            l = self.trajet.find('L') if 'L' in self.trajet else len(self.trajet)
            idx = min(r, l)
        ret = self.trajet[:idx]
        self.trajet = self.trajet[idx:]
        #print ('Next move', ret)
        return ret

    def move1(self):
        if self.dir == 0:
            lign = self.map[self.pos[1]]
            if len(lign) == self.pos[0]+1:
                if lign.strip()[0] == '.':
                    self.pos[0] = lign.find('.')
                    return True
            elif lign[self.pos[0]+1] == '.':
                self.pos[0] += 1
                return True
        elif self.dir == 2:
            lign = self.map[self.pos[1]]
            if self.pos[0] == len(lign.strip('.#')) :
                if lign[-1] == '.':
                    self.pos[0] = len(lign) - 1
                    return True
            elif lign[self.pos[0]-1] == '.':
                self.pos[0] -= 1
                return True
        else:
            f = False
            nli = self.pos[1]
            while not f:
                nli = (nli + (2 - self.dir)) % len(self.map)
                if nli >= 0 and nli < len(self.map) and len(self.map[nli]) > self.pos[0] and self.map[nli][self.pos[0]] != ' ':
                    f = True
                    if self.map[nli][self.pos[0]] == '.':
                        self.pos[1] = nli
                        return True
        return False

    def checkmove2(self,nx, ny, dir):
        if self.map[ny][nx] == '.':
            self.dir = dir
            self.pos = [nx, ny]
            #print (" => OK", self.pos, self.dir)
            return True
        else:
            #print(" ", nx, ny, self.map[ny][nx], " => KO")
            return False

    def move2(self):
        kp = (self.pos[0]//self.cubesize, self.pos[1]//self.cubesize)
        #print (self.pos, self.dir)
        if self.dir == 0:
            lign = self.map[self.pos[1]]
            if len(lign) == self.pos[0]+1:
                #print ("bout de ligne vers la droite en", kp)
                if kp == (0, 3):
                    return self.checkmove2(self.cubesize + self.pos[1]%self.cubesize, 3 * self.cubesize - 1, 3)
                elif kp == (1, 2):
                    return self.checkmove2(3 * self.cubesize - 1, self.cubesize - 1 - self.pos[1]%self.cubesize, 2)
                elif kp == (1, 1):
                    return self.checkmove2(2 * self.cubesize + self.pos[1]%self.cubesize, self.cubesize - 1, 3)
                elif kp == (2, 0):
                    return self.checkmove2(2 * self.cubesize - 1, 3 * self.cubesize - 1 - self.pos[1]%self.cubesize, 2)
                elif self.pos[1]//self.cubesize > 0 :
                    if self.pos[1]+self.cubesize < len(self.map) and self.pos[0]+self.cubesize < len(self.map[self.pos[1]+self.cubesize]):
                        if self.map[self.cubesize*(1+(self.pos[1]//self.cubesize))][self.pos[0]+self.cubesize-(self.pos[1]%self.cubesize)] == '.':
                            self.dir = 1
                            self.pos = [self.pos[0]+self.cubesize-(self.pos[1]%self.cubesize), self.cubesize*(1+(self.pos[1]%self.cubesize))]
                            return True    
                else:
                    print("TODO")
                    return False
            elif lign[self.pos[0]+1] == '.':
                self.pos[0] += 1
                return True
            else:
                return False
        elif self.dir == 2:
            lign = self.map[self.pos[1]]
            if self.pos[0] == len(lign.strip('.#')) :
                #print ("bout de ligne vers la gauche en", kp)
                if kp == (0, 3):
                    return self.checkmove2(self.cubesize + self.pos[1]%self.cubesize, 0, 1)
                elif kp == (0, 2):
                    return self.checkmove2(self.cubesize, self.cubesize - self.pos[1]%self.cubesize - 1, 0)
                elif kp == (1, 1):
                    return self.checkmove2(self.pos[1]%self.cubesize, 2 * self.cubesize, 1)
                elif kp == (1, 0):
                    return self.checkmove2(0, 3 * self.cubesize - 1 - self.pos[1]%self.cubesize, 0)
            elif lign[self.pos[0]-1] == '.':
                self.pos[0] -= 1
                return True
            else:
                return False
        else:
            #print (self.pos, self.dir)
            if self.dir == 3 and (self.pos[1] == 0 or self.map[self.pos[1] - 1][self.pos[0]] == ' '):
                #print ("bout de colonne vers le haut en", kp)
                if kp == (0, 2):
                    return self.checkmove2(self.cubesize, self.cubesize + self.pos[0]%self.cubesize, 0)
                elif kp == (1, 0):
                    return self.checkmove2(0, 3 * self.cubesize + self.pos[0]%self.cubesize, 0)
                elif kp == (2, 0):
                    return self.checkmove2(self.pos[0]%self.cubesize, 4 * self.cubesize - 1, 3)
                elif kp == (1, 1):
                    return self.checkmove2(2 * self.cubesize, self.pos[0]%self.cubesize, 0)
            elif self.dir == 1 and (self.pos[1] + 1 == len(self.map) or len(self.map[self.pos[1] + 1]) <= self.pos[0] or self.map[self.pos[1] + 1][self.pos[0]] == ' '):
                #print ("bout de colonne vers le bas en ", kp)
                if kp == (0, 3):
                    return self.checkmove2(self.pos[0] +  2 * self.cubesize, 0, 1)
                elif kp == (1, 2):
                    return self.checkmove2(self.cubesize - 1, 3 * self.cubesize + self.pos[0]%self.cubesize, 2)
                elif kp == (2, 0):
                    return self.checkmove2(2 * self.cubesize - 1, self.cubesize + self.pos[0]%self.cubesize, 2)
                if kp == (2, 2):
                    if self.map[self.pos[1]-self.cubesize][self.pos[0]-self.cubesize-1-2*(self.pos[0]%self.cubesize)] == '.':
                        self.dir = 3
                        self.pos = [self.pos[0]-self.cubesize-1-2*(self.pos[0]%self.cubesize), self.pos[1]-self.cubesize]
                        return True
            elif self.map[self.pos[1] + (2 - self.dir)][self.pos[0]] == '.':
                self.pos[1] += (2 - self.dir)
                return True
            else:
                return False
        print ("todo")
        return False

    def move(self, move, part2):
        if move in ('L', 'R'):
            self.dir = (self.dir + (1 if move == 'R' else -1)) % 4
        else:
            for _ in range(int(move)):
                if not part2 and not self.move1(): break
                if part2 and not self.move2(): break

    def solve(self, part2 = False):
        while (self.trajet):
            self.move(self.nextmove(), part2)

        #self.display(f'{self.pos}{self.dir}')
        self.soluce = 1000 * (1+self.pos[1]) + 4 * (1+self.pos[0]) + self.dir
        print (self.f, self.part, self.soluce)

    def display(self, prefix=""):
        print(prefix)
        print(self.trajet)
        m = copy.copy(self.map)
        m[self.pos[1]] = f'{m[self.pos[1]][:self.pos[0]]}{">" if self.dir == 0 else "v" if self.dir == 1 else "<" if self.dir == 2 else "^"}{m[self.pos[1]][self.pos[0]+1:]}'
        print("\n".join(map(lambda li: "".join(l for l in li), m)))

m = Maze('inputest', "part 1")
m.solve()

m = Maze('input', "part 1")
m.solve()

m = Maze('inputest', "part 2")
m.solve(True)

m = Maze('input', "part 2")
m.solve(True)
# 70218 : Too low
# 126192 : Too low
# 105214 : Too low