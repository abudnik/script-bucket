import random
import matplotlib.pyplot as plt


def Equation(r, xn):
    return r*xn*(1.0-xn)

points_per_iter = 250


def Avg(s):
    avg = 0.0
    for e in s:
        avg += e
    return avg / len(s)

def ComputeStep(r):
    x0 = random.random()
    max_iter = 10000
    xn = x0

    for i in range(0, max_iter):
        xn = Equation(r, xn)

    s = []
    for i in range(0, points_per_iter):
        xn = Equation(r, xn)
        s.append(xn)

    avg = Avg(s)

    print r, xn, avg
    return s, avg

def Main():
    r_min = 2.8
    r_max = 4.0
    r_step = 0.001
    r = r_min

    xs = []
    ys = []

    avgx = []
    avgy = []

    while r < r_max:
        s, avg = ComputeStep(r)
        ys.append( s )
        xs.append( [r for i in range(0, points_per_iter)] )
        avgy.append(avg)
        avgx.append(r)
        r += r_step

    plt.plot(xs, ys, 'ko', markersize=1)
    plt.plot(avgx, avgy, 'ro')
    plt.show()

Main()
