import math
import json

import numpy as np
from scipy.optimize import curve_fit

def transform(x, y, v):
    cosv = math.cos(v)
    sinv = math.sin(v)
    return np.array([cosv, sinv, 0, -sinv, cosv, 0, x, y, 1]).reshape(3,3)


def u0():
    P0 = np.array([1 ,1 ,1])
    T = np.array([1, 0, 0, 0, 1, 0, 0, 0, 1]).reshape(3, 3)
    T1 = np.array([1, 0, 0, 0, 1, 0, 1, 1, 1]).reshape(3, 3)
    print(T)
    print(P0)
    print(P0 @ T)
    print(P0 @ T1)
    print(P0 @ transform(2, 4, 0))
    print(P0 @ transform(0, 0, math.pi / 2))


# ----
def transform0(X, a, b, c):
    y = np.zeros(len(X), np.float64)
    for i in range(len(X)):
        x = X[i]
        #print(x[0])
        p0 = np.array([x[0], x[1], 1])
        p1 = np.array([x[2], x[3], 1])
        matrix = transform(a, b, c)
        p2 = p0 @ matrix
        p3 = p2 - p1
        dx = p3[0]
        dy = p3[1]
        y[i] = dx * dx + dy * dy
    return y

def u2():
    a0 = [1, 1, -1, 1]
    a1 = [-1, 1, -1, -1]
    x = np.stack([a0, a1, a0, a1])
    print(x)
    print(x.shape)
    y = np.array([0, 0, 0, 0])
    #print(x)
    #print(x.shape)
    popt, pcov = curve_fit(transform0, x, y)
    print(popt)
    print(pcov)

def u3():
    with open('star-cache/050__pairs.json', 'r') as fin:
        m0 = json.load(fin)
    x = np.array(m0)
    y = np.zeros(len(m0), np.float64)
    popt, pcov = curve_fit(transform0, x, y)
    print(pcov)
    print(popt)
# [ 1.66774462e+01  1.06190648e+01 -8.58275345e-05]


def main():
    #u0()
    #u2()
    u3()

if __name__ == '__main__':
    main()