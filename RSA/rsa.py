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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return(a)
    # print("GCD: %d\n" % a)

e = 65537

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
    totient_n = (p - 1) * (q - 1)
    totient_n_bv = BitVector(intVal=totient_n)

    e_bv = BitVector(intVal=e)
    d_bv = e_bv.multiplicative_inverse(totient_n_bv)        # d = MI of e mod n
    d = int(d_bv)

    print(n, p, q)
    print(d)



def encrypt(message, pfile,qfile, out):
    ip = open(pfile, "r")
    p_str = ip.read()
    iq = open(qfile, "r")
    q_str = iq.read()
    p = int(p_str)      # need to convert to int, since read in as string
    q = int(q_str)
    n = p * q

    f = open(out, "w")
    message_bv = BitVector(filename=message)
    while (message_bv.more_to_read):    # read in blocks of  128


        plaintext_bv = message_bv.read_bits_from_file(128)
        plainLen = plaintext_bv.length()

        if (plainLen < 128):
            plaintext_bv.pad_from_right(128 - plainLen)     # pad from right to make 128

        plaintext_bv.pad_from_left(128)                     # pad from left to make 256

        plaintext_int = int(plaintext_bv)
        ciphertext = pow(plaintext_int, e, n)                     # C = M^e mod n

        ciphertext_bv = BitVector(intVal=ciphertext, size=256)

        f.write(ciphertext_bv.get_bitvector_in_hex())   # write every block

    f.close()

    message_bv.close_file_object()


def decrypt(encrypted, pfile, qfile, out):
    ip = open(pfile, "r")
    p_str = ip.read()
    iq = open(qfile, "r")
    q_str = iq.read()
    p = int(p_str)  # need to convert to int, since read in as string
    q = int(q_str)
    n = p * q

    totient_n = (p - 1) * (q - 1)
    totient_n_bv = BitVector(intVal=totient_n)

    p_bv = BitVector(intVal=p)
    q_bv = BitVector(intVal=q)

    MI_p = p_bv.multiplicative_inverse(q_bv)    #MI of p mod q
    MI_q = q_bv.multiplicative_inverse(p_bv)    # MI of q mod p
    MI_p_int = int(MI_p)
    MI_q_int = int(MI_q)

    e_bv = BitVector(intVal=e)
    d_bv = e_bv.multiplicative_inverse(totient_n_bv)  # d = MI of e mod n
    d = int(d_bv)

    f = open(out, "w")
    encrypt = open(encrypted, "r")
    enc = encrypt.read()

    encrypted_bv = BitVector(hexstring=enc)
    x =0
    y = 256
    while (y <= encrypted_bv.length()):

    # while (encrypted_bv.):  # read in blocks of  128
        ciphertext_bv = encrypted_bv[x:y]
        ciphertext_int = int(ciphertext_bv)
        Vp = pow(ciphertext_int, d, p)
        Vq = pow(ciphertext_int, d, q)

        Xp = q * MI_q_int
        Xq = p * MI_p_int

        plaintext = (Vp * Xp + Vq * Xq) % n     # by CRT
        plaintext_bv = BitVector(intVal=plaintext, size=256)
        plaintext_bv = plaintext_bv[128:256]

        print(plaintext_bv.length())
        f.write(plaintext_bv.get_bitvector_in_ascii())  # write every block

        x = x +256
        y=y+256

    f.close()


if __name__ == '__main__':
    if sys.argv[1] == "-g":     ##for key gen
        key_gen()
    elif sys.argv[1] == "-e":   ##for encryption
        message = sys.argv[2]
        pfile = sys.argv[3]
        qfile = sys.argv[4]
        out = sys.argv[5]
        encrypt(message, pfile, qfile, out)
    elif sys.argv[1] == "-d":   ##for decryption
        encrypted = sys.argv[2]
        pfile = sys.argv[3]
        qfile = sys.argv[4]
        out = sys.argv[5]
        decrypt(encrypted, pfile, qfile, out)




