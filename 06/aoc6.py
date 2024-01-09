import functools
with open('06/input.txt') as f:
  input_string = f.read()
lines = input_string.split('\n')


startlen = 14

nblet = [0]*26
nbdupl = 0

for l in lines:
    nblet = [0]*26
    nbdupl = 0
    for i in range(startlen):
        nblet[ord(l[i])-ord("a")] += 1
        if nblet[ord(l[i])-ord("a")] > 1 : nbdupl += 1
    for i in range(len(l)-startlen):
        if nbdupl == 0:
            print(startlen+i)
            break
        else:
            nblet[ord(l[i])-ord("a")] -= 1
            nbdupl -= 1 if nblet[ord(l[i])-ord("a")] > 0 else 0
            nblet[ord(l[i+startlen])-ord("a")] +=1
            nbdupl += 1 if nblet[ord(l[i+startlen])-ord("a")] > 1 else 0
print (" ")
for l in lines:
    for i in range(len(l)-startlen):
        if len(set(l[i:i+startlen]))==startlen:
            print(i+startlen)
            break

