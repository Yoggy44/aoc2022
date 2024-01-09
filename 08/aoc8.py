import functools
with open('08/input.txt') as f:
  input_string = f.read()
lines = input_string.split('\n')

plan = list(map(lambda l:list(map(int,l)), lines))

m = [[[-2 if x != 0 else -1, -2 if y != len(lines[0])-1 else -1, -2 if x != len(lines)-1 else -1, -2 if y != 0 else -1] for y in range(len(lines[0]))] for x in range(len(lines))]
a = [[[-1 if x != 0 else [0]*10, -1 if y != len(lines[0])-1 else  [0]*10, -1 if x != len(lines)-1 else  [0]*10, -1 if y != 0 else  [0]*10] for y in range(len(lines[0]))] for x in range(len(lines))]

def dir(d):
    match d:
        case 0: return -1, 0
        case 1: return  0, 1
        case 2: return  1, 0
        case _: return  0,-1

def plus_grands_vers_d(x,y,d):
    if m[x][y][d] != -2: return m[x][y][d]
    dx, dy = dir(d)
    m[x][y][d] = max(plan[x+dx][y+dy],plus_grands_vers_d(x+dx, y+dy, d))
    return m[x][y][d]

def visible(xy):
    x,y = xy
    for d in range(4):
        if plan[x][y] > plus_grands_vers_d(x, y, d):
            return True
    return False

def nb_arbre_vers_d(x,y,d):
    if a[x][y][d] != -1: return a[x][y][d]
    dx, dy = dir(d)
    a_suiv = nb_arbre_vers_d(x+dx, y+dy, d)
    #print(f"x = {x}, y = {y}, d = {d}, h = {plan[x][y]}, h_suiv = {plan[x+dx][y+dy]}, a_suiv = {a_suiv}")
    a[x][y][d] = list(map(lambda h: 1 if h <= plan[x+dx][y+dy] else 1 + a_suiv[h], range(10)))
    return a[x][y][d]

def nb_arbre_vers_d_h(x,y,d,h):
    if a[x][y][d][h] != -1: return a[x][y][d][h]
    dx, dy = dir(d)
    a[x][y][d][h] = 1 if plan[x+dx][y+dy] >= plan[x][y] else 1 + nb_arbre_vers_d(x+dx, y+dy, d, h)
    return a[x][y][d]

def vue(xy):
    x,y = xy
    return functools.reduce(lambda v, e: v*nb_arbre_vers_d(x, y, e)[plan[x][y]], range(4), 1)

def coord(i):
    return i//len(lines[0]), i%len(lines[0])

print("part 1", list(map(lambda i: visible(coord(i)), range(len(lines)*len(lines[0])))).count(True))

print("part 2", max(list(map(lambda i: vue(coord(i)), range(len(lines)*len(lines[0]))))))
