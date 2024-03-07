from random import randint

citys = [
    (0,3),(0,0),
    (0,2),(0,1),
    (1,0),(1,3),
    (2,0),(2,3),
    (3,0),(3,3),
    (3,1),(3,2)
]

path = [i for i in range(len(citys))]

def distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return ((x2-x1)**2+(y2-y1)**2)**0.5

def pathLength(p):
    dist = 0
    plen = len(p)
    for i in range(plen):
        dist += distance(citys[p[i]], citys[p[(i+1)%plen]])
    return dist

length = pathLength(path)

fails = 0

def hillClimbing():
    global path
    global length
    global fails

    newPath = path.copy()

    city1 = randint(0, len(newPath) - 1)
    city2 = randint(0, len(newPath) - 1)
    newPath[city1], newPath[city2] = newPath[city2], newPath[city1]

    newLength = pathLength(newPath)

    if newLength < length:
        path = newPath
        length = newLength
        print(newPath, newLength)
    else:
        fails += 1

while fails < 10000:
    hillClimbing()
