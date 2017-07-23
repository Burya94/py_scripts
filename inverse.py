#!/usr/bin/python3


def merge_and_inverse(mass, le, ri):
     c = 0
     j = 0
     i = 0
     for k in range(len(le)+len(ri)):
         if i > len(le)-1 and j > len(ri) -1 :
             break
         elif  i > len(le)-1:
             j +=1
             continue
         elif j > len(ri) - 1:
             i +=1
             continue
         if le[i] <= ri[j]:
             mass.append(le[i])
             i += 1
         else:
             mass.append(ri[j])
             j += 1
             c = c + (len(le) - i + 1)
     return mass, c

def sort_and_find_inverse(mass):
    if len(mass) == 1:
        return mass, 0
    else:
        r = int(len(mass)/2)
        left, x = sort_and_find_inverse(mass[0 : r])
        right, y = sort_and_find_inverse(mass[r : len(mass)])
        mass, z = merge_and_inverse(mass, left, right)
        return mass, x + y + z



def main():
    n = int(input())
    mass = list(map(int, input().split()))
    print(sort_and_find_inverse(mass)[1])


if __name__ == "__main__":
    main()