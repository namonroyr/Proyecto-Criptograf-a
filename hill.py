import math
import imageio
import os.path
import numpy as np
import sympy

abc = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "I": 8, "J": 9, "K": 10,
       "L": 11, "M": 12, "N": 13, "O": 14, "P": 15, "Q": 16, "R": 17, "S": 18, "T": 19, "U": 20,
       "V": 21, "W": 22, "X": 23, "Y": 24, "Z": 25}
inv_abc = {value: key for key, value in abc.items()}


class Hill:
    def __init__(self, img, file_name, key=None):
        #Make image to have square dimensions
        self.new_height = self.h = img.shape[0]
        self.new_width = self.w = img.shape[1]
        self.n = 10
        n = self.n
        if self.h%n:
            self.new_height = (int((self.h-1)/n) + 1) * n
        if self.w%n:
            self.new_width = (int((self.w-1)/n) + 1) * n
        img_squared = np.zeros((self.new_height,self.new_width,3))
        img_squared[:self.h,:self.w,:] += img
        self.data = img_squared
        #Key creation
        self.Mod = 256
        Mod = self.Mod
        k = 23
        d = np.random.randint(256, size = (int(n/2),int(n/2)))
        I = np.identity(int(n/2))
        a = np.mod(-d, Mod)
        b = np.mod((k * np.mod(I - a,Mod)), Mod)
        k = np.mod(np.power(k,127), Mod)
        c = np.mod((I + a), Mod)
        c = np.mod(c * k, Mod)

        A1 = np.concatenate((a,b), axis = 1)
        A2 = np.concatenate((c,d), axis = 1)
        A = np.concatenate((A1,A2), axis = 0)
        self._key = A
        #Test = np.mod(np.matmul(np.mod(A,Mod),np.mod(A,Mod)),Mod)
        #print(Test)
        # Saving key as an image
        img_key = np.zeros((n + 1, n))
        img_key[:n, :n] += A
        img_key[-1][0] = int(self.h/Mod)
        img_key[-1][1] = self.h % Mod
        img_key[-1][2] = int(self.w/Mod)
        img_key[-1][3] = self.w % Mod
        img_ui8 = img_key.astype(np.uint8)
        imageio.imwrite(file_name+"_key.png", img_ui8)

    @property
    def key(self):
        return self._key

    def encriptar(self, file_name):
        Encrypted = np.zeros((self.new_height,self.new_width,3))
        n = self.n
        Mod = self.Mod
        for j in range(int(self.new_width/self.n)):
            for i in range(int(self.new_height/self.n)):
                Enc1 = (np.matmul(self._key % Mod,self.data[i * n:(i + 1) * n, j * n:(j + 1) * n,0] % Mod)) % Mod
                Enc1 = np.matmul(self._key % Mod, np.transpose(Enc1)) % Mod
                Enc2 = (np.matmul(self._key % Mod,self.data[i * n:(i + 1) * n, j * n:(j + 1) * n,1] % Mod)) % Mod
                Enc2 = np.matmul(self._key % Mod, np.transpose(Enc2)) % Mod
                Enc3 = (np.matmul(self._key % Mod,self.data[i * n:(i + 1) * n, j * n:(j + 1) * n,2] % Mod)) % Mod
                Enc3 = np.matmul(self._key % Mod, np.transpose(Enc3)) % Mod
                Enc1 = np.resize(Enc1,(Enc1.shape[0],Enc1.shape[1],1))
                Enc2 = np.resize(Enc2,(Enc2.shape[0],Enc2.shape[1],1))
                Enc3 = np.resize(Enc3,(Enc3.shape[0],Enc3.shape[1],1))
                Encrypted[i * n:(i + 1) * n, j * n:(j + 1) * n] += np.concatenate((Enc1,Enc2,Enc3), axis = 2)
        imageio.imwrite(file_name+'_cifrado.png', Encrypted)
        return file_name+'_cifrado.png'

