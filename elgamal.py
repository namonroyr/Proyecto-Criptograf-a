import random
import math as mth
import numpy as np
from aux_prime_functions import *

def gen_key(prime):
    a = random.randint(2, prime-1)
    return a

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
		for i in range(len(byte_array) ):
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
				y1 = modexp(alpha, k, prime)
				#d = ih^y mod p
				y2 = (i*modexp(beta, k, prime)) % prime
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
				x = modexp(y1, a, prime)
				#plaintext integer = ds^-1 mod p
				plain = (y2*modexp(x, prime-2, prime)) % prime
				#add plain to list of plaintext integers
				plaintext.append( plain )
		decryptedText = decode(plaintext, 256)
		decryptedText = "".join([ch for ch in decryptedText if ch != '\x00'])
		return decryptedText
