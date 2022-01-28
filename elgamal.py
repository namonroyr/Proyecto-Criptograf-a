import random as rd
import math as mth
import numpy as np

with open('primes.txt') as f:
	lines = f.readlines()
primes = list()
for line in lines:
	primes += list(map(int, line.strip().split(' ')))

def gen_prime():
    return np.random.choice(primes, size=1)[0]


def gen_key(q):
    key = rd.randint(2, q)
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
 
    k = mod_pow(q)
    s = mod_pow(h, k, q)
    p = mod_pow(g, k, q)
     
    for i in range(0, len(msg)):
        en_msg.append(msg[i])

    for i in range(0, len(en_msg)):
        en_msg[i] = s * ord(en_msg[i])
 
    return en_msg, p
 
def decrypt(en_msg, p, key, q):
 
    dr_msg = []
    h = mod_pow(p, key, q)
    for i in range(0, len(en_msg)):
        dr_msg.append(chr(int(en_msg[i]/h)))
         
    return dr_msg