import functools
with open('10/input.txt') as f:
    input_string = f.read()
lines = input_string.split('\n')

ticks = " ".join(lines).split(' ')

x=1
sum=0
for i,t in enumerate(ticks[:221]):
    if not (i+21)%40: sum += (i+1)*x
    try:
        x += int(t)
    except ValueError :
        pass
print("Part1", sum)


x=1
img = ""
for i,t in enumerate(ticks):
    img += "#" if abs(x-(i%40)) < 2 else "."
    if not (i+1)%40: img += "\n" 
    try:
        x += int(t)
    except ValueError :
        pass

print("Part2")
print(img)
