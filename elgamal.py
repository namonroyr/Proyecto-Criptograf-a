import random as rd
import math as mth

def gen_key(q):
    key = rd.randint(mth.pow(10, 20), q)
    while mth.gcd(q,key) != 1:
        key = rd.randint(mth.pow(10, 20), q)
    return key

def mod_pow(a, b, c):
    x, y = 1, a
    while b > 0:
        if b % 2 != 0:
            x = (x * y) % c
        y = (y * y) % c
        b = int(b / 2)
    return x % c

def encrypt(msg, q, h, g):
 
    en_msg = []
 
    k = mod_pow(q)# Private key for sender
    s = mod_pow(h, k, q)
    p = mod_pow(g, k, q)
     
    for i in range(0, len(msg)):
        en_msg.append(msg[i])
 
    print("g^k used : ", p)
    print("g^ak used : ", s)
    for i in range(0, len(en_msg)):
        en_msg[i] = s * ord(en_msg[i])
 
    return en_msg, p
 
def decrypt(en_msg, p, key, q):
 
    dr_msg = []
    h = mod_pow(p, key, q)
    for i in range(0, len(en_msg)):
        dr_msg.append(chr(int(en_msg[i]/h)))
         
    return dr_msg
