#####
# Homework Number: 6
# Name: Prekshaa Veeraragavan
# ECN login: pveerar
# Due Date: March 9, 2021
#####
#!/usr/bin/env python 3.7

import sys
from BitVector import *
import PrimeGenerator
from solve_pRoot_BST import *


def gcd(a, b):
    while b:
        a, b = b, a % b
    return(a)

e = 3

def key_gen():

    goodPrimes = False     # condition to check if p,q good vals

    while (goodPrimes == False):
        # Generate prime numbers p and q
        p_q = PrimeGenerator.PrimeGenerator(bits=128)
        p = p_q.findPrime()
        q = p_q.findPrime()

        if (p != q):    #condition 1
            if ( gcd(p-1, e) == 1 and gcd(q-1, e) == 1):    # condition 2
                goodPrimes = True                           # dont have to check for cond 3, leftmost bits already set

    n = p * q

    return n

def encrypt(message, enc1, enc2, enc3, outfile):
    message_bv = BitVector(filename=message)

    n1 = key_gen()
    n2 = key_gen()
    n3 = key_gen()

    f1 = open(enc1, "w")
    f2 = open(enc2, "w")
    f3 = open(enc3, "w")
    f4 = open(outfile, "w")

    f4.write(str(n1) + '\n')
    f4.write(str(n2) + '\n')
    f4.write(str(n3))
    f4.close()

    while message_bv.more_to_read:
        plaintext_bv = message_bv.read_bits_from_file(256)
        plainLen = plaintext_bv.length()

        if (plainLen < 128):
            plaintext_bv.pad_from_right(128 - plainLen)  # pad from right to make 128

        # for enc1
        plaintext_bv.pad_from_left(128)  # pad from left to make 256
        plaintext_int = int(plaintext_bv)
        ciphertext = pow(plaintext_int, e, n1)  # C = M^e mod n

        ciphertext_bv = BitVector(intVal=ciphertext, size=256)

        f1.write(ciphertext_bv.get_bitvector_in_hex())  # write every block

        # for enc 2
        ciphertext = pow(plaintext_int, e, n2)  # C = M^e mod n
        ciphertext_bv = BitVector(intVal=ciphertext, size=256)
        f2.write(ciphertext_bv.get_bitvector_in_hex())  # write every block

        # for enc 3
        ciphertext = pow(plaintext_int, e, n3)  # C = M^e mod n
        ciphertext_bv = BitVector(intVal=ciphertext, size=256)
        f3.write(ciphertext_bv.get_bitvector_in_hex())  # write every block


    f1.close()
    f2.close()
    f3.close()

    message_bv.close_file_object()

def decrypt(enc1, enc2, enc3, n_1_2_3, outfile):
    #input1 = open(enc1, "r")
    #cipher1 = input1.read()     # message encrypted with 1st public key
    #input2 = open(enc2, "r")
    #cipher2 = input2.read()     # message encrypted with 2st public key
    #input3 = open(enc3, "r")
    #cipher3 = input3.read()     # message encrypted with 3st public key

    ip = open(n_1_2_3, "r")
    n1 = ip.readline()  # n values (public keys) are separated by newline
    n2 = ip.readline()
    n3 = ip.readline()

    int_n1 = int(n1)
    int_n2 = int(n2)
    int_n3 = int(n3)

    n1_bv = BitVector(intVal=int_n1)
    n2_bv = BitVector(intVal=int_n2)
    n3_bv = BitVector(intVal=int_n3)

    M = int_n1 * int_n2 * int_n3

    M1 = int(M / int_n1)
    M2 = int(M / int_n2)
    M3 = int(M / int_n3)
    M1_bv = BitVector(intVal=M1)
    M2_bv = BitVector(intVal=M2)
    M3_bv = BitVector(intVal=M3)
    M1_MI = int(M1_bv.multiplicative_inverse(n1_bv))
    M2_MI = int(M2_bv.multiplicative_inverse(n2_bv))
    M3_MI = int(M3_bv.multiplicative_inverse(n3_bv))

    c1 = M1 * M1_MI
    c2 = M2 * M2_MI
    c3 = M3 * M3_MI

    a11 = open(enc1, "r")
    a111 = a11.read()
    a22 = open(enc2, "r")
    a222 = a22.read()
    a33 = open(enc3, "r")
    a333 = a33.read()

    x = 0
    y = 256

    a1 = BitVector(hexstring=a111)   #bitvecftor from 1st ciphertext
    a2 = BitVector(hexstring=a222)   #bitvecftor from 2st ciphertext
    a3 = BitVector(hexstring=a333)   #bitvecftor from 3st ciphertext

    while (y <= a1.length()):
        a1_int = int(a1[x:y])
        a2_int = int(a2[x:y])
        a3_int = int(a3[x:y])

        A = (a1_int * c1 + a2_int * c2 + a3_int * c3) % M   #using CRT

        # print(A)
        A_cuberoot = solve_pRoot(3, A)
        M_bv = BitVector(intVal=A_cuberoot, size=128)
        M_ascii = M_bv.get_bitvector_in_ascii()
        fout = open(outfile, "w")
        fout.write(M_ascii)
        x = x + 256
        y = y + 256

    fout.close()


if __name__ == '__main__':
    if sys.argv[1] == "-e":   ##for encryption
        message = sys.argv[2]
        enc1 = sys.argv[3]
        enc2 = sys.argv[4]
        enc3 = sys.argv[5]
        outfile = sys.argv[6]
        encrypt(message, enc1, enc2, enc3, outfile)
    elif sys.argv[1] == "-c":   ##for cracking
        enc1 = sys.argv[2]
        enc2 = sys.argv[3]
        enc3 = sys.argv[4]
        n_1_2_3 = sys.argv[5]
        outfile = sys.argv[6]
        decrypt(enc1, enc2, enc3, n_1_2_3, outfile)