from math import gcd
from aux_prime_functions import *
import random

def keyGeneration():
	loop = True
	while loop:
		k=random.randrange(2**(415), 2**(416)) #416 bits
		q=generateLargePrime(160)
		p=(k*q)+1
		while not (isPrime(p)):
			k=random.randrange(2**(415), 2**(416)) #416 bits
			q=generateLargePrime(160)
			p=(k*q)+1
		L = p.bit_length()
		t = random.randint(1,p-1)
		g = squareAndMultiply(t, (p-1)//q, p)

		if(L>=512 and L<=1024 and L%64 == 0 and (gcd(p-1,q)) > 1 and squareAndMultiply(g,q,p) == 1):
			loop = False
			a = random.randint(2,q-1)
			h = squareAndMultiply(g,a,p)
			file1 = open("key.txt","w")
			file1.write(str(p))
			file1.write("\n")
			file1.write(str(q))
			file1.write("\n")
			file1.write(str(g))
			file1.write("\n")
			file1.write(str(h))
			file1.close()
			file2 = open("secretkey.txt","w")
			file2.write(str(a))
			file2.close()
            #print("Verification key stored at key.txt and secret key stored at secretkey.txt")

def shaHash(fileName):
	BLOCKSIZE = 65536
	hasher = hashlib.sha1()
	with open(fileName, 'rb') as afile:
		buf = afile.read(BLOCKSIZE)
		while len(buf) > 0:
			hasher.update(buf)
			buf = afile.read(BLOCKSIZE)
	hex = "0x"+hasher.hexdigest()
	return int(hex,0)

def sign():
	if(len(sys.argv) < 2):
		print("Format: python sign.py filename")
	elif(len(sys.argv) == 2):
		print("Signing the file...")
		fileName = sys.argv[1]
		file1 = open("key.txt","r")
		file2 = open("secretkey.txt","r")
		p=int(file1.readline().rstrip())
		q=int(file1.readline().rstrip())
		g=int(file1.readline().rstrip())
		h=int(file1.readline().rstrip())
		a=int(file2.readline().rstrip())
		loop = True
		while loop:
			r = random.randint(1,q-1)
			c1 = squareAndMultiply(g,r,p)
			c1 = c1%q
			c2 = shaHash(fileName) + (a*c1)
			Rinverse = computeInverse(r,q)
			c2 = (c2*Rinverse)%q
			if(c1 != 0 and c2 != 0):
				loop = False
		file = open("signature.txt","w")
		file.write(str(c1))
		file.write("\n")
		file.write(str(c2))
		print("cipher stored at signature.txt")
