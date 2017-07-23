#!/usr/bin/python3


def parent(x):
    return int(x/2)

def left(x):
    return 2*x

def right(x):
    return 2*x+1

def max_heapify(a, x):
    heap_size = len(a)
    l = left(x)
    largest = 0
    r = right(x)
    if l <= heap_size and a[l] > a[x]:
        largest = l
    else:
        largest = x
    if r <=heap_size and a[r] > a[largest]:
        largest = r
    if largest != x:
        b = a[x]
        a[x] = a[largest]
        a[largest] = b
        max_heapify(a, largest)


def build_max_heap(a):
    a.reverse()
    for i in range(int(len(a)/2)):
        max_heapify(a, i)

def main():

    a = [9, 10, 7, 14, 16, 8]
    build_max_heap(a)
    print(a)

if __name__ == "__main__":
    main()