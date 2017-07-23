#!/usr/bin/python3

import string

def counting_sort(a, b, k):
    c = []
    for j in range(k + 1):
        c.append(0)
    print(c)
    for i in range(len(a)):
        c[a[i]] += 1
    print(c)
    for j in range(1, k + 1):
        c[j] = c[j] + c[j-1]
    print(c)
    a.reverse()
    for i in range(len(a)):
        b[c[a[i]]] = a[i]
        c[a[i]] -= 1

def radix_sort(a, d):
    b =[]
    k = max(a)
    for i in range(len(a) + 1):
        b.append(0)
    for i in range(d):
        counting_sort(a, b, k)


def main():
    a = []
    with open("anagrams.txt", 'r') as base:
        for line in base:
            a.append(line.strip())
    a.sort(key=lambda x: x[2])
    a.sort(key=lambda x: x[1])
    print(a)
    alphabet = string.ascii_lowercase
    d = {}
    for i in alphabet:
        d[i] = 0
    for n in d.keys():
        c = 0
        for j in range(len(a)):
            c += a[j].count(n)
        d[n] = c
    print(d)
    print(a[0] + max(d, key=lambda x: d[x]) + a[len(a)-1])

    #radix_sort(a, 3)

if __name__ == "__main__":
    main()