#!/usr/bin/python3

c = 0

def count_c(p, r):
    global c
    c += r-p

def portion(mass, p, r):
    x = mass[r]
    i = p - 1
    for j in range(p, r-1):
        if  mass[j] <= x:
            i += 1
            b = mass[i]
            mass[i] = mass[j]
            mass[j] = mass[i]
    count_c(p, r - 1)
    s = mass[r]
    mass[r] = mass[i+1]
    mass[i+1] = mass[r]
    return i + 1

def quick_sort(mass, p, r):
    if p < r:
        q = portion(mass, p, r)
        quick_sort(mass, p, q - 1)
        quick_sort(mass, q + 1, r)

def main():
    mass = []
    with open("input__10000.txt", 'r') as input_file:
        n = int(input_file.readline())
        for i in range(n):
            mass.append(int(input_file.readline()))
    quick_sort(mass, 0, n-1)
    print(mass)
    print(c)



if __name__ == "__main__":
    main()