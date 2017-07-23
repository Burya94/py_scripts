#!usr/bin/python3



def main():
    a = [5, 2, 1, 9, 4, 3, 7]
    for i in reversed(range(len(a))):
        for j in range(1, i+1):
            if a[j-1] > a[j]:
                a[j], a[j-1] = a[j-1], a[j]
    print(a)


if __name__ == "__main__":
    main()