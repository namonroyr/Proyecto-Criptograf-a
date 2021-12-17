import DES
key = [1, 0, 1, 0, 0, 0, 0, 0, 1, 0]
P10 = [2,4,1,6,3,9,0,8,7,5]
P8 = [5,2,6,3,7,4,9,8]
IP = [2, 6, 3, 1, 4, 8, 5, 7 ]
EP = [ 4, 1, 2, 3, 2, 3, 4, 1 ]
P4 = [ 2, 4, 3, 1 ]
IP_inv = [ 4, 1, 3, 5, 7, 2, 8, 6 ]

def key_generation():
    key_prime = [key[P10[i]] for i in range(10)]
    Ls = key_prime[:5]
    Rs = key_prime[5:]
    Ls_1 = Ls[1:]+Ls[:1]
    Rs_1 = Rs[1:]+Rs[:1]
    key_prime = Ls_1 + Rs_1
    key1 = [key_prime[P8[i]] for i in range(8)]
    Ls_2 = Ls[2:]+Ls[:2]
    Rs_2 = Rs[2:]+Rs[:2]
    key_prime = Ls_2 + Rs_2
    key2 = [key_prime[P8[i]] for i in range(8)]
    return key1, key2


def Function(arr,key):
    l = arr[:4]
    r = arr[4:]



def encriptar(x):
    arr = [x[IP[i]] for i in range(8)]
    pass



