#!/usr/bin/python3

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

def main():
    a = [2, 5, 3, 0, 2, 3, 0, 3]
    b = []
    for i in range(len(a) + 1):
        b.append(0)
    k = max(a)
    counting_sort(a, b, k)
    b.pop(0)
    print(b)

if __name__ == "__main__":
    main()