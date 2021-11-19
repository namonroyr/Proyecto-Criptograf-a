import sys
import math
import numpy as np
from egcd import egcd
from PyQt5.QtWidgets import QApplication, QGridLayout, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QPlainTextEdit, QMainWindow, QLineEdit, QComboBox
from PyQt5.QtCore import (Qt, QFile, QDate, QTime, QSize, QTimer, QRect, QRegExp, QTranslator,
                          QLocale, QLibraryInfo)
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor
import vigenere as vg
abc = {"A" : 0, "B" : 1, "C" : 2, "D" : 3, "E" : 4, "F" : 5, "G" : 6, "H" : 7, "I" : 8, "J" : 9, "K" : 10,
        "L" : 11, "M" : 12, "N" : 13, "O" : 14, "P" : 15, "Q" : 16, "R" : 17, "S" : 18, "T" : 19, "U" : 20,
        "V" : 21, "W" : 22, "X" : 23, "Y" : 24, "Z" : 25}
inv_abc = {value:key for key, value in abc.items()}

class Criptosistema:
    def __init__(self, clave):
        self.clave = clave


class CriptosistemaDesplazamiento(Criptosistema):
    def __init__(self, clave):
        super().__init__(clave)

    def encriptar(self, input, output):
        b = self.clave
        texto_claro = input.toPlainText()

        texto_cifrado = ""
        for i in texto_claro:
            i_cifrado = ( abc[i.upper()] + int(b) )%26
            texto_cifrado += inv_abc[ i_cifrado ]

        output.setPlainText(texto_cifrado)

    def desencriptar(self, input, output):
        b = self.clave
        texto_cifrado = input.toPlainText()

        texto_descifrado = ""
        for i in texto_cifrado:
            i_claro = ( abc[i.upper()] - int(b) )%26
            texto_descifrado += inv_abc[i_claro]

        output.setPlainText(texto_descifrado)

class CriptosistemaAfin(Criptosistema):
    def __init__(self, clave):
        super().__init__(clave)

    def encriptar(self, input, output):
        a, b = self.clave
        if math.gcd(int(a), 26) == 1:
            texto_claro = input.toPlainText().strip()

            texto_cifrado = ""
            for i in texto_claro:
                i_cifrado = (int(a)*abc[i.upper()] + int(b))%26
                texto_cifrado += inv_abc[ i_cifrado ]

            output.setPlainText(texto_cifrado)

        else:
            input.setPlainText("La clave ingresada no es válida")

    def desencriptar(self, input, output):
        a, b = self.clave
        if math.gcd(int(a), 26) == 1:
            texto_cifrado = input.toPlainText().strip()

            texto_descifrado = ""
            for i in texto_cifrado:
                i_claro = (( pow(int(a), -1, 26) )*( abc[i.upper()] - int(b) ))%26
                texto_descifrado += inv_abc[i_claro]

            output.setPlainText(texto_descifrado)
        else:
            input.setPlainText("La clave ingresada no es válida")

