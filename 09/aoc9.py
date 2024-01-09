import functools

rope_len=0
x=[]
y=[]
lines=[]

def puzzle(part, infile, rope):
    global rope_len, x, y, lines
    with open('09/' + infile + '.txt') as f:
        input_string = f.read()
    lines = input_string.split('\n')

    # nb of knots in the rope (2 or 10)
    rope_len=rope
    # initialise the position of the knots
    x=[0]*rope_len 
    y=[0]*rope_len
    # initialise the history of tail position with the initial position
    pos_tail = dict()
    pos_tail[(0,0)]=True

    # Main : compute each input line
    for l in lines:
        l=l.split(" ") # l = [directionULDR, nb_moves]
        # loop iterative identical moves
        for _ in range(int(l[1])):
            # Manualy moves the Head accordind to input file direction
            dx1, dy1 = dir(l[0])
            x[0] += dx1
            y[0] += dy1
            # Automatically move following knots based on puzzle rules
            for k in range(1, rope_len):
                # Except for the Tail, try to move the knot, stop if knot doesn't move
                if k < rope_len -1:
                    if not move(k): break
                # If the Tail moves, record the position in the dict of tail moves
                elif move(k) : pos_tail[(x[k],y[k])] = True 
                #1 + (0 if (x[a],y[a]) not in pos_tail else pos_tail[(x[a],y[a])])
    print("Part"+part, "tail:",rope_len, "/ input:", infile+'.txt', " / nb of tail positions:", len(pos_tail))

# Transform input direction (Up, Down, Left, Right) in variation (dx, dy)
def dir(d):
    match d:
        case "U": return 0, 1
        case "R": return 1, 0
        case "D": return 0,-1
        case _: return  -1, 0

# Define Sign function
sign = lambda x: x and (-1 if x < 0 else 1)

# compute the move of knot number i (>0) of the rope
# based on the position of the previous knot
# return if the knot moved (bool)
def move(i):
    global x, y
    mx, my = (x[i-1]-x[i], y[i-1]-y[i])
    # No move needed if contiguous node
    if abs(mx) <= 1 and abs(my) <= 1:
        return False
    # move the knot number i and return that it moved
    x[i] += sign(mx)
    y[i] += sign(my)
    return True

# For debug only : Print the grid a*b
def p_grid(a,b):
    global x, y
    li=[["."]*a for _ in range(b)] # empty grid with "."
    for ind in range(rope_len-1, -1, -1):  li[y[ind]][x[ind]] = str(ind) if ind>0 else "H" # Add the knots
    for j in range(b-1, -1,-1): print("".join(li[j]))
    print(" ")


for (part, inf,rop) in [("1", "inputest", 2), ("1", "input", 2), ("2", "inputest", 10), ("2", "inputest2", 10), ("2", "input", 10)]:
    puzzle(part, inf, rop)