#####
#Homework Number: 3
#Name: Prekshaa Veeraragavan
#ECN login: pveerar
#Due Date: February 11, 2021
#####
#!/usr/bin/env python 3.7


## FindMI.py
#reference for mult: https://stackoverflow.com/questions/3722004/how-to-perform-multiplication-using-bitwise-operators

import sys

if len(sys.argv) != 3:
    sys.stderr.write("Usage: %s   <integer>   <modulus>\n" % sys.argv[0])
    sys.exit(1)

NUM, MOD = int(sys.argv[1]), int(sys.argv[2])

def mult(x, y):
    r = 0   ##var to return
    while (y > 0):      ##for positive ints
        if (y & 1):     ##check if odd
            r = r + x   ##add 1x to itself

        x = x << 1      ##multiply by 2
        y = y >> 1      ##divide by 2, because multiplicatio(by 2) taken care of

    return r

def div(x, y):

    quo = 0 ##quotient

    if (x < y):
        quo = 0
    elif (x == y):
        quo = 1
    else:

        while (x > y):


                x = x - y      ##remove 1y from x
                quo = quo + 1   ##update quotient odd


    return quo


def MI(num, mod):
    '''
    This function uses ordinary integer arithmetic implementation of the
    Extended Euclid's Algorithm to find the MI of the first-arg integer
    vis-a-vis the second-arg integer.
    '''
    NUM = num; MOD = mod
    x, x_old = 0, 1
    y, y_old = 1, 0
    while mod:
        q = div(num, mod)
        num, mod = mod, num % mod
        x, x_old = x_old - mult(x, q), x
        y, y_old = y_old - mult(y, q), y
    if num != 1:
        print("\nNO MI. However, the GCD of %d and %d is %u\n" % (NUM, MOD, num))
    else:
        MI = (x_old + MOD) % MOD
        print("\nMI of %d modulo %d is: %d\n" % (NUM, MOD, MI))

MI(NUM, MOD)