class CriptosistemaPermutacion(Criptosistema):
    def __init__(self, clave):
        super().__init__(clave)

    def encriptar(self, input, output):
        m = self.clave[0]
        values =  list(map(int, self.clave[1].split()))
        
        if (len(set(values)) < m):
            limpiarCampos()
            input.setPlainText("Error: Ingresó valores repetidos o no ingreso {} valores".format(m))

        for a, b in zip(tuple(range(1, m+1)), tuple(sorted(values))):
            if a != b:
                limpiarCampos()
                input.setPlainText("Error: Debe ingresar los numeros del 1 al", m)
                break

        mat_permutacion = np.array([range(1, m+1), values]).reshape(2, m)
        texto_claro = input.toPlainText().strip()
        texto_separado = [texto_claro[i:i+m] for i in range(0, len(texto_claro), m)]

        texto_cifrado = ""
        for subtexto in texto_separado:
            for indice in range(1, m+1):
                letra_cifrada = subtexto[ int(mat_permutacion[1][ int(np.where(mat_permutacion == indice)[1][0]) ]) - 1 ]
                texto_cifrado += letra_cifrada
                
        output.setPlainText(texto_cifrado)

    def desencriptar(self, input, output):
        m = self.clave[0]
        values =  list(map(int, self.clave[1].split()))
        
        if (len(set(values)) < m):
            limpiarCampos()
            input.setPlainText("Error: Ingresó valores repetidos o no ingreso {} valores".format(m))

        for a, b in zip(tuple(range(1, m+1)), tuple(sorted(values))):
            if a != b:
                limpiarCampos()
                input.setPlainText("Error: Debe ingresar los numeros del 1 al", m)
                break

        mat_inv_permutacion = np.array( [ range(1, m+1), [x[0] for x in sorted( list(zip(tuple(range(1, m+1)), tuple(values))), key = lambda x: x[1] )] ] ).reshape(2, m)
        texto_cifrado = input.toPlainText().strip()
        texto_separado = [texto_cifrado[i:i+m] for i in range(0, len(texto_cifrado), m)]

        texto_descifrado = ""
        for subtexto in texto_separado:
            for indice in range(1, m+1):
                letra_descifrada = subtexto[ int(mat_inv_permutacion[1][ int(np.where(mat_inv_permutacion == indice)[1][0]) ]) - 1 ]
                texto_descifrado += letra_descifrada
            
        output.setPlainText(texto_descifrado)

class CriptosistemaHill(Criptosistema):
    def __init__(self, clave, m):
        super().__init__(clave)
        self.m = int(m)

    def createMatrix(self, matrix, m):
        """
        Crea una matriz numpy a partir del input
        """
        entradas = list(map(int, matrix.split()))
        np_matrix = np.matrix(np.array(entradas).reshape(m, m))
        return np_matrix

    def matrixInv(matriz, mod):
        """
        Función para encontrar la matriz módulo inversa
        """
        det = int(np.round(np.linalg.det(matriz)))
        det_inv = egcd(det, mod)[1] % mod
        matriz_inv = det_inv * np.round(det*np.linalg.inv(matriz)).astype(int)%mod
        return matriz_inv

    def encriptar(self, input, output):
        K = self.createMatrix(self.clave, self.m)
        det_K = int(np.round(np.linalg.det(K)))
        #Se verifica si la clave es válida
        if (det_K != 0 and math.gcd(det_K, 26) == 1):
            texto_claro = input.toPlainText().strip()
            texto_cifrado = ''
            texto_num = []
            m = self.m
            for letter in texto_claro:
                texto_num.append(abc[letter.upper()])
            #Se divide el texto en secciones de tamaño m
            div_m = [texto_num[i:i+int(m)] for i in range (0, len(texto_num), int(m))]
            #Se encripta cada sección de tamaño m con la matriz Clave
            for s in div_m:
                while len(s) != K.shape[0]:
                    s.append(abc["B"])
                num = np.dot(s, K) % 26
                n = num.shape[1]
                for i in range(n):
                    numero = int(num[0, i])
                    texto_cifrado += inv_abc[numero]
            output.setPlainText(texto_cifrado)
        else:
            input.setPlainText("La clave ingresada no es válida")

    #def desencriptar(self, input, output):

def botonAfin(clave, input, output, encriptar):
    criptosistema_afin = CriptosistemaAfin(clave)
    if encriptar == True:
        criptosistema_afin.encriptar(input, output)
    elif encriptar == False:
        criptosistema_afin.desencriptar(input, output)

def botonDesplazamiento(clave, input, output, encriptar):
    criptosistema_desplazamiento = CriptosistemaDesplazamiento(clave)
    if encriptar == True:
        criptosistema_desplazamiento.encriptar(input, output)
    elif encriptar == False:
        criptosistema_desplazamiento.desencriptar(input, output)

def botonPermutacion(clave, input, output, encriptar):
    criptosistema_permutacion = CriptosistemaPermutacion(clave)
    if encriptar == True:
        criptosistema_permutacion.encriptar(input, output)
    elif encriptar == False:
        criptosistema_permutacion.desencriptar(input, output)

