import functools
# open the file containing the plays
with open('04/input.txt') as f:
  input_string = f.read()
lines = input_string.split('\n')

def include(a):
    b = list(map(lambda s: list(map(int,s.split("-"))), a.split(",")))
    return (b[0][0] <= b[1][0] and b[0][1] >= b[1][1]) or (b[1][0] <= b[0][0] and b[1][1] >= b[0][1])

print(list(map(include,lines)).count(True))

# Part 2

def disjoints(a):
    b = list(map(lambda s: list(map(int,s.split("-"))), a.split(",")))
    return (b[0][0] > b[1][1] or b[0][1] < b[1][0])

print(list(map(disjoints,lines)).count(False))