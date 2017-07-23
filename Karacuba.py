import math

def multiply_karacuba(a, b):
    if len(a) != len(b):
        nules = int(math.fabs(len(b) - len(a)))
        if len(a) < len(b):
            a = '0'*nules + a
        else:
            b = '0'*nules + b
        return multiply_karacuba(a, b)
    elif len(a) > 1 and len(b) >1:
        a1 = a[0 : int(len(a)/2)]
        a2 = a[int(len(a)/2) : len(a)]
        b1 = b[0 : int(len(a)/2)]
        b2 = b[int(len(a)/2) : len(a)]
        a1b1 = multiply_karacuba(a1, b1)
        a2b2 = multiply_karacuba(a2, b2)
        a1sa2 = int(a1 + a2)
        b1sb2 = int(b1 + b2)
        third = multiply_karacuba(str(a1sa2), str(b1sb2)) - a1b1 - a2b2
        return int(10**len(a)*a1b1 + 10**(len(a)/2)*third + a2b2)
    else:
        return int(a) * int(b)

def main():
    a = input()
    b = input()
    print("{:}".format(multiply_karacuba(a, b)))

if __name__ == "__main__":
    main()