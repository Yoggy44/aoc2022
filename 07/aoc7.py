import functools
with open('07/input.txt') as f:
  input_string = f.read()
lines = input_string.split('\n')

maxlen = 100000

curdir = ""
tree = dict()
tds = dict()

for l in lines :
    if l[0] in "0123456789" : #localsize
        tree[curdir][0] += int(l.split(" ")[0])
    elif l[0:4] == "dir ":
        tree[curdir][1].append(curdir+l[4:]+"/")
    elif l == "$ cd ..":
        curdir = curdir[:curdir[:-1].rfind("/")+1]
    elif l[0:4] == "$ cd":
        curdir = curdir + l[5:] + ("/" if curdir != "" else "")
        tree[curdir] = [0, []]

def size(d):
    if d in tds:
        return tds[d]
    else:
        s = tree[d][0]
        for sd in tree[d][1]:
            s += size(sd)
        tds[d] = s
        return s

print("part1", functools.reduce(lambda acc, k: acc+(size(k) if size(k) <= maxlen else 0), tree.keys(), 0))

# Part 2
total = 70000000
unusedmin = 30000000

mindelete = max(0, size("/") - total + unusedmin)

print("Part2", size(functools.reduce(lambda md,k: md if size(md) < size(k) or size(k) < mindelete else k ,tree.keys())))