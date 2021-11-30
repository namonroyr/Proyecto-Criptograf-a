import sys
import math
import cv2
import numpy as np
import string
#import imageio
import vigenere as vg
import substitution as sb
import string
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage, QPalette, QBrush, QColor
from PyQt5.QtCore import (Qt, QFile, QDate, QTime, QSize, QTimer, QRect, QRegExp, QTranslator,
                          QLocale, QLibraryInfo)
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QGridLayout, QLabel, QDialog, QTableWidget, QMenu,
                             QTableWidgetItem, QAbstractItemView, QLineEdit, QPushButton, QTabWidget,
                             QActionGroup, QAction, QMessageBox, QFrame, QStyle, QGridLayout,
                             QVBoxLayout, QHBoxLayout, QLabel, QToolButton, QGroupBox, QStackedLayout,
                             QDateEdit, QComboBox, QPushButton, QFileDialog, QPlainTextEdit, QLineEdit,
                             QTextEdit)
from PyQt5.QtGui import (QFont, QIcon, QPalette, QBrush, QColor, QPixmap, QRegion, QClipboard,
                         QRegExpValidator)
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor
import hill

abc = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "I": 8, "J": 9, "K": 10,
       "L": 11, "M": 12, "N": 13, "O": 14, "P": 15, "Q": 16, "R": 17, "S": 18, "T": 19, "U": 20,
       "V": 21, "W": 22, "X": 23, "Y": 24, "Z": 25}
inv_abc = {value: key for key, value in abc.items()}

criptosistemas = ["Criptosistema Afín", "Criptosistema por Desplazamiento",
                  "Criptosistema por Permutación", "Criptosistema por Sustitución",
                  "Criptosistema de Vigenere"]


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
            i_cifrado = (abc[i.upper()] + int(b)) % 26
            texto_cifrado += inv_abc[i_cifrado]

        output.setPlainText(texto_cifrado)

    def desencriptar(self, input, output):
        b = self.clave
        texto_cifrado = input.toPlainText()

        texto_descifrado = ""
        for i in texto_cifrado:
            i_claro = (abc[i.upper()] - int(b)) % 26
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
                i_cifrado = (int(a) * abc[i.upper()] + int(b)) % 26
                texto_cifrado += inv_abc[i_cifrado]

            output.setPlainText(texto_cifrado)

        else:
            input.setPlainText("La clave ingresada no es válida")

    def desencriptar(self, input, output):
        a, b = self.clave
        if math.gcd(int(a), 26) == 1:
            texto_cifrado = input.toPlainText().strip()

            texto_descifrado = ""
            for i in texto_cifrado:
                i_claro = ((pow(int(a), -1, 26)) * (abc[i.upper()] - int(b))) % 26
                texto_descifrado += inv_abc[i_claro]

            output.setPlainText(texto_descifrado)
        else:
            input.setPlainText("La clave ingresada no es válida")


class CriptosistemaPermutacion(Criptosistema):
    def __init__(self, clave):
        super().__init__(clave)

    def encriptar(self, input, output):
        m = self.clave[0]
        values = list(map(int, self.clave[1].split()))

        if (len(set(values)) < m):
            limpiarCampos()
            input.setPlainText("Error: Ingresó valores repetidos o no ingreso {} valores".format(m))

        for a, b in zip(tuple(range(1, m + 1)), tuple(sorted(values))):
            if a != b:
                limpiarCampos()
                input.setPlainText("Error: Debe ingresar los numeros del 1 al", m)
                break

        mat_permutacion = np.array([range(1, m + 1), values]).reshape(2, m)
        texto_claro = input.toPlainText().strip()
        texto_separado = [texto_claro[i:i + m] for i in range(0, len(texto_claro), m)]

        texto_cifrado = ""
        for subtexto in texto_separado:
            for indice in range(1, m + 1):
                letra_cifrada = subtexto[int(mat_permutacion[1][int(np.where(mat_permutacion == indice)[1][0])]) - 1]
                texto_cifrado += letra_cifrada

        output.setPlainText(texto_cifrado)

    def desencriptar(self, input, output):
        m = self.clave[0]
        values = list(map(int, self.clave[1].split()))

        if (len(set(values)) < m):
            limpiarCampos()
            input.setPlainText("Error: Ingresó valores repetidos o no ingreso {} valores".format(m))

        for a, b in zip(tuple(range(1, m + 1)), tuple(sorted(values))):
            if a != b:
                limpiarCampos()
                input.setPlainText("Error: Debe ingresar los numeros del 1 al", m)
                break

        mat_inv_permutacion = np.array([range(1, m + 1), [x[0] for x in
                                                          sorted(list(zip(tuple(range(1, m + 1)), tuple(values))),
                                                                 key=lambda x: x[1])]]).reshape(2, m)
        texto_cifrado = input.toPlainText().strip()
        texto_separado = [texto_cifrado[i:i + m] for i in range(0, len(texto_cifrado), m)]

        texto_descifrado = ""
        for subtexto in texto_separado:
            for indice in range(1, m + 1):
                letra_descifrada = subtexto[
                    int(mat_inv_permutacion[1][int(np.where(mat_inv_permutacion == indice)[1][0])]) - 1]
                texto_descifrado += letra_descifrada

        output.setPlainText(texto_descifrado)


class PhotoLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAlignment(Qt.AlignCenter)
        # self.resize(300,650)
        self.setText('\n\n Arrastre la imagen aquí \n\n')
        self.setStyleSheet('''
        QLabel {
            border: 4px dashed #aaa;
            font: 17px;
        }''')

    def setPixmap(self, *args, **kwargs):
        super().setPixmap(*args, **kwargs)
        self.setStyleSheet('''
        QLabel {
            border: none;
        }''')


class Template(QWidget):
    def __init__(self):
        super().__init__()
        self.photo = PhotoLabel()
        self.file = ""
        self.setAcceptDrops(True)
        grid = QGridLayout(self)
        grid.addWidget(self.photo, 0, 0)
        self.resize(self.sizeHint())

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasImage:
            event.setDropAction(Qt.CopyAction)
            filename = event.mimeData().urls()[0].toLocalFile()
            event.accept()
            self.file = filename
            self.open_image(filename)
        else:
            event.ignore()

    def open_image(self, filename=None):
        self.photo.setPixmap(QPixmap(filename))


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


def botonHill(input, encriptar):
    image_file_name = input.file
    img_name = image_file_name.split('.')[0]
    img_extension = image_file_name.split('.')[1]
    file_ext = ['jpg', 'png', 'jpeg']
    if image_file_name != "" and img_extension in file_ext:
        img = cv2.imread(image_file_name)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        if encriptar == True:
            criptosistema_Hill = hill.Hill(img_rgb, img_name)
            encoded_img_name = criptosistema_Hill.encriptar(img_name)
            QMessageBox.information(None, 'Éxito',
                                    'Encriptación realizada, puede encrontrar la imagen encriptada en: ' + encoded_img_name + '\n' + 'La clave con la que se encriptó se encuentra en: ' + image_file_name + '_key.png',
                                    QMessageBox.Ok)
            img_d.open_image(encoded_img_name)
        elif encriptar == False and txt_key.text() != '':
            key = txt_key.text()
            img_dec_vec = hill.desencriptar(img_rgb, key)
            decoded_img_name = '{0}-descifrada.{1}'.format(img_name, img_extension)
            img_dec_gbr = cv2.cvtColor(img_dec_vec.astype(np.uint8), cv2.COLOR_RGB2BGR)
            cv2.imwrite(decoded_img_name, img_dec_gbr)
            QMessageBox.information(None, 'Éxito',
                                    'Desencriptación realizada, puede encrontrar la imagen desencriptada en: ' + decoded_img_name,
                                    QMessageBox.Ok)
            img_c.open_image(decoded_img_name)
        else:
            QMessageBox.critical(None, 'Clave no ingresada',
                                 'Sleccione el archivo que contiene la clave para descifrar la imagen (.png)',
                                 QMessageBox.Ok)
    else:
        QMessageBox.critical(None, 'Imagen no ingresada',
                             'Arrastre una imagen para procesar o ingrese una imagen con formato válido (.jpg, .png)',
                             QMessageBox.Ok)


