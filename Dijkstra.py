#!/usr/bin/python3


import math


def deikstra_search(g, start, end):
    a, b = [], []
    v = set([i for i in range(len(g))])
    for va in range(len(g)):
        a.append(math.inf)
        b.append(None)
    x = {start}
    a[start] = 0
    vc = start
    while x != v:
        for u in g[vc].keys():
            if u in v and u not in x:
                if a[u] > a[vc] + g[vc][u]:
                    a[u] = a[vc] + g[vc][u]
                    b[u] = vc
        minm = {}
        for ve in v:
            if ve not in x:
                minm[ve] = a[ve]
        vn = min(minm, key=minm.get)
        vc = vn
        x.add(vn)
        if vc == end:
            break

    return a, b


def main():
    with open("input_5_10.txt", "r") as ople:
        n = int(ople.readline().split()[0])
        g = [{}for i in range(n)]
        for line in ople:
            u, v, w = list(map(int, line.split()))
            g[u-1][v-1] = w
    print(deikstra_search(g, 0, 9))


if __name__ == "__main__":
    main()
