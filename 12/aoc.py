import functools, time

class Maze():
    def __init__(self, f):
        with open('12/'+f+'.txt') as f:
            input_string = f.read()
        lines = input_string.split("\n")
        self.h=len(lines)
        self.w=len(lines[0])
        self.carte=[[-1 for x in range(self.w)] for y in range(self.h)]
        self.cartebyalti=[[[0 for x in range(self.w)] for y in range(self.h)] for h in range(26)]
        self.xstart = self.ystart = self.xend = self.yend = 0
        self.zoneexit=[dict() for h in range(26)]
        self.dists = dict()
        for li in range(self.h):
            for l in range(self.w):
                self.carte[li][l]=ord(lines[li][l])-ord('a') if lines[li][l] not in ('S', 'E') else 0 if lines[li][l] =='S' else 25
                self.cartebyalti[self.carte[li][l]][li][l] = 1
                if lines[li][l] == 'S': self.xstart, self.ystart = l, li
                elif lines[li][l] == 'E': self.xend, self.yend = l, li
        #self.display(self.carte)
        #print("xy end", self.xend, self.yend)
        #time.sleep(2)
        for h in range(25, -1, -1):
            #print("HAUTEUR = ",h)
            #if h in[6,7]:
                #print("exits ",h+1, self.zoneexit[h+1])
                #self.displ
                # ay(self.cartebyalti[h+1])
            self.markzonbyh(h)

    def solve(self, part):
        self.soluce = self.w*self.h
        print(part, self.minexit((self.xstart, self.ystart), 0))
        
    def minexit(self, xy, actualcount):
        if xy == (self.xend, self.yend): return actualcount
        h = self.carte[xy[1]][xy[0]]
        z = self.cartebyalti[h][xy[1]][xy[0]]
        #if h==2 and z==3: self.display(self.cartebyalti[h])
        #print("minexit xy, actualcount, h, z", xy, actualcount, h, z)
        #print("self.zoneexit[h]", self.zoneexit[h])
        #print("self.zoneexit[h][z]", self.zoneexit[h][z])
        for xye in self.zoneexit[h][z]:
            me = self.minexit(xye, actualcount + self.mindist(h+1, xy, xye))
            if me < self.soluce:
                self.soluce = me
        return self.soluce

    def mindist(self, h, xy, xye):
        if (xy,xye) not in self.dists: 
            #TODO
            self.dists[(xy, xye)] = abs(xye[0]-xy[0])+abs(xye[1]-xy[1])
        #if xye == (self.xend, self.yend):            print("exit dist from xy", xy, "=", self.dists[(xy,xye)])
        return self.dists[(xy,xye)]

    def removedeadend(self, h , zone):
        if h==10000:
            print("removedeadend h,zone", h, zone)
            print("exits:",self.zoneexit[h])
            print("Before removal")
            self.display(self.cartebyalti[h])
        for li in range(len(self.cartebyalti[h])):
            for l in range(len(self.cartebyalti[h][li])):
                if self.cartebyalti[h][li][l] == zone: self.cartebyalti[h][li][l] = 0
        if h==10000:
            print("After removal")
            self.display(self.cartebyalti[h])

    def markzonbyh(self,h):
        #if h==10:print("markzonbyh h", h)
        zone=2
        xy = self.findnext(h)
        while xy:
            if not self.markadjacent(h, zone, xy):
                #if h==10 : print("markzonbyh: markadjacent h, zone, xy return False", h, zone, xy)    
                self.removedeadend(h, zone)
                zone -= 1
            #elif h==10 : print("markzonbyh: markadjacent OK h=2, zone=2, xy ", xy)    
            zone += 1
            xy = self.findnext(h)
        
    def findnext(self, h):
        #if h==10:print("findnext h=", h)
        for li in range(len(self.cartebyalti[h])):
            for l in range(len(self.cartebyalti[h][li])):
                if self.cartebyalti[h][li][l] == 1:
                    #if h==7:print("findnext found h,(xy)",h, (l, li))
                    return (l,li)
        #if h==8:print("findnext NotFound for h=",h)
        #self.display(self.cartebyalti[h])
        return False

    def markadjacent(self, h, zone, xy):
        #if h==7 and xy == (39,35): print("markadjacent h,zone,xy = ", h, zone, xy)
        #print("markadjacent marking h, xy, zone", h, xy, zone)
        self.cartebyalti[h][xy[1]][xy[0]] = zone
        if h==25 and xy[1] == self.yend and xy[0] == self.xend:
            #print("markadjacent adding exit h, xy for zone", h, (xy[0], xy[1]), zone)
            if zone in self.zoneexit[h]:
                self.zoneexit[h][zone].append((xy[0], xy[1]))
            else:
                self.zoneexit[h][zone] = [(xy[0], xy[1])]
        for direction in range(4):
            dx,dy = dir(direction)
            if 0 <= xy[0]+dx < self.w and 0 <= xy[1]+dy < self.h:
                #if h==7 and xy == (38,34): print("direction", dx,dy)
                if self.cartebyalti[h][xy[1]+dy][xy[0]+dx] == 1:
                    #if h==7 :print("markadjacent marking adjacent h, xy, zone", h, (xy[0]+dx, xy[1]+dy), zone)
                    self.cartebyalti[h][xy[1]+dy][xy[0]+dx] = zone
                    self.markadjacent(h, zone, (xy[0]+dx, xy[1]+dy))
                if (h==25 and xy[1]+dy == self.yend and xy[0]+dx == self.xend) or (h<25 and self.cartebyalti[h+1][xy[1]+dy][xy[0]+dx] > 0):
                    #print("markadjacent adding exit h, xy for zone", h, (xy[0]+dx, xy[1]+dy), zone)
                    if zone in self.zoneexit[h]:
                        self.zoneexit[h][zone].append((xy[0]+dx, xy[1]+dy))
                    else:
                        self.zoneexit[h][zone] = [(xy[0]+dx, xy[1]+dy)]
        return zone in self.zoneexit[h]

    def display(self, carte):
        print("\n".join((map(lambda li: "".join([chr(ord('a')+l) for l in li]), carte))))
        #print (self.carte, self.xstart, self.ystart, self.xend, self.yend)

def dir(d):
    match d:
        case 0: return -1, 0
        case 1: return  0, 1
        case 2: return  1, 0
        case _: return  0,-1

m = Maze('inputest')
m.solve("part 1")
m = Maze('input')
m.solve("part 2")