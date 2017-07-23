#!/usr/bin/python3


DFS = []
f = {}
t = 0


def strong_conn_component(g):

    dfs_loop(g)
    ng = trans_g(g)
    dfs_loop_t(ng)


def dfs_loop_t(g):

    global DFS, t
    DFS = []
    t = 0
    for v in sorted(f, key=f.get, reverse=True):
        if v not in DFS:
            dfsr(g, v)


def trans_g(g):
    newg = {}
    for v in g.keys():
        for s in g[v]:
            if s in newg.keys():
                newg[s].append(v)
            else:
                newg[s] = [v]

    return newg


def dfs_loop(g):

    global DFS, t
    DFS = []
    t = 0
    for v in g.keys():
        if v not in DFS:
            dfsr(g, v)


def dfsr(g, s):

    global t, DFS
    DFS.append(s)
    if s in g.keys():
        for u in g[s]:
            if u not in DFS:
                dfsr(g, u)
    t += 1
    f[s] = t

"""def dfsr(g, s, k):
    global DFS
    DFS[s] = k
    if s in g.keys():
        for u in g[s]:
            if u not in DFS.keys():
                k = dfsr(g, u, k+1)
    return k"""


def build_graph():
    graph_dict = {}
    with open("test_08_1.txt", "r") as graph:
        for line in graph:
            i, number = line.split()
            if i in graph_dict.keys():
                graph_dict[i].append(number)
            else:
                graph_dict[i] = [number]
    return graph_dict


def main():

    g = build_graph()
    strong_conn_component(g)
    print(f)

if __name__ == "__main__":
    main()
