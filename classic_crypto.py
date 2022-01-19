import math
import numpy as np
import string
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import (Qt, QFile, QDate, QTime, QSize, QTimer, QRect, QRegExp, QTranslator,
                          QLocale, QLibraryInfo, QSize)
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QGridLayout, QLabel, QDialog, QTableWidget, QMenu,
                             QTableWidgetItem, QAbstractItemView, QLineEdit, QPushButton, QTabWidget,
                             QActionGroup, QAction, QMessageBox, QFrame, QStyle, QGridLayout,
                             QVBoxLayout, QHBoxLayout, QLabel, QToolButton, QGroupBox, QStackedLayout,
                             QDateEdit, QComboBox, QPushButton, QFileDialog, QPlainTextEdit, QLineEdit,
                             QTextEdit)
from PyQt5.QtGui import (QFont, QIcon, QPalette, QBrush, QColor, QPixmap, QRegion, QClipboard,
                         QRegExpValidator, QImage, QCursor)


abc = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "I": 8, "J": 9, "K": 10,
           "L": 11, "M": 12, "N": 13, "O": 14, "P": 15, "Q": 16, "R": 17, "S": 18, "T": 19, "U": 20,
           "V": 21, "W": 22, "X": 23, "Y": 24, "Z": 25}
inv_abc = {value: key for key, value in abc.items()}


class Criptosistema:
    def __init__(self, clave):
        self.clave = clave

class CriptosistemaAfin(Criptosistema):
    def __init__(self, clave):
        super().__init__(clave)

    def encriptar(self, texto_claro):
        a, b = self.clave
        if math.gcd(int(a), 26) == 1:
            texto_cifrado = ""
            for i in texto_claro:
                i_cifrado = (int(a) * abc[i.upper()] + int(b)) % 26
                texto_cifrado += inv_abc[i_cifrado]
            return texto_cifrado
        else:
            QMessageBox.critical(None, 'Clave inválida',
                                 "Error: La clave ingresada no es válida".format(len(texto_claro)),
                                 QMessageBox.Ok)

    def desencriptar(self, texto_cifrado):
        a, b = self.clave
        if math.gcd(int(a), 26) == 1:
            texto_descifrado = ""
            for i in texto_cifrado:
                i_claro = ((pow(int(a), -1, 26)) * (abc[i.upper()] - int(b))) % 26
                texto_descifrado += inv_abc[i_claro]
            return texto_descifrado
        else:
            QMessageBox.critical(None, 'Clave inválida',
                                 "Error: La clave ingresada no es válida".format(len(texto_claro)),
                                 QMessageBox.Ok)

class CriptosistemaDesplazamiento(Criptosistema):
    def __init__(self, clave):
        super().__init__(clave)

    def encriptar(self, texto_claro):
        b = self.clave
        texto_cifrado = ""
        for i in texto_claro:
            i_cifrado = (abc[i.upper()] + int(b)) % 26
            texto_cifrado += inv_abc[i_cifrado]

        return texto_cifrado

    def desencriptar(self, texto_cifrado):
        b = self.clave
        texto_descifrado = ""
        for i in texto_cifrado:
            i_claro = (abc[i.upper()] - int(b)) % 26
            texto_descifrado += inv_abc[i_claro]
        return texto_descifrado

class CriptosistemaPermutacion(Criptosistema):
    def __init__(self, clave):
        super().__init__(clave)

    def encriptar(self, texto_claro):
        m = self.clave[0]
        values = list(map(int, self.clave[1].split()))
        comp = [i for i in range(1,len(texto_claro)+1)]
        print("Flag1")
        if (len(set(values)) < m or len(texto_claro) != len(set(values))):
            QMessageBox.critical(None, 'Error matriz',
                                 "Error: Ingresó valores repetidos o no ingreso {} valores".format(len(texto_claro)),
                                 QMessageBox.Ok)
        elif (set(comp) != set(values)):
            QMessageBox.critical(None, 'Error matriz',
                                 "No ingresó una permutación adecuada para el input",
                                 QMessageBox.Ok)
        else:
            print("Flag2")
            for a, b in zip(tuple(range(1, m + 1)), tuple(sorted(values))):
                if a != b:
                    QMessageBox.critical(None, 'Error matriz',
                                         "Error: Debe ingresar los numeros del 1 al ", m,
                                         QMessageBox.Ok)
                    break
                else:
                    mat_permutacion = np.array([range(1, m + 1), values]).reshape(2, m)
                    print("Flag3")
                    texto_separado = [texto_claro[i:i + m] for i in range(0, len(texto_claro), m)]
                    print("Flag4")
            texto_cifrado = ""
            for subtexto in texto_separado:
                print("Flag5")
                for indice in range(1, m + 1):
                    letra_cifrada = subtexto[int(mat_permutacion[1][int(np.where(mat_permutacion == indice)[1][0])]) - 1]
                    texto_cifrado += letra_cifrada
                print("Flag6")
            return texto_cifrado

    def desencriptar(self, texto_cifrado):
        m = self.clave[0]
        values = list(map(int, self.clave[1].split()))
        comp = [i for i in range(1,len(texto_cifrado)+1)]
        if (len(set(values)) < m or len(texto_cifrado) != len(set(values))):
            QMessageBox.critical(None, 'Error matriz',
                                 "Error: Ingresó valores repetidos o no ingreso {} valores".format(m),
                                 QMessageBox.Ok)
        elif (set(comp) != set(values)):
            QMessageBox.critical(None, 'Error matriz',
                                 "No ingresó una permutación adecuada para el input",
                                 QMessageBox.Ok)
        else:
            for a, b in zip(tuple(range(1, m + 1)), tuple(sorted(values))):
                if a != b:
                    QMessageBox.critical(None, 'Error matriz',
                                         "Error: Debe ingresar los numeros del 1 al ", m,
                                         QMessageBox.Ok)
                    break
                else:
                    mat_inv_permutacion = np.array([range(1, m + 1), [x[0] for x in
                                                          sorted(list(zip(tuple(range(1, m + 1)), tuple(values))),
                                                                 key=lambda x: x[1])]]).reshape(2, m)
                    texto_separado = [texto_cifrado[i:i + m] for i in range(0, len(texto_cifrado), m)]

            texto_descifrado = ""
            for subtexto in texto_separado:
                for indice in range(1, m + 1):
                    letra_descifrada = subtexto[
                        int(mat_inv_permutacion[1][int(np.where(mat_inv_permutacion == indice)[1][0])]) - 1]
                    texto_descifrado += letra_descifrada

            return texto_descifrado
