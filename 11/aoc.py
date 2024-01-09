import functools, time
with open('11/input.txt') as f:
    input_string = f.read()
lines = input_string.split("\n\n")

class Monkey():
    def __init__(self, lines, d):
        lines_list = lines.split("\n")
        self.id = int(lines_list[0][-2])
        self.items = list(map(int,lines_list[1].split(":")[1].split(",")))
        self.op = eval("lambda old:" + lines_list[2].split("=")[1])
        self.montrue = int(lines_list[4].split(" ")[-1])
        self.monfalse = int(lines_list[5].split(" ")[-1])
        self.test_nb = int(lines_list[3].split(" ")[-1])
        self.test = lambda i: self.monfalse if (i%self.test_nb) else self.montrue
        self.activity = 0
        self.d = d

    def turn(self):
        envois = {self.montrue : [] , self.monfalse : []}
        for _ in range(len(self.items)):
            i = self.items.pop(0)
            self.activity += 1
            new = self.op(i) // self.d
            new = new % ppcm
            envois[self.test(new)].append(new)
        return envois

    def attrape_objet(self, items):
        self.items += items

monkeys = [Monkey(l,3) for l in lines]
ppcm = functools.reduce(lambda c, t: c*t, map(lambda m: m.test_nb, monkeys), 1)
for _ in range(20):
    for m in monkeys:
        for m_cible, items in m.turn().items():
            monkeys[m_cible].attrape_objet(items)

monkeys.sort(key=(lambda m: -m.activity))
print("part 1", monkeys[0].activity * monkeys[1].activity)
#10605

monkeys = [Monkey(l,1) for l in lines]
ppcm = functools.reduce(lambda c, t: c*t, map(lambda m: m.test_nb, monkeys), 1)

for i in range(10000):
#    if not ((i+1)%1000) :
#        print("Round ", i+1)
#        for m in monkeys:
#            print("Monkey ",m.id," activity : ", m.activity," items : ", m.items)
    for m in monkeys:
        for m_cible, items in m.turn().items():
            monkeys[m_cible].attrape_objet(items)

monkeys.sort(key=(lambda m: -m.activity))
print("part 2", monkeys[0].activity * monkeys[1].activity)

