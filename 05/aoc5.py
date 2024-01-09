import functools
with open('05/input.txt') as f:
  input_string = f.read()
lines = input_string.split('\n')

nbstacks = (len(lines[0])+1)//4
stacks = [[] for _ in range(nbstacks)]
debut = 0
for i in range(len(lines)):
    if debut==0 :
        if not ('['  in lines[i]) :
            for j in range(i-1, -1, -1):
                for c in range(nbstacks):
                    crate = lines[j][1+4*c]
                    if crate != ' ':
                        stacks[c].append(crate)
            debut = 1
    elif debut == 1: debut = 2 
    else:
        move = lines[i].split(" ")
        interm = []
        for _ in range(int(move[1])):
            interm.append(stacks[int(move[3]) - 1].pop())
        for _ in range(int(move[1])):
            stacks[int(move[5]) - 1].append(interm.pop())

print(functools.reduce(lambda acc, s: acc+s, map(lambda l: l[-1], stacks), ""))
