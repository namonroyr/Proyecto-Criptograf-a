import random
import math as mth
import numpy as np

#find n bit prime
def find_prime(iNumBits=256, iConfidence=32):
		#keep testing until one is found
		while(1):
				#generate potential prime randomly
				p = random.randint( 2**(iNumBits-2), 2**(iNumBits-1) )
				#make sure it is odd
				while( p % 2 == 0 ):
						p = random.randint(2**(iNumBits-2),2**(iNumBits-1))

				#keep doing this if the solovay-strassen test fails
				while( not is_prime(p, iConfidence) ):
						p = random.randint( 2**(iNumBits-2), 2**(iNumBits-1) )
						while( p % 2 == 0 ):
								p = random.randint(2**(iNumBits-2), 2**(iNumBits-1))

				#if p is prime compute p = 2*p + 1
				#if p is prime, we have succeeded; else, start over
				p = p * 2 + 1
				if is_prime(p, iConfidence):
						return p

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
		if not (power( g, (p-1)//p1, p ) == 1):
			if not power( g, (p-1)//p2, p ) == 1:
				return g

'''
Tests to see if a number is prime with Fermat's Theorem
'''

# Iterative Function to calculate
# (a^n)%p in O(logy)
def power(a, n, p):
    # Initialize result
    res = 1
    # Update 'a' if 'a' >= p
    a = a % p
    while n > 0:
        # If n is odd, multiply 'a' with result
        if n % 2:
            res = (res * a) % p
            n = n - 1
        else:
            a = (a ** 2) % p
            # n must be even now
            n = n // 2
    return res % p

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
            if power(a, n - 1, n) != 1:
                return False

    return True

def gen_key(prime):
    a = random.randint(2, prime-1)
    return a

def mod_pow(a, b, c):
    x, y = 1, a
    while b > 0:
        if b % 2 != 0:
            x = (x * y) % c
        y = (y * y) % c
        b = int(b / 2)
    return x % c

def encode(sPlaintext, iNumBits):
		byte_array = bytearray(sPlaintext, 'utf-16')
		#z is the array of integers mod p
		z = []
		k = iNumBits//8
		#j marks the jth encoded integer
		j = -1 * k
		#num is the summation of the message bytes
		num = 0
		#i iterates through byte array
		for i in range( len(byte_array) ):
				#if i is divisible by k, start a new encoded integer
				if i % k == 0:
						j += k
						num = 0
						z.append(0)
				#add the byte multiplied by 2 raised to a multiple of 8
				z[j//k] += byte_array[i]*(2**(8*(i%k)))
		return z

#decodes integers to the original message bytes
def decode(aiPlaintext, iNumBits):
		#bytes array will hold the decoded original message bytes
		bytes_array = []
		k = iNumBits//8
		#num is an integer in list aiPlaintext
		for num in aiPlaintext:
				#get the k message bytes from the integer, i counts from 0 to k-1
				for i in range(k):
						#temporary integer
						temp = num
						#j goes from i+1 to k-1
						for j in range(i+1, k):
								#get remainder from dividing integer by 2^(8*j)
								temp = temp % (2**(8*j))
						#message byte representing a letter is equal to temp divided by 2^(8*i)
						letter = temp // (2**(8*i))
						#add the message byte letter to the byte array
						bytes_array.append(letter)
						num = num - (letter*(2**(8*i)))
		decodedText = bytearray(b for b in bytes_array).decode('utf-16')
		return decodedText

def encrypt(prime, alpha, beta, sPlaintext):
		z = encode(sPlaintext, 256)
		#cipher_pairs list will hold pairs (c, d) corresponding to each integer in z
		cipher_pairs = []
		#i is an integer in z
		for i in z:
				#pick random k from (0, prime-1) inclusive
				k = random.randint( 0, prime)
				y1 = power(alpha, k, prime)
				#d = ih^y mod p
				y2 = (i*power( beta, k, prime)) % prime
				#add the pair to the cipher pairs list
				cipher_pairs.append( [y1, y2] )
		encryptedStr = ""
		for pair in cipher_pairs:
				encryptedStr += str(pair[0]) + ' ' + str(pair[1]) + ' '
		return encryptedStr

def decrypt(prime, a, cipher):
		#decrpyts each pair and adds the decrypted integer to list of plaintext integers
		plaintext = []
		cipherArray = cipher.split()
		if (not len(cipherArray) % 2 == 0):
				return "Malformed Cipher Text"
		for i in range(0, len(cipherArray), 2):
				y1 = int(cipherArray[i])
				y2 = int(cipherArray[i+1])
				#s = c^x mod p
				x = power(y1, a, prime)
				#plaintext integer = ds^-1 mod p
				plain = (y2*power(x, prime-2, prime)) % prime
				#add plain to list of plaintext integers
				plaintext.append( plain )
		decryptedText = decode(plaintext, 256)
		decryptedText = "".join([ch for ch in decryptedText if ch != '\x00'])
		return decryptedText