def desencriptar(Enc, key):
    nl = int(Enc.shape[0])
    nw = int(Enc.shape[1])
    Mod = 256
    A = imageio.imread(key)
    n = int(A.shape[0] - 1)
    l = int(A[-1][0] * Mod + A[-1][1])
    w = int(A[-1][2] * Mod + A[-1][3])
    A = A[0:-1]
    Decrypted = np.zeros((nl,nw,3))
    for j in range(int(nw/n)):
        for i in range(int(nl/n)):
            Dec1 = (np.matmul(A % Mod,Enc[i * n:(i + 1) * n, j * n:(j + 1) * n,0] % Mod)) % Mod
            Dec1 = np.matmul(A % Mod, np.transpose(Dec1)) % Mod
            Dec2 = (np.matmul(A % Mod,Enc[i * n:(i + 1) * n, j * n:(j + 1) * n,1] % Mod)) % Mod
            Dec2 = np.matmul(A % Mod, np.transpose(Dec2)) % Mod
            Dec3 = (np.matmul(A % Mod,Enc[i * n:(i + 1) * n, j * n:(j + 1) * n,2] % Mod)) % Mod
            Dec3 = np.matmul(A % Mod, np.transpose(Dec3)) % Mod
            Dec1 = np.resize(Dec1,(Dec1.shape[0],Dec1.shape[1],1))
            Dec2 = np.resize(Dec2,(Dec2.shape[0],Dec2.shape[1],1))
            Dec3 = np.resize(Dec3,(Dec3.shape[0],Dec3.shape[1],1))
            Dec = np.concatenate((Dec1,Dec2,Dec3), axis = 2)
            Decrypted[i * n:(i + 1) * n, j * n:(j + 1) * n] += Dec
    Final = Decrypted[:l,:w,:]
    return Final

def attack(p_text, c_text):
    m = 2
    key = 0
    verification = False
    while not verification:
        if (len(p_text) < pow(m,2)):
            break
        d = pow(m,2)
        n = np.random.randint(0, len(p_text)-d)
        d = pow(m,2)
        print(d)
        plain = np.array(p_text[n:n+d])
        cipher = np.array(c_text[n:n+d])
        p = plain.reshape(m,m)
        print(p)
        c = cipher.reshape(m,m)
        p_sympy = sympy.Matrix(p)
        adj_p = p_sympy.adjugate() % 26
        print(adj_p)
        det_p = round(np.linalg.det(p))%26
        print(np.linalg.det(p))
        print(round(np.linalg.det(p)))
        print(det_p)
        print(math.gcd(det_p,26))
        if det_p == 0 or math.gcd(det_p,26) != 1:
            continue
        inv_det = modInverse(det_p, 26)
        print(inv_det)
        inv_p = (inv_det*adj_p)%26
        print(inv_p)
        key = (np.matmul(inv_p % 26, c % 26)) % 26
        print('**********KEY*********')
        print(key)
        new_cal = (np.matmul(p % 26, key % 26)) % 26
        v = new_cal == p
        if v.all():
            verification = True
        else:
            m += 1
    return m, key

def modInverse(a, m):
    """
    Función que utiliza el algoritmo de Euclides para encontrar el inverso mod m de un número a
    """
    m0 = m
    y = 0
    x = 1
    if (m == 1):
        return 0
    while (a > 1):
        # q is quotient
        q = a // m
        t = m
        m = a % m
        a = t
        t = y
        # Update x and y
        y = x - q * y
        x = t
    # Make x positive
    if (x < 0):
        x = x + m0
    return x

p = "GONAVYBEATARMYA"
c = "OAXELQLSMTKTCOQ"
texto_cifrado = []
texto_plano = []
for i in c:
    i_cifrado = abc[i.upper()] % 26
    texto_cifrado.append(i_cifrado)

for i in p:
    i_plano = abc[i.upper()] % 26
    texto_plano.append(i_plano)

print(texto_plano)
print(texto_cifrado)

print(attack(texto_plano, texto_cifrado))
