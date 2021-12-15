import DES
key = [1, 0, 1, 0, 0, 0, 0, 0, 1, 0]
P10 = [2,4,1,6,3,9,0,8,7,5]
P8 = [5,2,6,3,7,4,9,8]

def key_generation():
    key_prime = [key[P10[i]] for i in range(10)]
    Ls = key_prime[0:5]
    Rs = key_prime[5:10]
    Ls_1 = Ls[1:]+Ls[:1]
    Rs_1 = Rs[1:]+Rs[:1]
    key_prime = Ls_1 + Rs_1
    key1 = [key_prime[P8[i]] for i in range(8)]
    Ls_2 = Ls_1[1:]+Ls_1[:1]
    Rs_2 = Rs_1[1:]+Rs_1[:1]
    key_prime = Ls_2 + Rs_2
    print("Esto es Ls2: {} y esto es Rs2: {}".format(Ls_2,Rs_2))
    key2 = [key_prime[P8[i]] for i in range(8)]
    return key1, key2
print(key_generation())