def botonHill(clave, m, input, output, encriptar):
    criptosistema_Hill = CriptosistemaHill(clave, m)
    if encriptar == True:
        criptosistema_Hill.encriptar(input, output)
    elif encriptar == False:
        criptosistema_Hill.desencriptar(input, output)

def crearBoton(cifrado):
    if cifrado:
        boton = QPushButton(text = "Cifrar texto")
    else:
        boton = QPushButton(text = "Descifrar texto")
    boton.setStyleSheet(
        """
        QPushButton {
            border:1px solid #161616;
            border-radius:5%;
            padding:5px;
        }
        QPushButton:hover {
            background-color:#E3E3E3;
        }
        """
    )
    boton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    boton.setFixedWidth(150)
    return boton

def limpiarCampos():
    res_clave.setText("")
    for i in [input_aCifrar, input_aDescifrar, output_cifrado, output_descifrado]:
        i.setPlainText("")

def escogerCriptosistema():
    if str(menu.currentText()) == "Criptosistema afin":
        # Clave afin
        txt_clave.setText("Ingrese los dos digitos de la clave afin separados por un espacio:")

        res_clave.setText("")
        for i in [input_aCifrar, input_aDescifrar, output_cifrado, output_descifrado]:
            i.setPlainText("")

        boton_cifrar = crearBoton(cifrado = True)
        boton_descifrar = crearBoton(cifrado = False)
        boton_cifrar.clicked.connect(lambda : botonAfin(res_clave.text().split(), input_aCifrar, output_cifrado, True))
        boton_descifrar.clicked.connect(lambda : botonAfin(res_clave.text().split(), input_aDescifrar, output_descifrado, False))
        grid.addWidget(boton_descifrar, 7, 1)
        grid.addWidget(boton_cifrar, 7, 0)

    elif str(menu.currentText()) == "Criptosistema por desplazamiento":
        # Clave por desplazamiento
        txt_clave.setText("Ingrese el digito de la clave por desplazamiento:")

        res_clave.setText("")
        for i in [input_aCifrar, input_aDescifrar, output_cifrado, output_descifrado]:
            i.setPlainText("")

        boton_cifrar = crearBoton(cifrado = True)
        boton_descifrar = crearBoton(cifrado = False)
        boton_cifrar.clicked.connect(lambda : botonDesplazamiento(res_clave.text(), input_aCifrar, output_cifrado, True))
        boton_descifrar.clicked.connect(lambda : botonDesplazamiento(res_clave.text(), input_aDescifrar, output_descifrado, False))
        grid.addWidget(boton_descifrar, 7, 1)
        grid.addWidget(boton_cifrar, 7, 0)

    elif str(menu.currentText()) == "Criptosistema por permutacion":
        txt_clave.setText("Ingrese los digitos de la matriz de permutacion separados por un espacio:")

        limpiarCampos()

        boton_cifrar = crearBoton(cifrado = True)
        boton_descifrar = crearBoton(cifrado = False)
        boton_cifrar.clicked.connect(lambda : botonPermutacion([len(res_clave.text().split()), res_clave.text()], input_aCifrar, output_cifrado, True))
        boton_descifrar.clicked.connect(lambda : botonPermutacion([len(res_clave.text().split()), res_clave.text()], input_aDescifrar, output_descifrado, False))
        grid.addWidget(boton_descifrar, 7, 1)
        grid.addWidget(boton_cifrar, 7, 0)

    elif str(menu.currentText()) == "Criptosistema de Hill":
        # Clave por desplazamiento
        grid.addWidget(txt_m, 1, 1)
        grid.addWidget(res_m, 2, 1)
        txt_clave.setText("Ingrese los valores de la matriz clave separados por un espacio: ")
        res_clave.setText("")
        res_m.setText("")
        for i in [input_aCifrar, input_aDescifrar, output_cifrado, output_descifrado]:
            i.setPlainText("")
        boton_cifrar = crearBoton(cifrado = True)
        boton_descifrar = crearBoton(cifrado = False)
        boton_cifrar.clicked.connect(lambda : botonHill(res_clave.text(), res_m.text(), input_aCifrar, output_cifrado, True))
        boton_descifrar.clicked.connect(lambda : botonDesplazamiento(res_clave.text(), input_aDescifrar, output_descifrado, False))
        grid.addWidget(boton_descifrar, 7, 1)
        grid.addWidget(boton_cifrar, 7, 0)

