import numpy as np, functools

a=[1,2,3,4]
b=[1,2]

print  (a[:3], b[:3])
print([i for i in range(3) if i != 1])
r=range(1,-1,-1)
print (r)
for i in r:
    print (r)
a=[(0,2,1,1), (0,0,0,1)]

b = set(a)
print(b)
a=[1,2,4,5,3,2]
print (set(a))
a=[set()]
a[0].add(1)
a[0].add(1)
a[0].add(2)
print (a)
a = [a[0], a[0].add(2)]
print (a)
print(False*4)