import functools
# open the file containing the plays
with open('03/input.txt') as f:
  input_string = f.read()
lines = input_string.split('\n')


prio = lambda c: ord(c) + (1 - ord("a") if ord(c) > ord("Z") else 27 - ord("A"))

def commun(s1,s2):
    tab = [False]*53
    for c in s1:
        tab[prio(c)] = True
    for c in s2:
        if tab[prio(c)]:
            return prio(c)

somme = functools.reduce(lambda acc, e : acc + commun(e[0],e[1]),
    map(lambda s: (s[:len(s)//2], s[len(s)//2:]), lines), 0)

print(somme)



# PART 2

groupedlines = [(lines[3*k],lines[3*k+1],lines[3*k+2]) for k in range(len(lines)//3)]

def commun3(s1,s2,s3):
    tab = [0]*53
    for c in s1:
        tab[prio(c)] = 1
    for c in s2:
        if tab[prio(c)] == 1:
            tab[prio(c)] = 2
    for c in s3:
        if tab[prio(c)] == 2:
            return prio(c)

somme = functools.reduce(lambda acc, e : acc + commun3(e[0],e[1],e[2]),groupedlines, 0)

print(somme)