import random
import math as mth
import numpy as np


def modexp( base, exp, modulus ):
        return pow(base, exp, modulus)

'''
Tests to see if a number is prime with Fermat's Theorem
'''
# If n is prime, then always returns true,
# If n is composite than returns false with
# high probability Higher value of k increases
# probability of correct result
def is_prime(n, k):
    # Corner cases
    if n == 1 or n == 4:
        return False
    elif n == 2 or n == 3:
        return True
    # Try k times
    else:
        for i in range(k):
            # Pick a random numberin [2..n-2]
            # Above corner cases makesure that n > 4
            a = random.randint(2, n - 2)
            # Fermat's little theorem
            if modexp(a, n - 1, n) != 1:
                return False
    return True

"""Function to find n bit prime"""
def find_prime(iNumBits=256, iConfidence=32):
		#keep testing until one is found
		while(1):
				#generate potential prime randomly
				p = random.randint( 2**(iNumBits-2), 2**(iNumBits-1) )
				#make sure it is odd
				while( p % 2 == 0 ):
						p = random.randint(2**(iNumBits-2),2**(iNumBits-1))

				#keep doing this if the prime test fails
				while(not is_prime(p, iConfidence) ):
						p = random.randint( 2**(iNumBits-2), 2**(iNumBits-1) )
						while( p % 2 == 0 ):
								p = random.randint(2**(iNumBits-2), 2**(iNumBits-1))
				#if p is prime compute p = 2*p + 1
				#if p is prime, we have succeeded; else, start over
				p = p * 2 + 1
				if is_prime(p, iConfidence):
					return p

def squareAndMultiply(x,c,n):
	z=1
	#getting value of l by converting c into binary representation and getting its length
	c="{0:b}".format(c)[::-1] #reversing the binary string

	l=len(c)
	for i in range(l-1,-1,-1):
		z=pow(z,2)
		z=z%n
		if(c[i] == '1'):
			z=(z*x)%n
	return z

#finds a primitive root for prime p
#this function was implemented from the algorithm described here:
#http://modular.math.washington.edu/edu/2007/spring/ent/ent-html/node31.html
def find_primitive_root(p):
	if p == 2:
		return 1
	#the prime divisors of p-1 are 2 and (p-1)/2 because
	#p = 2x + 1 where x is a prime
	p1 = 2
	p2 = (p-1) // p1
	#test random g's until one is found that is a primitive root mod p
	while(1):
		g = random.randint( 2, p-1 )
		#g is a primitive root if for all prime factors of p-1, p[i]
		#g^((p-1)/p[i]) (mod p) is not congruent to 1
		if not (modexp( g, (p-1)//p1, p ) == 1):
			if not modexp( g, (p-1)//p2, p ) == 1:
				return g

'''
Euclid's extended algorithm for finding the multiplicative inverse of two numbers
'''
def multiplicative_inverse(e, phi):
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_phi = phi

    while e > 0:
        temp1 = temp_phi//e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2

        x = x2 - temp1 * x1
        y = d - temp1 * y1

        x2 = x1
        x1 = x
        d = y1
        y1 = y

    if temp_phi == 1:
        return d + phi
