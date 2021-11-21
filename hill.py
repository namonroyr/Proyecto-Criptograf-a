import math as mth
import functools as ft
import cv2
import string
import os.path
import pickle
import numpy as np
from egcd import egcd
from numpy.linalg import inv, det


class Hill:
    def __init__(self, img, key=None):
        self.data = img
        print("Hilll0")
        # Computet the chunk
        self.chunk = self.compute_chunk()
        print("Hilll--")
        if key != None:
            # Load the key if she exist in the current dir
            self._key = key
        else:
            # Generate a random key
            self._key = np.random.random_integers(0, 256, (self.chunk, self.chunk))

            # If det is equal to zero regenrate another key
            det_k = det(self._key)
            if (det_k == 0 or egcd(det_k, 256) != 1):
                self._key = np.random.random_integers(0, 256, (self.chunk, self.chunk))

        print(self._key.dtype)
        print(self._key.shape)
        print(self._key)

        # Inverse of the key
        self.reversed_key = np.matrix(self._key).I.A

        print(self.reversed_key.dtype)
        print(self.reversed_key.shape)
        print(self.reversed_key)

    def compute_chunk(self):
        print("hemllo")
        max_chunk = 23
        data_shape = self.data.shape[1]
        print(data_shape)

        for i in range(max_chunk, 0, -1):
            if data_shape % i == 0:
                return i

    def createMatrix(self, matrix, m):
        """
        Crea una matriz numpy a partir del input
        """
        np_matrix = np.matrix(np.array(matrix).reshape(m, m))
        return np_matrix

    def matrixInv(matriz, mod):
        """
        Función para encontrar la matriz módulo inversa
        """
        det = int(np.round(np.linalg.det(matriz)))
        det_inv = egcd(det, mod)[1] % mod
        matriz_inv = det_inv * np.round(det*np.linalg.inv(matriz)).astype(int)%mod
        return matriz_inv

    @property
    def key(self):
        return self._key

    def encriptar(self, data):
        cript = []
        chunk = self.chunk
        key = self._key

        for i in range(0, len(data), chunk):
            temp = list(np.dot(key, data[i:i + chunk]) % 256)
            cript.append(temp)
        cript = (np.array(cript)).reshape((1, len(data)))
        return cript[0]

    def decode(self, data):
        """ Decode function """
        uncrypted = []
        chunk = self.chunk
        reversed_key = self.reversed_key

        for i in range(0, len(data), chunk):
            temp = list(np.dot(reversed_key, data[i:i + chunk]))
            uncrypted.append(temp)

        uncrypted = (np.array(uncrypted)).reshape((1, len(data)))

        return uncrypted[0]