# Crea la ventana
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Criptosistema Afin")
window.setFixedWidth(1050)
window.setStyleSheet("background: #ffffff;")

#### Añade todos los elementos ####

# Menu de criptosistemas
menu = QComboBox()
menu.setStyleSheet(
    """
    QComboBox {
        padding:5px;
        border:1px solid #161616;
        border-radius:3%;
    }
    QComboBox::drop-down
    {
        border: 0px;
        width:20px;
    }
    QComboBox::down-arrow {
        image: url(resources/dropdown.png);
        width: 12px;
        height: 12px;
    }
    QComboBox::drop-down:hover {
       background-color:#E3E3E3;
    }
    """)
criptosistemas = ["Criptosistema afin", "Criptosistema por desplazamiento", "Criptosistema por permutacion", 
                    "Criptosistema de Hill", "Criptosistema de Vigenere"]
menu.addItems(criptosistemas)

menu.currentTextChanged.connect(escogerCriptosistema)

# Clave
txt_clave = QLabel()
txt_clave.setText("Ingrese los dos digitos de la clave afin separados por un espacio:")
res_clave = QLineEdit()
res_clave.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;")

# m de la Matriz Hill
txt_m = QLabel()
txt_m.setText("Ingrese el valor M (número de filas y columnas de la matriz clave MxM):")
res_m = QLineEdit()
res_m.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;")

# Texto a cifrar
txt_aCifrar = QLabel(text = "Ingrese el texto a cifrar:")
input_aCifrar = QPlainTextEdit()
input_aCifrar.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;")

# Texto cifrado
txt_cifrado = QLabel(text = "Texto cifrado:")
output_cifrado = QPlainTextEdit()
output_cifrado.setDisabled(True)
output_cifrado.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;color:black;")

# Button
boton_cifrar = crearBoton(cifrado = True)
boton_cifrar.clicked.connect(lambda : botonAfin(res_clave.text().split(), input_aCifrar, output_cifrado, True))

# Texto a descifrar
txt_aDescifrar = QLabel(text = "Ingrese el texto a descifrar:")
input_aDescifrar = QPlainTextEdit()
input_aDescifrar.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;")

# Texto descifrado
txt_descifrado = QLabel(text = "Texto descifrado:")
output_descifrado = QPlainTextEdit()
output_descifrado.setDisabled(True)
output_descifrado.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;color:black;")

# Button
boton_descifrar = crearBoton(cifrado = False)
boton_descifrar.clicked.connect(lambda : botonAfin(res_clave.text().split(), input_aDescifrar, output_descifrado, False))

# Añade los widgets a la ventana.
grid = QGridLayout()
grid.addWidget(menu, 0, 0)

grid.addWidget(txt_clave, 1, 0)
grid.addWidget(res_clave, 2, 0)
grid.addWidget(txt_aCifrar, 3, 0)
grid.addWidget(input_aCifrar, 4, 0)
grid.addWidget(txt_cifrado, 5, 0)
grid.addWidget(output_cifrado, 6, 0)
grid.addWidget(boton_cifrar, 7, 0)

grid.addWidget(txt_aDescifrar, 3, 1)
grid.addWidget(input_aDescifrar, 4, 1)
grid.addWidget(txt_descifrado, 5, 1)
grid.addWidget(output_descifrado, 6, 1)
grid.addWidget(boton_descifrar, 7, 1)

window.setLayout(grid)

window.show()
sys.exit(app.exec())