def botonVigenere(clave, input, output, encriptar):
    texto_cifrado = input.toPlainText().strip()
    if encriptar:
        output.setPlainText(vg.encriptar(texto_cifrado, clave))
    else:
        output.setPlainText(vg.decriptar(texto_cifrado, clave))


def botonSustitucion(clave, input, output, encriptar):
    clave = ''.join([i for i in clave if i != ' ']).lower().split(',')
    clave = {i.split(':')[0]: i.split(':')[1] for i in clave}
    texto_cifrado = input.toPlainText().strip()
    sus = sb.substitution(texto_cifrado)
    if encriptar:
        sus.permutar(clave)
        output.setPlainText(sus.permutado.upper())
    else:
        sus.invert()
        output.setPlainText(sus.permutado.upper())


def crearBoton(cifrado):
    if cifrado:
        boton = QPushButton(text="Cifrar")
    else:
        boton = QPushButton(text="Descifrar")
    boton.setStyleSheet(
        """
        QPushButton {
            border:1px solid #161616;
            border-radius:5%;
            padding:5px;
            background:#145795;
            color:white;
        }
        QPushButton:hover {
            background-color:#0B3862;
            font: bold;
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
    if str(menu.currentText()) == "Criptosistema Afín":
        # Clave afin
        for i in reversed(range(1, gridcifrado.count())):
            gridcifrado.itemAt(i).widget().deleteLater()
        txt_clave_afin = QLabel()
        txt_clave_afin.setText("Ingrese los dos digitos de la clave afin separados por un espacio:")
        res_clave_afin = QLineEdit()
        res_clave_afin.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;")
        res_clave_afin.setText("")
        for i in [input_aCifrar, input_aDescifrar, output_cifrado, output_descifrado]:
            i.setPlainText("")
        boton_cifrar = crearBoton(cifrado=True)
        boton_descifrar = crearBoton(cifrado=False)
        boton_cifrar.clicked.connect(lambda: botonAfin(res_clave.text().split(), input_aCifrar, output_cifrado, True))
        boton_descifrar.clicked.connect(
            lambda: botonAfin(res_clave.text().split(), input_aDescifrar, output_descifrado, False))
        gridcifrado.addWidget(txt_clave_afin, 1, 0)
        gridcifrado.addWidget(res_clave_afin, 2, 0)
        gridcifrado.addWidget(boton_descifrar, 7, 1)
        gridcifrado.addWidget(boton_cifrar, 7, 0)

    elif str(menu.currentText()) == "Criptosistema por Desplazamiento":
        # Clave por desplazamiento
        txt_clave.setText("Ingrese el dígito de la clave por Desplazamiento:")
        res_clave.setText("")
        for i in [input_aCifrar, input_aDescifrar, output_cifrado, output_descifrado]:
            i.setPlainText("")
        boton_cifrar = crearBoton(cifrado=True)
        boton_descifrar = crearBoton(cifrado=False)
        boton_cifrar.clicked.connect(lambda: botonDesplazamiento(res_clave.text(), input_aCifrar, output_cifrado, True))
        boton_descifrar.clicked.connect(
            lambda: botonDesplazamiento(res_clave.text(), input_aDescifrar, output_descifrado, False))
        gridcifrado.addWidget(boton_descifrar, 7, 1)
        gridcifrado.addWidget(boton_cifrar, 7, 0)

    elif str(menu.currentText()) == "Criptosistema por Permutación":
        txt_clave.setText("Ingrese los digitos de la matriz de permutación separados por un espacio:")
        limpiarCampos()
        boton_cifrar = crearBoton(cifrado=True)
        boton_descifrar = crearBoton(cifrado=False)
        boton_cifrar.clicked.connect(
            lambda: botonPermutacion([len(res_clave.text().split()), res_clave.text()], input_aCifrar, output_cifrado,
                                     True))
        boton_descifrar.clicked.connect(
            lambda: botonPermutacion([len(res_clave.text().split()), res_clave.text()], input_aDescifrar,
                                     output_descifrado, False))
        gridcifrado.addWidget(boton_descifrar, 7, 1)
        gridcifrado.addWidget(boton_cifrar, 7, 0)
    elif str(menu.currentText()) == "Criptosistema de Vigenere":
        txt_clave.setText("Ingrese la palabra clave:")
        limpiarCampos()
        boton_cifrar = crearBoton(cifrado=True)
        boton_descifrar = crearBoton(cifrado=False)
        boton_cifrar.clicked.connect(lambda: botonVigenere(res_clave.text(), input_aCifrar, output_cifrado, True))
        boton_descifrar.clicked.connect(
            lambda: botonVigenere(res_clave.text(), input_aDescifrar, output_descifrado, False))
        gridcifrado.addWidget(boton_descifrar, 7, 1)
        gridcifrado.addWidget(boton_cifrar, 7, 0)
    elif str(menu.currentText()) == "Criptosistema por Sustitución":
        txt_clave.setText(
            "Ingrese la regla de sustitución (letra seguido por \":\" y la letra que la sustituye) separado por comas:")
        limpiarCampos()
        boton_cifrar = crearBoton(cifrado=True)
        boton_descifrar = crearBoton(cifrado=False)
        boton_cifrar.clicked.connect(lambda: botonSustitucion(res_clave.text(), input_aCifrar, output_cifrado, True))
        boton_descifrar.clicked.connect(
            lambda: botonSustitucion(res_clave.text(), input_aDescifrar, output_descifrado, False))
        gridcifrado.addWidget(boton_descifrar, 7, 1)
        gridcifrado.addWidget(boton_cifrar, 7, 0)


# Crea la ventana
app = QApplication(sys.argv)
app.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
window = QtWidgets.QMainWindow()
window.setWindowTitle("CriptoTool")
window.setFixedWidth(1200)
window.setFixedHeight(770)
# window.setStyleSheet("background: #ffffff;")
font = QtGui.QFont()
font.setFamily("Segoe UI SemiLight")
font.setPointSize(10)
QApplication.setFont(font)
#### Añade todos los elementos ####
# Tab
tabWidget = QtWidgets.QTabWidget(window)
tabWidget.setGeometry(QtCore.QRect(25, 55, 1150, 700))
tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
tabWidget.setObjectName("tabWidget")
tabWidget.setStyleSheet("""
QTabWidget::tab-bar {
    left: 1px; /* move to the right by 5px */
}
QTabWidget::pane {
    border: 1px solid lightgray;
    top:-1px;
    background-color: #FFFFFF;
    }
QTabBar::tab {
    background: #0B3862;
    color: white;
    font-size: 20px;
    min-width: 200px;
    min-height: 30px;
    padding: 2px;
}
QTabBar::tab:selected, QTabBar::tab:hover {
    background: #145795;
    font: bold;
                        }
QTabBar::tab:!selected {
    margin-top: 3px;
}""")
cifrado = QtWidgets.QWidget()
tabWidget.addTab(cifrado, "Cifrado/Descifrado")
gridcifrado = QGridLayout(cifrado)
gridcifrado.setGeometry(QtCore.QRect(10, 10, 1030, 600))
# ------------------Hill----------------------------------
Hill = QtWidgets.QWidget()
tabWidget.addTab(Hill, "Hill - Imagen")
gridHill = QGridLayout(Hill)
gridHill.setGeometry(QtCore.QRect(10, 10, 1030, 600))
img_c = Template()
img_d = Template()
txt_img = QLabel()
txt_img.setText("Imagen a encriptar / encriptada: ")
txt_img.setAlignment(Qt.AlignCenter)
txt_img.setStyleSheet('''
QLabel {
    font-size: 22px;
    font-family: Segoe UI;
}''')
txt_img_d = QLabel()
txt_img_d.setText("Imagen a desencriptar / desencriptada: ")
txt_img_d.setAlignment(Qt.AlignCenter)
txt_img_d.setStyleSheet('''
QLabel {
    font-size: 22px;
    font-family: Segoe UI;
}''')
boton_cifrar_hill = crearBoton(cifrado=True)
boton_descifrar_hill = crearBoton(cifrado=False)
boton_cifrar_hill.clicked.connect(lambda: botonHill(img_c, True))
boton_descifrar_hill.clicked.connect(lambda: botonHill(img_d, False))
boton_limpiar = QPushButton(text="Limpiar")
boton_limpiar.setStyleSheet(
    """
QPushButton {
    border:1px solid #161616;
    border-radius:5%;
    padding:5px;
    background:#0B3862;
    color:white;
}
QPushButton:hover {
    background-color:#145795;
    font: bold;
}
""")
boton_limpiar.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
boton_limpiar.setFixedWidth(150)
boton_limpiar.clicked.connect(lambda: clean(gridHill))


def clean(layout):
    global img_c, img_d, boton_cifrar_hill, boton_descifrar_hill
    txt_key.setText('')
    img_c.setParent(None)
    img_d.setParent(None)
    boton_cifrar_hill.setParent(None)
    boton_descifrar_hill.setParent(None)
    img_c = Template()
    img_d = Template()
    boton_cifrar_hill = crearBoton(cifrado=True)
    boton_descifrar_hill = crearBoton(cifrado=False)
    boton_cifrar_hill.clicked.connect(lambda: botonHill(img_c, True))
    boton_descifrar_hill.clicked.connect(lambda: botonHill(img_d, False))
    gridHill.addWidget(img_c, 1, 0, 4, 1)
    gridHill.addWidget(img_d, 1, 2, 4, 1)
    gridHill.addWidget(boton_cifrar_hill, 2, 1)
    gridHill.addWidget(boton_descifrar_hill, 3, 1)


boton_browsekey = QPushButton(text="Clave")
boton_browsekey.setStyleSheet(
    """
QPushButton {
    border:1px solid #161616;
    border-radius:5%;
    padding:5px;
    background:#0B3862;
    color:white;
}
QPushButton:hover {
    background-color:#145795;
    font: bold;
}
""")
boton_browsekey.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
boton_browsekey.setFixedWidth(150)
boton_browsekey.clicked.connect(lambda: browse_key())


def browse_key():
    fname = QFileDialog.getOpenFileName(None, 'Select key file', QtCore.QDir.rootPath())
    txt_key.setText(fname[0])


txt_key = QLabel()
txt_key.setStyleSheet('''
QLabel {
    border:1px solid #161616;
}''')
boton_key = QPushButton(text="Clave")
boton_key.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
boton_key.setFixedWidth(150)
boton_key.clicked.connect(lambda: info())


def info():
    QMessageBox.information(None, 'Info',
                            'La clave para encriptar (Involutory Key) se genera automáticamente y se almacena en un archivo .png',
                            QMessageBox.Ok)


txt_key2 = QLabel()
txt_key2.setText('*Nota: Siempre limpiar campos antes de \n encriptar/desencriptar')
gridHill.addWidget(img_c, 1, 0, 6, 1)
gridHill.addWidget(img_d, 1, 2, 6, 1)
gridHill.addWidget(txt_img, 0, 0)
gridHill.addWidget(txt_img_d, 0, 2)
gridHill.addWidget(boton_cifrar_hill, 2, 1)
gridHill.addWidget(boton_descifrar_hill, 3, 1)
gridHill.addWidget(boton_limpiar, 5, 1)
gridHill.addWidget(boton_key, 8, 0)
gridHill.addWidget(txt_key2, 9, 0)
gridHill.addWidget(boton_browsekey, 8, 2)
gridHill.addWidget(txt_key, 9, 2)

# ----------Criptoanalisis-----------------
criptoitems = ["Criptoanálisis Afín", "Criptoanálisis Desplazamiento", "Criptoanálisis Hill / Permutación", "Criptoanálisis Sustitución",
               "Criptoanálisis Vigenere"]


def vigenereAnalisis(input_criptoanalysis, output_descifrado):
    texto = input_criptoanalysis.toPlainText().strip()
    res = list(vg.vigenereAttack(texto))
    if len(res) == 0:
        print("entra1")
        output_descifrado.setPlainText("No se encontró ninguna palabra clave.")
    else:
        retorno = ''
        for j, k in res:
            retorno = retorno + 'La clave podría ser ' + j.upper() + '. De ser ese el caso el texto descifrado es:\n' + k + '\n'
        output_descifrado.setPlainText(retorno)


def desplazamientoAnalisis(input_criptoanalysis, output_descifrado):
    texto = input_criptoanalysis.toPlainText().strip()
    texto = texto.upper()
    texto = [i for i in texto if i in string.ascii_uppercase]
    output = ""
    for i in range(1, 26):
        lista = [(abc[k] + i) % 26 for k in texto]
        lista = [string.ascii_uppercase[k] for k in lista]
        output = output + "Con desplazamiento {}: \n".format(i) + ''.join(lista) + "\n"
    output_descifrado.setPlainText(output)


def afinAnalisis(input_criptoanalysis, output_descifrado):
    texto = input_criptoanalysis.toPlainText().strip().upper()
    texto = [i for i in texto if i in string.ascii_uppercase]
    output = ""
    for i in range(1, 26):
        if math.gcd(i, 26) > 1:
            continue
        inverse_m = [k for k in range(1, 26) if (i * k) % 26 == 1][0]
        for j in range(1, 26):
            if math.gcd(i, j) > 1:
                continue
            inverse_s = 26 - j
            if (i, j) == (3, 5):
                print(inverse_m, inverse_s)
            output = output + "Para a = {} y b = {} el texto es:\n".format(i, j) + ''.join(
                [string.ascii_uppercase[(inverse_m * (abc[k] + inverse_s)) % 26] for k in texto]) + '\n'
    output_descifrado.setPlainText(output)


# ------menu---------------
menu_cripto = QComboBox()
menu_cripto.setStyleSheet(
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
menu_cripto.addItems(criptoitems)

menu_cripto.setCurrentIndex(0)
tabWidget.setCurrentIndex(0)
# menu_cripto.setCurrentText("Criptoanálisis Afín")
# escogerCriptoanalisis()
criptanalysis = QWidget()
tabWidget.addTab(criptanalysis, "Criptoanálisis")
gridCripto = QVBoxLayout()
criptanalysis.setLayout(gridCripto)
gridCripto.setGeometry(QtCore.QRect(10, 10, 1030, 600))
stackedLayout = QStackedLayout()
# Afin**************************
afin_ca = QWidget()
afinLayout = QGridLayout()
input_label = QLabel()
input_label.setText("Texto Cifrado")
input_criptoanalysisafin = QPlainTextEdit()
input_criptoanalysisafin.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;")
decript_label = QLabel()
decript_label.setText("Llave / Texto Claro")
output_descifradoafin = QPlainTextEdit()
output_descifradoafin.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;color:black;")
output_descifradoafin.setReadOnly(True)
boton_submitafin = QPushButton(text="Submit")
boton_submitafin.setStyleSheet(
    """
    QPushButton {
        border:1px solid #161616;
        border-radius:5%;
        padding:5px;
        background:#145795;
        color:white;
    }
    QPushButton:hover {
        background-color:#0B3862;
        font: bold;
    }
    """)
afinLayout.addWidget(input_label, 0, 1)
afinLayout.addWidget(decript_label, 0, 2)
afinLayout.addWidget(input_criptoanalysisafin, 1, 1)
afinLayout.addWidget(output_descifradoafin, 1, 2)
afinLayout.addWidget(boton_submitafin, 2, 1)
afin_ca.setLayout(afinLayout)
stackedLayout.addWidget(afin_ca)
boton_submitafin.clicked.connect(lambda: afinAnalisis(input_criptoanalysisafin, output_descifradoafin))
# Desplazamiento*********************************
des_ca = QWidget()
desLayout = QGridLayout()
input_label = QLabel()
input_label.setText("Texto Cifrado")
input_criptoanalysisDesplazamiento = QPlainTextEdit()
input_criptoanalysisDesplazamiento.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;")
decript_label = QLabel()
decript_label.setText("Llave / Texto Claro")
output_descifradoDesplazamiento = QPlainTextEdit()
output_descifradoDesplazamiento.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;color:black;")
output_descifradoDesplazamiento.setReadOnly(True)
boton_submitDesplazamiento = QPushButton(text="Submit")
boton_submitDesplazamiento.setStyleSheet(
    """
    QPushButton {
        border:1px solid #161616;
        border-radius:5%;
        padding:5px;
        background:#145795;
        color:white;
    }
    QPushButton:hover {
        background-color:#0B3862;
        font: bold;
    }
    """)
desLayout.addWidget(input_label, 0, 1)
desLayout.addWidget(decript_label, 0, 2)
desLayout.addWidget(input_criptoanalysisDesplazamiento, 1, 1)
desLayout.addWidget(output_descifradoDesplazamiento, 1, 2)
desLayout.addWidget(boton_submitDesplazamiento, 2, 1)
des_ca.setLayout(desLayout)
stackedLayout.addWidget(des_ca)
boton_submitDesplazamiento.clicked.connect(
    lambda: desplazamientoAnalisis(input_criptoanalysisDesplazamiento, output_descifradoDesplazamiento))
# Hill**************************
hill_ca = QWidget()
hillLayout = QGridLayout()
txt_plano = QLabel()
txt_plano.setText("Ingrese el texto plano: ")
input_plano = QPlainTextEdit()
input_plano.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;")
txt_cifrado = QLabel()
txt_cifrado.setText("Ingrese el correspondiente texto crifrado: ")
input_cifrado = QPlainTextEdit()
input_cifrado.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;")
boton_getkey = QPushButton(text="Obtener Clave")
boton_getkey.setStyleSheet(
    """
    QPushButton {
        border:1px solid #161616;
        border-radius:5%;
        padding:5px;
        background:#145795;
        color:white;
    }
    QPushButton:hover {
        background-color:#0B3862;
        font: bold;
    }
    """)
boton_getkey.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
boton_getkey.setFixedWidth(170)
boton_getkey.clicked.connect(lambda: criptanalisisHill(input_plano, input_cifrado))

boton_limpiar_caHill = QPushButton(text="Limpiar Campos")
boton_limpiar_caHill.setStyleSheet(
    """
QPushButton {
    border:1px solid #161616;
    border-radius:5%;
    padding:5px;
    background:#0B3862;
    color:white;
}
QPushButton:hover {
    background-color:#145795;
    font: bold;
}
""")
boton_limpiar_caHill.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
boton_limpiar_caHill.setFixedWidth(170)


def limpiarCampos_caHill():
    res_clave.setText("")
    for i in [input_plano, input_cifrado, output_m, output_keyfound]:
        i.setPlainText("")


boton_limpiar_caHill.clicked.connect(limpiarCampos_caHill)
txt_m = QLabel()
txt_m.setText("Valor de m: ")
output_m = QPlainTextEdit()
output_m.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;color:black;")
output_m.setReadOnly(True)
txt_keyfound = QLabel()
txt_keyfound.setText("Clave: ")
output_keyfound = QPlainTextEdit()
output_keyfound.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;color:black;")
output_keyfound.setReadOnly(True)
hillLayout.addWidget(txt_plano, 0, 0)
hillLayout.addWidget(input_plano, 1, 0)
hillLayout.addWidget(txt_cifrado, 2, 0)
hillLayout.addWidget(input_cifrado, 3, 0)
hillLayout.addWidget(boton_getkey, 0, 1, -1, 1)
hillLayout.addWidget(boton_limpiar_caHill, 2, 1, -1, 1)
hillLayout.addWidget(txt_m, 0, 2)
hillLayout.addWidget(output_m, 1, 2)
hillLayout.addWidget(txt_keyfound, 2, 2)
hillLayout.addWidget(output_keyfound, 3, 2)
hill_ca.setLayout(hillLayout)
stackedLayout.addWidget(hill_ca)
# Add the combo box and the stacked layout to the top-level layout
gridCripto.addWidget(menu_cripto)
gridCripto.addLayout(stackedLayout)


def switchPage():
    stackedLayout.setCurrentIndex(menu_cripto.currentIndex())


menu_cripto.currentTextChanged.connect(switchPage)

# Permutación*********************************
'''
permutacion_ca = QWidget()
permutacionLayout = QGridLayout()
input_label = QLabel()
input_label.setText("Texto Cifrado")
input_criptoanalysisPermutacion = QPlainTextEdit()
input_criptoanalysisPermutacion.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;")
decript_label = QLabel()
decript_label.setText("Llave / Texto Claro")
output_descifradoPermutacion = QPlainTextEdit()
output_descifradoPermutacion.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;color:black;")
output_descifradoPermutacion.setReadOnly(True)
boton_submit = QPushButton(text="Submit")
permutacionLayout.addWidget(input_label, 0, 1)
permutacionLayout.addWidget(decript_label, 0, 2)
permutacionLayout.addWidget(input_criptoanalysisPermutacion, 1, 1)
permutacionLayout.addWidget(output_descifradoPermutacion, 1, 2)
permutacionLayout.addWidget(boton_submit, 2, 1)
permutacion_ca.setLayout(permutacionLayout)
stackedLayout.addWidget(permutacion_ca)
'''
# Sustitución*********************************
alphabet_string = string.ascii_uppercase
alphabet_list = list(alphabet_string)

sustitucion_ca = QWidget()
sus_layout = QHBoxLayout()
crifrado_sus_label = QLabel()
crifrado_sus_label.setText("Texto Cifrado:")
crifrado_sus = QPlainTextEdit()
crifrado_sus.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;")
boton_analizarsus = QPushButton(text="Analizar")
boton_analizarsus.setFixedWidth(150)
boton_analizarsus.clicked.connect(lambda: criptanalisisSus(crifrado_sus))
boton_analizarsus.setStyleSheet(
    """
    QPushButton {
        border:1px solid #161616;
        border-radius:5%;
        padding:5px;
        background:#145795;
        color:white;
    }
    QPushButton:hover {
        background-color:#0B3862;
        font: bold;
    }
    """)
decript_label = QLabel()
decript_label.setText("Texto Plano con \nsustituciones introducidas:")
output_descifrado_sus = QPlainTextEdit()
output_descifrado_sus.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;color:black;")
output_descifrado_sus.setReadOnly(True)
# letters
a_label = QLabel()
a_label.setText("A")
b_label = QLabel()
b_label.setText("B")
c_label = QLabel()
c_label.setText("C")
d_label = QLabel()
d_label.setText("D")
e_label = QLabel()
e_label.setText("E")
f_label = QLabel()
f_label.setText("F")
g_label = QLabel()
g_label.setText("G")
h_label = QLabel()
h_label.setText("H")
i_label = QLabel()
i_label.setText("I")
j_label = QLabel()
j_label.setText("J")
k_label = QLabel()
k_label.setText("K")
l_label = QLabel()
l_label.setText("L")
m_label = QLabel()
m_label.setText("M")
n_label = QLabel()
n_label.setText("N")
o_label = QLabel()
o_label.setText("O")
p_label = QLabel()
p_label.setText("P")
q_label = QLabel()
q_label.setText("Q")
r_label = QLabel()
r_label.setText("R")
s_label = QLabel()
s_label.setText("S")
t_label = QLabel()
t_label.setText("T")
u_label = QLabel()
u_label.setText("U")
v_label = QLabel()
v_label.setText("V")
w_label = QLabel()
w_label.setText("W")
x_label = QLabel()
x_label.setText("X")
y_label = QLabel()
y_label.setText("Y")
z_label = QLabel()
z_label.setText("Z")
a_label.setAlignment(QtCore.Qt.AlignCenter)
b_label.setAlignment(QtCore.Qt.AlignCenter)
c_label.setAlignment(QtCore.Qt.AlignCenter)
d_label.setAlignment(QtCore.Qt.AlignCenter)
e_label.setAlignment(QtCore.Qt.AlignCenter)
f_label.setAlignment(QtCore.Qt.AlignCenter)
g_label.setAlignment(QtCore.Qt.AlignCenter)
h_label.setAlignment(QtCore.Qt.AlignCenter)
i_label.setAlignment(QtCore.Qt.AlignCenter)
j_label.setAlignment(QtCore.Qt.AlignCenter)
k_label.setAlignment(QtCore.Qt.AlignCenter)
l_label.setAlignment(QtCore.Qt.AlignCenter)
m_label.setAlignment(QtCore.Qt.AlignCenter)
n_label.setAlignment(QtCore.Qt.AlignCenter)
o_label.setAlignment(QtCore.Qt.AlignCenter)
p_label.setAlignment(QtCore.Qt.AlignCenter)
q_label.setAlignment(QtCore.Qt.AlignCenter)
r_label.setAlignment(QtCore.Qt.AlignCenter)
s_label.setAlignment(QtCore.Qt.AlignCenter)
t_label.setAlignment(QtCore.Qt.AlignCenter)
u_label.setAlignment(QtCore.Qt.AlignCenter)
v_label.setAlignment(QtCore.Qt.AlignCenter)
w_label.setAlignment(QtCore.Qt.AlignCenter)
x_label.setAlignment(QtCore.Qt.AlignCenter)
y_label.setAlignment(QtCore.Qt.AlignCenter)
z_label.setAlignment(QtCore.Qt.AlignCenter)

sus_a = QComboBox()
sus_a.addItems(alphabet_list)
sus_b = QComboBox()
sus_b.addItems(alphabet_list)
sus_c = QComboBox()
sus_c.addItems(alphabet_list)
sus_d = QComboBox()
sus_d.addItems(alphabet_list)
sus_e = QComboBox()
sus_e.addItems(alphabet_list)
sus_f = QComboBox()
sus_f.addItems(alphabet_list)
sus_g = QComboBox()
sus_g.addItems(alphabet_list)
sus_h = QComboBox()
sus_h.addItems(alphabet_list)
sus_i = QComboBox()
sus_i.addItems(alphabet_list)
sus_j = QComboBox()
sus_j.addItems(alphabet_list)
sus_k = QComboBox()
sus_k.addItems(alphabet_list)
sus_l = QComboBox()
sus_l.addItems(alphabet_list)
sus_m = QComboBox()
sus_m.addItems(alphabet_list)
sus_n = QComboBox()
sus_n.addItems(alphabet_list)
sus_o = QComboBox()
sus_o.addItems(alphabet_list)
sus_p = QComboBox()
sus_p.addItems(alphabet_list)
sus_q = QComboBox()
sus_q.addItems(alphabet_list)
sus_r = QComboBox()
sus_r.addItems(alphabet_list)
sus_s = QComboBox()
sus_s.addItems(alphabet_list)
sus_t = QComboBox()
sus_t.addItems(alphabet_list)
sus_u = QComboBox()
sus_u.addItems(alphabet_list)
sus_v = QComboBox()
sus_v.addItems(alphabet_list)
sus_w = QComboBox()
sus_w.addItems(alphabet_list)
sus_x = QComboBox()
sus_x.addItems(alphabet_list)
sus_y = QComboBox()
sus_y.addItems(alphabet_list)
sus_z = QComboBox()
sus_z.addItems(alphabet_list)
boton_applysus = QPushButton(text="Aplicar")
boton_applysus.clicked.connect(lambda: aplicar(lista_caracteres, crifrado_sus, output_descifrado_sus))
boton_applysus.setFixedWidth(100)
boton_applysus.setStyleSheet(
    """
    QPushButton {
        border:1px solid #161616;
        border-radius:5%;
        padding:5px;
        background:#145795;
        color:white;
    }
    QPushButton:hover {
        background-color:#0B3862;
        font: bold;
    }
    """)

monfreq_eng = QLabel()
monfreq_eng.setText('Probabilidad de ocurrencia \nde letras en Inglés')
monoeng_table = QTableWidget()
font = QtGui.QFont()
font.setFamily("Segoe UI Semilight")
font.setPointSize(8)
monoeng_table.setFont(font)
monoeng_table.setColumnCount(4)
monoeng_table.setRowCount(13)
monoeng_table.resizeRowsToContents()
monoeng_table.setHorizontalHeaderLabels(["Letra", "Proba.", "Letra", "Proba."])
monoeng_table.resizeRowsToContents()
monoeng_table.resizeColumnsToContents()
monoeng_table.verticalHeader().hide()
header = monoeng_table.horizontalHeader()

for row in range(13):
    item = alphabet_list[row]
    cell = QTableWidgetItem(item)
    cell.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
    monoeng_table.setItem(row, 0, cell)

for row in range(13):
    item = alphabet_list[row + 13]
    cell = QTableWidgetItem(item)
    cell.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
    monoeng_table.setItem(row, 2, cell)

letters_prob = [0.082, 0.015, 0.028, 0.043, 0.127, 0.022, 0.020, 0.061, 0.070,
                0.002, 0.008, 0.040, 0.240, 0.067, 0.075, 0.019, 0.001, 0.060,
                0.063, 0.091, 0.028, 0.010, 0.023, 0.001, 0.020, 0.001]

for row in range(13):
    item = str(letters_prob[row])
    cell = QTableWidgetItem(item)
    cell.setTextAlignment(Qt.AlignRight)
    cell.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
    monoeng_table.setItem(row, 1, cell)

for row in range(13):
    item = str(letters_prob[row + 13])
    cell = QTableWidgetItem(item)
    cell.setTextAlignment(Qt.AlignRight)
    cell.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
    monoeng_table.setItem(row, 3, cell)

digrams = ['TH', 'HE', 'IN', 'ER', 'AN', 'RE', 'ED', 'ON', 'ES', 'ST',
           'EN', 'AT', 'TO', 'NT', 'HA', 'ND', 'OU', 'EA', 'NG', 'AS',
           'OR', 'TI', 'IS', 'ET', 'IT', 'AR', 'TE', 'SE', 'HI', 'OF']

difreq_eng = QLabel()
difreq_eng.setText('Digramas más frecuentes \nen Inglés')
digeng_table = QTableWidget()
digeng_table.setFont(font)
digeng_table.setColumnCount(5)
digeng_table.setRowCount(6)
digeng_table.resizeRowsToContents()
digeng_table.resizeColumnsToContents()
digeng_table.verticalHeader().hide()
digeng_table.horizontalHeader().hide()

for row in range(6):
    item = digrams[row]
    cell = QTableWidgetItem(item)
    cell.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
    digeng_table.setItem(row, 0, cell)
for row in range(6):
    item = digrams[row + 6]
    cell = QTableWidgetItem(item)
    cell.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
    digeng_table.setItem(row, 1, cell)
for row in range(6):
    item = digrams[row + 12]
    cell = QTableWidgetItem(item)
    cell.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
    digeng_table.setItem(row, 2, cell)
for row in range(6):
    item = digrams[row + 18]
    cell = QTableWidgetItem(item)
    cell.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
    digeng_table.setItem(row, 3, cell)
for row in range(6):
    item = digrams[row + 24]
    cell = QTableWidgetItem(item)
    cell.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
    digeng_table.setItem(row, 4, cell)

trigrams = ['THE', 'ING', 'AND', 'HER', 'ERE', 'ENT', 'THA', 'NTH', 'WAS', 'ETH', 'FOR', 'DTH']

trifreq_eng = QLabel()
trifreq_eng.setText('Trigramas más frecuentes \nen Inglés')
trigeng_table = QTableWidget()
trigeng_table.setFont(font)
trigeng_table.setColumnCount(5)
trigeng_table.setRowCount(2)
trigeng_table.resizeRowsToContents()
trigeng_table.resizeColumnsToContents()
trigeng_table.verticalHeader().hide()
trigeng_table.horizontalHeader().hide()

for row in range(2):
    item = trigrams[row]
    cell = QTableWidgetItem(item)
    cell.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
    trigeng_table.setItem(row, 0, cell)
for row in range(2):
    item = trigrams[row + 2]
    cell = QTableWidgetItem(item)
    cell.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
    trigeng_table.setItem(row, 1, cell)
for row in range(2):
    item = trigrams[row + 4]
    cell = QTableWidgetItem(item)
    cell.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
    trigeng_table.setItem(row, 2, cell)
for row in range(2):
    item = trigrams[row + 6]
    cell = QTableWidgetItem(item)
    cell.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
    trigeng_table.setItem(row, 3, cell)
for row in range(2):
    item = trigrams[row + 8]
    cell = QTableWidgetItem(item)
    cell.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
    trigeng_table.setItem(row, 4, cell)

monfreq_txt = QLabel()
monfreq_txt.setText('Frecuencia de Monogramas en \nel texto')
monofreq_out = QTableWidget()
difreq_txt = QLabel()
difreq_txt.setText('Frecuencia de Digramas en el \ntexto')
difreq_out = QTableWidget()
trifreq_txt = QLabel()
trifreq_txt.setText('Frecuencia de Trigramas en el \ntexto')
trifreq_out = QTableWidget()

sus1_ly = QVBoxLayout()
sus1_ly.addWidget(crifrado_sus_label)
sus1_ly.addWidget(crifrado_sus)
sus1_ly.addWidget(boton_analizarsus)
sus1_ly.addWidget(decript_label)
sus1_ly.addWidget(output_descifrado_sus)

sus2_ly = QGridLayout()
sus2_ly.addWidget(monfreq_eng, 0, 0)
sus2_ly.addWidget(monoeng_table, 1, 0)
sus2_ly.addWidget(difreq_eng, 2, 0)
sus2_ly.addWidget(digeng_table, 3, 0)
sus2_ly.addWidget(trifreq_eng, 4, 0)
sus2_ly.addWidget(trigeng_table, 5, 0)
sus2_ly.addWidget(monfreq_txt, 0, 1)
sus2_ly.addWidget(monofreq_out, 1, 1)
sus2_ly.addWidget(difreq_txt, 2, 1)
sus2_ly.addWidget(difreq_out, 3, 1)
sus2_ly.addWidget(trifreq_txt, 4, 1)
sus2_ly.addWidget(trifreq_out, 5, 1)

d_k = QLabel()
d_k.setText('d(y)')
d_k.setAlignment(QtCore.Qt.AlignCenter)
y = QLabel()
y.setText('y')
y.setAlignment(QtCore.Qt.AlignCenter)
d_k1 = QLabel()
d_k1.setText('dₖ(y)')
d_k1.setAlignment(QtCore.Qt.AlignCenter)
y1 = QLabel()
y1.setText('y')
y1.setAlignment(QtCore.Qt.AlignCenter)
d_k2 = QLabel()
d_k2.setText('dₖ(y)')
d_k2.setAlignment(QtCore.Qt.AlignCenter)
y2 = QLabel()
y2.setText('y')
y2.setAlignment(QtCore.Qt.AlignCenter)

sustitucionLayout = QGridLayout()

sustitucionLayout.addWidget(d_k, 1, 0)
sustitucionLayout.addWidget(a_label, 2, 0)
sustitucionLayout.addWidget(b_label, 3, 0)
sustitucionLayout.addWidget(c_label, 4, 0)
sustitucionLayout.addWidget(d_label, 5, 0)
sustitucionLayout.addWidget(e_label, 6, 0)
sustitucionLayout.addWidget(f_label, 7, 0)
sustitucionLayout.addWidget(g_label, 8, 0)
sustitucionLayout.addWidget(h_label, 9, 0)
sustitucionLayout.addWidget(i_label, 10, 0)
sustitucionLayout.addWidget(y, 1, 1)
sustitucionLayout.addWidget(sus_a, 2, 1)
sustitucionLayout.addWidget(sus_b, 3, 1)
sustitucionLayout.addWidget(sus_c, 4, 1)
sustitucionLayout.addWidget(sus_d, 5, 1)
sustitucionLayout.addWidget(sus_e, 6, 1)
sustitucionLayout.addWidget(sus_f, 7, 1)
sustitucionLayout.addWidget(sus_g, 8, 1)
sustitucionLayout.addWidget(sus_h, 9, 1)
sustitucionLayout.addWidget(sus_i, 10, 1)
sustitucionLayout.addWidget(d_k1, 1, 2)
sustitucionLayout.addWidget(j_label, 2, 2)
sustitucionLayout.addWidget(k_label, 3, 2)
sustitucionLayout.addWidget(l_label, 4, 2)
sustitucionLayout.addWidget(m_label, 5, 2)
sustitucionLayout.addWidget(n_label, 6, 2)
sustitucionLayout.addWidget(o_label, 7, 2)
sustitucionLayout.addWidget(p_label, 8, 2)
sustitucionLayout.addWidget(q_label, 9, 2)
sustitucionLayout.addWidget(r_label, 10, 2)
sustitucionLayout.addWidget(y1, 1, 3)
sustitucionLayout.addWidget(sus_j, 2, 3)
sustitucionLayout.addWidget(sus_k, 3, 3)
sustitucionLayout.addWidget(sus_l, 4, 3)
sustitucionLayout.addWidget(sus_m, 5, 3)
sustitucionLayout.addWidget(sus_n, 6, 3)
sustitucionLayout.addWidget(sus_o, 7, 3)
sustitucionLayout.addWidget(sus_p, 8, 3)
sustitucionLayout.addWidget(sus_q, 9, 3)
sustitucionLayout.addWidget(sus_r, 10, 3)
sustitucionLayout.addWidget(d_k2, 1, 4)
sustitucionLayout.addWidget(s_label, 2, 4)
sustitucionLayout.addWidget(t_label, 3, 4)
sustitucionLayout.addWidget(u_label, 4, 4)
sustitucionLayout.addWidget(v_label, 5, 4)
sustitucionLayout.addWidget(w_label, 6, 4)
sustitucionLayout.addWidget(x_label, 7, 4)
sustitucionLayout.addWidget(y_label, 8, 4)
sustitucionLayout.addWidget(z_label, 9, 4)

sustitucionLayout.addWidget(y2, 1, 5)
sustitucionLayout.addWidget(sus_s, 2, 5)
sustitucionLayout.addWidget(sus_t, 3, 5)
sustitucionLayout.addWidget(sus_u, 4, 5)
sustitucionLayout.addWidget(sus_v, 5, 5)
sustitucionLayout.addWidget(sus_w, 6, 5)
sustitucionLayout.addWidget(sus_x, 7, 5)
sustitucionLayout.addWidget(sus_y, 8, 5)
sustitucionLayout.addWidget(sus_z, 9, 5)
nn_l = QLabel()
nn_l.setText('')
sustitucionLayout.addWidget(nn_l, 0, 6)
sustitucionLayout.addWidget(boton_applysus, 11, 2, 1, 2)

sus_layout.addLayout(sus1_ly)
sus_layout.addLayout(sustitucionLayout)
sus_layout.addLayout(sus2_ly)
sus_layout.addStretch(1)

sustitucion_ca.setLayout(sus_layout)
stackedLayout.addWidget(sustitucion_ca)
lista_caracteres = [sus_a, sus_b, sus_c, sus_d, sus_e, sus_f, sus_g, sus_h, sus_i,
                    sus_j, sus_k, sus_l, sus_m, sus_n, sus_o, sus_p, sus_q, sus_r,
                    sus_s, sus_t, sus_u, sus_v, sus_w, sus_x, sus_y, sus_z]

# Vigenere*********************************
vigenere_ca = QWidget()
vigenereLayout = QGridLayout()
input_label = QLabel()
input_label.setText("Texto Cifrado")
input_criptoanalysisVigenere = QPlainTextEdit()
input_criptoanalysisVigenere.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;")
decript_label = QLabel()
decript_label.setText("Llave / Texto Claro")
output_descifradoVigenere = QPlainTextEdit()
output_descifradoVigenere.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;color:black;")
output_descifradoVigenere.setReadOnly(True)
boton_submitVigenere = QPushButton(text="Submit")
boton_submitVigenere.setStyleSheet(
    """
    QPushButton {
        border:1px solid #161616;
        border-radius:5%;
        padding:5px;
        background:#145795;
        color:white;
    }
    QPushButton:hover {
        background-color:#0B3862;
        font: bold;
    }
    """)
vigenereLayout.addWidget(input_label, 0, 1)
vigenereLayout.addWidget(decript_label, 0, 2)
vigenereLayout.addWidget(input_criptoanalysisVigenere, 1, 1)
vigenereLayout.addWidget(output_descifradoVigenere, 1, 2)
vigenereLayout.addWidget(boton_submitVigenere, 2, 1)
vigenere_ca.setLayout(vigenereLayout)
stackedLayout.addWidget(vigenere_ca)
boton_submitVigenere.clicked.connect(lambda: vigenereAnalisis(input_criptoanalysisVigenere, output_descifradoVigenere))
# --------------------------funciones criptoanalisis--------------------------
def criptanalisisHill(txt_plano, txt_cifrado):
    p = txt_plano.toPlainText().strip().upper()
    c = txt_cifrado.toPlainText().strip().upper()
    texto_cifrado = []
    texto_plano = []
    for i in c:
        i_cifrado = abc[i.upper()] % 26
        texto_cifrado.append(i_cifrado)
    for i in p:
        i_plano = abc[i.upper()] % 26
        texto_plano.append(i_plano)
    if len(texto_cifrado) == len(texto_plano):
        v, m, k = hill.attack(texto_plano, texto_cifrado)
        if not v:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('No se encontró una clave para los textos ingresados')
        else:
            output_m.setPlainText(str(m))
            output_keyfound.setPlainText(str(k))
    else:
        error_dialog = QtWidgets.QErrorMessage()
        error_dialog.showMessage('Los textos ingresados deben tener la misma longitud de caracteres')


def criptanalisisSus(txt):
    alphabet_lower = string.ascii_lowercase

    txt_cifrado = txt.toPlainText().strip()
    cipher = sb.substitution(txt_cifrado)
    freq_mono = cipher.mono()
    freq_di = cipher.digrams()
    freq_tri = cipher.trigrams()
    # *-*-*-*-*-*-
    monofreq_out.setFont(font)
    monofreq_out.setColumnCount(2)
    monofreq_out.setRowCount(26)
    monofreq_out.resizeRowsToContents()
    monofreq_out.setHorizontalHeaderLabels(["Letra", "Freq."])
    monofreq_out.resizeRowsToContents()
    monofreq_out.resizeColumnsToContents()
    monofreq_out.verticalHeader().hide()
    alphabet_list = sorted(freq_mono, key=lambda x: freq_mono[x])
    alphabet_list.reverse()
    for row in range(26):
        item = alphabet_list[row].upper()
        cell = QTableWidgetItem(item)
        cell.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        monofreq_out.setItem(row, 0, cell)

    for row in range(26):
        try:
            item = str(freq_mono[alphabet_list[row]])
        except:
            item = str(0)
        cell = QTableWidgetItem(item)
        cell.setTextAlignment(Qt.AlignRight)
        cell.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        monofreq_out.setItem(row, 1, cell)

    difreq_out.setFont(font)
    difreq_out.setColumnCount(2)
    difreq_out.setRowCount(len(freq_di))
    difreq_out.resizeRowsToContents()
    difreq_out.setHorizontalHeaderLabels(["Digrama", "Freq."])
    difreq_out.resizeRowsToContents()
    difreq_out.resizeColumnsToContents()
    difreq_out.verticalHeader().hide()
    digrams_order = sorted(freq_di, key=lambda x: freq_di[x])
    digrams_order.reverse()

    for row in range(len(freq_di)):
        item = digrams_order[row].upper()
        cell = QTableWidgetItem(item)
        cell.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        difreq_out.setItem(row, 0, cell)
    for row in range(len(freq_di)):
        try:
            item = str(freq_di[digrams_order[row]])
        except:
            item = ""
        cell = QTableWidgetItem(item)
        cell.setTextAlignment(Qt.AlignRight)
        cell.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        difreq_out.setItem(row, 1, cell)

    trifreq_out.setFont(font)
    trifreq_out.setColumnCount(2)
    trifreq_out.setRowCount(len(freq_tri))
    trifreq_out.resizeRowsToContents()
    trifreq_out.setHorizontalHeaderLabels(["Trigrama", "Freq."])
    trifreq_out.resizeRowsToContents()
    trifreq_out.resizeColumnsToContents()
    trifreq_out.verticalHeader().hide()
    trigrams_order = sorted(freq_tri, key=lambda x: freq_tri[x])
    trigrams_order.reverse()
    for row in range(len(freq_tri)):
        item = trigrams_order[row].upper()
        cell = QTableWidgetItem(item)
        cell.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        trifreq_out.setItem(row, 0, cell)
    for row in range(len(freq_tri)):
        try:
            item = str(freq_tri[trigrams_order[row]])
        except:
            item = ""
        cell = QTableWidgetItem(item)
        cell.setTextAlignment(Qt.AlignRight)
        cell.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        trifreq_out.setItem(row, 1, cell)


def aplicar(lista_caracteres, txt_in, txt_out):
    llave = {string.ascii_lowercase[i]: str(lista_caracteres[i].currentText()).lower() for i in range(26)}
    if len(set(j for i,j in llave.items())) < 26:
        txt_out.setPlainText("Esta sustitución no es válida. La función de esta sustitución no es inyectiva. Por favor inténtelo de nuevo")
        return
    cypher = sb.substitution(txt_in.toPlainText().strip())
    cypher.permutar(llave)
    txt_out.setPlainText(str(cypher.permutado))
    criptanalisisSus(txt_out)


"""
#------funcion menu-------
def clean2(layout):
    for i in reversed(range(layout.count())):
        if layout.itemAt(i):
            layout.itemAt(i).widget().setParent(None)
def escogerCriptoanalisis():
    if str(menu_cripto.currentText()) == "Criptoanalisis Afín":
        clean2(gridCripto)
        gridCripto.addWidget(menu_cripto, 1, 0)
        input_criptoanalysis = QPlainTextEdit()
        input_criptoanalysis.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;")
        output_descifrado = QPlainTextEdit()
        output_descifrado.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;color:black;")
        output_descifrado.setReadOnly(True)
        gridCripto.addWidget(input_criptoanalysis,1,1)
        gridCripto.addWidget(output_descifrado,1,2)
        boton_submit = QPushButton(text="submit")
        gridCripto.addWidget(boton_submit,2,1)
        input_label = QLabel()
        input_label.setText("Texto Cifrado")
        gridCripto.addWidget(input_label,0,1)
        decript_label = QLabel()
        decript_label.setText("Llave / Texto Claro")
        gridCripto.addWidget(decript_label,0,2)
    elif str(menu_cripto.currentText()) == "Criptoanalisis Desplazamiento":
        clean2(gridCripto)
        gridCripto.addWidget(menu_cripto, 1, 0)
        input_criptoanalysis = QPlainTextEdit()
        input_criptoanalysis.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;")
        output_descifrado = QPlainTextEdit()
        output_descifrado.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;color:black;")
        output_descifrado.setReadOnly(True)
        gridCripto.addWidget(input_criptoanalysis, 1, 1)
        gridCripto.addWidget(output_descifrado, 1, 2)
        boton_submit = QPushButton(text="submit")
        gridCripto.addWidget(boton_submit, 2, 1)
        input_label = QLabel()
        input_label.setText("Texto Cifrado")
        gridCripto.addWidget(input_label, 0, 1)
        decript_label = QLabel()
        decript_label.setText("Llave / Texto Claro")
        gridCripto.addWidget(decript_label, 0, 2)
        boton_submit.clicked.connect(lambda: desplazamientoAnalisis(input_criptoanalysis, output_descifrado))
    elif str(menu_cripto.currentText()) == "Criptoanalisis Sustitución":
        clean2(gridCripto)
        gridCripto.addWidget(menu_cripto, 0, 0)
    elif str(menu_cripto.currentText()) == "Criptoanalisis Permutación":
        clean2(gridCripto)
        gridCripto.addWidget(menu_cripto, 0, 0)
    elif str(menu_cripto.currentText()) == "Criptoanalisis Vigenere":
        clean2(gridCripto)
        gridCripto.addWidget(menu_cripto, 1, 0)
        input_criptoanalysis = QPlainTextEdit()
        input_criptoanalysis.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;")
        output_descifrado = QPlainTextEdit()
        output_descifrado.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;color:black;")
        output_descifrado.setReadOnly(True)
        gridCripto.addWidget(input_criptoanalysis, 1, 1)
        gridCripto.addWidget(output_descifrado, 1, 2)
        boton_submit = QPushButton(text="submit")
        gridCripto.addWidget(boton_submit, 2, 1)
        input_label = QLabel()
        input_label.setText("Texto Cifrado")
        gridCripto.addWidget(input_label, 0, 1)
        decript_label = QLabel()
        decript_label.setText("Llave / Texto Claro")
        gridCripto.addWidget(decript_label, 0, 2)
        boton_submit.clicked.connect(lambda: vigenereAnalisis(input_criptoanalysis,output_descifrado))
    elif str(menu_cripto.currentText()) == "Criptoanalisis Hill":
        clean2(gridCripto)
        gridCripto.addWidget(menu_cripto, 1, 0)
        input_criptoanalysis = QPlainTextEdit()
        input_criptoanalysis.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;")
        output_descifrado = QPlainTextEdit()
        output_descifrado.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;color:black;")
        gridCripto.addWidget(input_criptoanalysis, 1, 1)
        gridCripto.addWidget(output_descifrado, 1, 2)
        boton_submit = QPushButton(text="submit")
        gridCripto.addWidget(boton_submit, 2, 1)
        input_label = QLabel()
        input_label.setText("Texto Cifrado")
        gridCripto.addWidget(input_label, 0, 1)
        decript_label = QLabel()
        decript_label.setText("Texto Claro")
        gridCripto.addWidget(decript_label, 0, 2)
        matrix_text = QLabel()
        matrix_text.setText("Matrix")
        Matrix = QPlainTextEdit()
        Matrix.setReadOnly(True)
        gridCripto.addWidget(matrix_text,2,2)
        gridCripto.addWidget(Matrix,3,2)
"""

# MenuBar
menubar = QtWidgets.QMenuBar(window)
menubar.setGeometry(QtCore.QRect(0, 0, 500, 200))
menubar.setStyleSheet("""
QMenuBar{
    padding: 2px 10px;
    background-color: #0B3862;
    color: #51CBFF;
    border-radius: 5px;
    font-size: 22px;
    }
QMenu::item {
    height: 42px;
    margin: 0px;
    }""")
menuClasicos = QtWidgets.QMenu(menubar)
menuBloque = QtWidgets.QMenu(menubar)
menuClaveP = QtWidgets.QMenu(menubar)
#menuSalir = QtWidgets.QMenu(menubar)
window.setMenuBar(menubar)
menuClasicos.setTitle("Criptosistemas CLÁSICOS")
menuBloque.setTitle("DE BLOQUE")
menuClaveP.setTitle("CLAVE PÚBLICA")
#menuSalir.setTitle("Salir")
menubar.addAction(menuClasicos.menuAction())
menubar.addAction(menuBloque.menuAction())
menubar.addAction(menuClaveP.menuAction())
#menubar.addAction(menuSalir.menuAction())

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
menu.addItems(criptosistemas)
menu.currentTextChanged.connect(escogerCriptosistema)
menu.setCurrentIndex(0)
# Clave
txt_clave = QLabel()
txt_clave.setText("Ingrese los dos digitos de la clave afin separados por un espacio:")
res_clave = QLineEdit()
res_clave.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;")

# Texto a cifrar
txt_aCifrar = QLabel(text="Ingrese el texto a cifrar:")
input_aCifrar = QPlainTextEdit()
input_aCifrar.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;")

# Texto cifrado
txt_cifrado = QLabel(text="Texto cifrado:")
output_cifrado = QPlainTextEdit()
output_cifrado.setDisabled(True)
output_cifrado.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;color:black;")

# Button
boton_cifrar = crearBoton(cifrado=True)
boton_cifrar.clicked.connect(lambda: botonAfin(res_clave.text().split(), input_aCifrar, output_cifrado, True))

# Texto a descifrar
txt_aDescifrar = QLabel(text="Ingrese el texto a descifrar:")
input_aDescifrar = QPlainTextEdit()
input_aDescifrar.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;")

# Texto descifrado
txt_descifrado = QLabel(text="Texto descifrado:")
output_descifrado = QPlainTextEdit()
output_descifrado.setDisabled(True)
output_descifrado.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;color:black;")

# Button
boton_descifrar = crearBoton(cifrado=False)
boton_descifrar.clicked.connect(lambda: botonAfin(res_clave.text().split(), input_aDescifrar, output_descifrado, False))

# Añade los widgets al tab de cifrado
gridcifrado.addWidget(menu, 0, 0)
gridcifrado.addWidget(txt_clave, 1, 0)
gridcifrado.addWidget(res_clave, 2, 0)
gridcifrado.addWidget(txt_aCifrar, 3, 0)
gridcifrado.addWidget(input_aCifrar, 4, 0)
gridcifrado.addWidget(txt_cifrado, 5, 0)
gridcifrado.addWidget(output_cifrado, 6, 0)
gridcifrado.addWidget(boton_cifrar, 7, 0)

gridcifrado.addWidget(txt_aDescifrar, 3, 1)
gridcifrado.addWidget(input_aDescifrar, 4, 1)
gridcifrado.addWidget(txt_descifrado, 5, 1)
gridcifrado.addWidget(output_descifrado, 6, 1)
gridcifrado.addWidget(boton_descifrar, 7, 1)

window.show()
sys.exit(app.exec())
