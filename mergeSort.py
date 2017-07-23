#!/usr/bin/python

def merge(mass1, mass2):
    mass = []
    for i in mass1:
        for j in mass2:
            if j < i:
                mass.append(j)
            else:
                mass.append(i)
                break

def merge_sort(mass, l, r):
    if l < r:
        middle = (l+r)/2
        merge(merge_sort(mass, l, middle), merge_sort(mass, middle + 1, r))

def main():
    mass = list(map(int, input().split()))
    merge_sort(mass, 0, len(mass) - 1)
    print(mass)


if __name__ == "__main__":
    main()