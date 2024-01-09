import functools
# open the file containing the plays
with open('02/input.txt') as f:
  input_string = f.read()
lines = input_string.split('\n')

score = functools.reduce(lambda acc, e : acc + (3*(((e[1]-e[0]+1)%3)) + e[1]+1),
    map(lambda s: (ord(s[0])-ord("A"), ord(s[2])-ord("X")), lines), 0)
print(score)

score=0
for line in lines:
    i, j = ord(line[0])-ord("A"), ord(line[2])-ord("X")
    score += 3*((j-i+1)%3) + j + 1
print (score)


# Part 2

score = functools.reduce(lambda acc, e : acc + (e[1]*3 + 1+(e[1]+e[0]+2)%3),
    map(lambda s: (ord(s[0])-ord("A"), ord(s[2])-ord("X")), lines), 0)
print(score)

score=0
for line in lines:
    i, j = ord(line[0])-ord("A"), ord(line[2])-ord("X")
    score += 3*j + 1+(i+j+2)%3 
print (score)