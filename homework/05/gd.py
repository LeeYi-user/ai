import numpy as np
from numpy.linalg import norm
from engine import Value

def gradientDescendent(f, p0, h=0.01, max_loops=100000):
    p = p0.copy()
    for _ in range(max_loops):
        fp = f(p)
        fp.backward()
        gp = []
        for param in p:
            gp.append(param.grad)
        glen = norm(gp)
        if glen < 0.00001:
            break
        gh = np.multiply(gp, -1*h)
        p += gh
    print(p)
    return p

def f(p):
    [x, y, z] = p
    return (x-1)**2+(y-2)**2+(z-3)**2

p = [Value(0), Value(0), Value(0)]
print(f(gradientDescendent(f, p)))
