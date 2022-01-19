import numpy as np
import cv2
import sdes_new
import math

def encrypt_image(img_matrix):
    c=0
    for i in range(0,len(img_matrix)):
        for j in range(0,len(img_matrix[i])):
            for k in range(len(img_matrix[i][j])):
                c=c+1
                original_bin=binary(img_matrix[i][j][k])
                encrypted_bin=sdes_new.encrypt(original_bin)
                img_matrix[i][j][k]=decimal(encrypted_bin)
    return img_matrix

def decrypt_image(img_matrix):
    c=0
    for i in range(0,len(img_matrix)):
        for j in range(0,len(img_matrix[i])):
            for k in range(len(img_matrix[i][j])):
                c=c+1
                original_bin=binary(img_matrix[i][j][k])
                decrypted_bin=sdes_new.decrypt(original_bin)
                img_matrix[i][j][k]=decimal(decrypted_bin)
    return img_matrix

def decimal(binary):
	num=0
	pos=7
	for val in binary:
		num=num+int(val)*math.pow(2,pos)
		pos=pos-1
	return int(num)

def binary(number):
	s=''
	bin_val=''
	while(number>0):
		s=s+str(number%2)
		number=number//2
	#print(s)
	if(len(s)<8):
		s=s+"0"*(8-len(s))
	#print(s)
	for val in s[len(s)-1::-1]:
		bin_val+=val
	return bin_val
