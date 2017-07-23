#!/usr/bin/python3

def insert_sort(mass):
    for i in range(1, len(mass)):
        j = i
        while j > 0 and mass[j] < mass[j-1]:
            b = mass[j]
            mass[j] = mass[j-1]
            mass[j-1] = b
            j -= 1


def main():
    mass = list(map(int, input().split()))
    insert_sort(mass)
    print(mass)


if __name__ == "__main__":
    main()