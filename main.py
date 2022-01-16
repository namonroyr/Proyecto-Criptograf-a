import sys
import os
import math
import cv2
import numpy as np
import string
import hill
import AES, DES
import vigenere as vg
import substitution as sb
import classic_crypto as cc
import string
from pyDes import *
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

# Modes of crypting / cyphering
ECB =	0
CBC =	1

# Modes of padding
PAD_NORMAL = 1
PAD_PKCS5 = 2

class PhotoLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAlignment(Qt.AlignCenter)
        # self.resize(300,650)
        self.setText('\n\n Drop image Here \n\n')
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

def crearBoton(cifrado):
    if cifrado:
        boton = QPushButton(text="Encrypt")
    else:
        boton = QPushButton(text="Decrypt")
    boton.setStyleSheet(
        """
        QPushButton {
            border-radius:5%;
            padding:5px;
            background:#52F6E0;
            font: 12pt;
            font: semi-bold;
        }
        QPushButton:hover {
            background-color: #13A5EE;
            color:white;
            font: bold;
            }
        """)
    boton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    boton.setFixedWidth(150)
    return boton

class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        vbox = QVBoxLayout()
        self.hbox1 = QHBoxLayout()
        self.hbox2 = QHBoxLayout()
        self.hbox1.setAlignment(Qt.AlignCenter)
        self.hbox2.setAlignment(Qt.AlignCenter)
        vbox.setAlignment(Qt.AlignCenter)
        self.image = QLabel()
        self.image.setPixmap(QPixmap('resources/Cryptool_logo.png'))
        buttonStyle = """
        QPushButton {
            width: 170px;
            border-radius: 5%;
            padding: 5px;
            background: #52F6E0;
            color: #283433;
            font: 14pt;
            font: semi-bold;
        }
        QPushButton:hover {
            background-color: #4DB4FA;
            color: white;
        }
        """
        self.clasicos_button = QPushButton("Classic")
        self.bloque_button = QPushButton("Block")
        self.gamma_button = QPushButton("Gamma-Pentagonal")
        self.clasicos_button.setStyleSheet(buttonStyle)
        self.bloque_button.setStyleSheet(buttonStyle)
        self.gamma_button.setStyleSheet(buttonStyle)
        self.clasicos_button.clicked.connect(self.gotoclasicos)
        self.bloque_button.clicked.connect(self.gotobloque)
        #self.gamma_button.clicked.connect(self.gotogamma)
        self.hbox1.addWidget(self.image)
        self.hbox2.addWidget(self.clasicos_button)
        self.hbox2.addWidget(self.bloque_button)
        self.hbox2.addWidget(self.gamma_button)
        vbox.addLayout(self.hbox1)
        vbox.addLayout(self.hbox2)
        self.setLayout(vbox)
        #self.show()

    def gotoclasicos(self):
        widget.setCurrentIndex(1)

    def gotobloque(self):
        widget.setCurrentIndex(2)

class ClasicosScreen(QDialog):

    def __init__(self):
        super(ClasicosScreen, self).__init__()
        # Tab
        vbox1 = QVBoxLayout()
        hbox1 = QHBoxLayout()
        hbox1.setAlignment(Qt.AlignRight)
        self.back_button = QPushButton("Back to Main Menu")
        back_buttonStyle = """
        QPushButton {
            width: 170px;
            border-radius: 5%;
            padding: 5px;
            background: #8DD3F6;
            font: 12pt;
            font: semi-bold;
        }
        QPushButton:hover {
            background-color: #4DB4FA;
            color: white;
        }
        """
        self.back_button.setStyleSheet(back_buttonStyle)
        self.back_button.clicked.connect(lambda: widget.setCurrentIndex(0))
        tabWidget = QtWidgets.QTabWidget(self)
        vbox1.addWidget(tabWidget)
        hbox1.addWidget(self.back_button)
        vbox1.addLayout(hbox1)
        self.setLayout(vbox1)
        tabWidget.setGeometry(QtCore.QRect(10, 20, 1150, 700))
        tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        tabWidget.setObjectName("tabWidget")
        tabWidget.setStyleSheet("""
        QTabWidget::tab-bar {
            left: 1px; /* move to the right by 5px */
        }
        QTabWidget::pane {
            top:-1px;
            background-color: #FFFFFF;
        }
        QTabBar::tab {
            background: #52F6E0;
            font-size: 15px;
            min-width: 200px;
            min-height: 30px;
            padding: 2px;
        }
        QTabBar::tab:selected, QTabBar::tab:hover {
            background: #13A5EE;
            color: white;
            font: bold;
        }
        QTabBar::tab:!selected {
            margin-top: 3px;
        }""")
        cifrado = QtWidgets.QWidget()
        tabWidget.addTab(cifrado, "Encryption/Decryption")
        gridcifrado = QGridLayout(cifrado)
        gridcifrado.setGeometry(QtCore.QRect(10, 10, 1030, 600))
        # Menu de criptosistemas
        menu = QComboBox(self)
        menu.setStyleSheet(
            """
            QComboBox {
                padding:5px;
                border:1px solid #161616;
                border-radius:3%;
                }
            QComboBox::drop-down {
                border:0px;
                width:20px;
                }
            QComboBox::down-arrow {
                image: url(resources/dropdown.png);
                width: 12px;
                height: 12px;
                }
            QComboBox::drop-down:hover {
                background-color: #D7DDE1;
                }
            """)
        self.txt_crypto = QLabel()
        self.txt_crypto.setText("Select a Cryptosystem:")
        criptosistemas = ["Affine cipher", "Shift cipher",
                          "Permutation cipher", "Substitution cipher",
                          "Vigenère cipher"]
        """
        Buttons ----------------------------------------------------------
        """

        def botonAfin(clave, input, output, encriptar):
            print("Flag0")
            texto_cifrado = input.toPlainText().strip()
            criptosistema_afin = cc.CriptosistemaAfin(clave)
            if encriptar == True:
                output.setPlainText(criptosistema_afin.encriptar(texto_cifrado))
                print("Flag4")
            elif encriptar == False:
                output.setPlainText(criptosistema_afin.desencriptar(texto_cifrado))

        def botonDesplazamiento(clave, input, output, encriptar):
            texto_cifrado = input.toPlainText().strip()
            criptosistema_desplazamiento = cc.CriptosistemaDesplazamiento(clave)
            if encriptar == True:
                output.setPlainText(criptosistema_desplazamiento.encriptar(texto_cifrado))
            elif encriptar == False:
                output.setPlainText(criptosistema_desplazamiento.desencriptar(texto_cifrado))

        def botonPermutacion(clave, input, output, encriptar):
            texto_cifrado = input.toPlainText().strip()
            criptosistema_permutacion = cc.CriptosistemaPermutacion(clave)
            if encriptar == True:
                output.setPlainText(criptosistema_permutacion.encriptar(texto_cifrado))
            elif encriptar == False:
                output.setPlainText(criptosistema_permutacion.desencriptar(texto_cifrado))

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
                if len(set(k for j,k in sus.key.items())) < 26:
                    output.setPlainText("Permutación inválida. Las llaves no definidas son reemplazadas por ellas mismas. Dicho esto: asegúrese de que este mapa es inyectivo")
                else:
                    output.setPlainText(sus.permutado.upper())
            else:
                sus.permutar({v: k for k, v in clave.items()})
                if len(set(k for j,k in sus.key.items())) < 26:
                    output.setPlainText("Permutación inválida. Las llaves no definidas son reemplazadas por ellas mismas. Dicho esto: asegúrese de que este mapa es inyectivo")
                else:
                    output.setPlainText(sus.permutado.upper())

        self.txt_clave = QLabel()
        self.txt_clave.setText("Ingrese los dos digitos de la clave afin separados por un espacio:")
        self.res_clave = QLineEdit()
        self.res_clave.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;")
        # Texto a cifrar
        self.txt_aCifrar = QLabel(text="Ingrese el texto a cifrar:")
        self.input_aCifrar = QPlainTextEdit()
        self.input_aCifrar.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;")
        # Texto cifrado
        self.txt_cifrado = QLabel(text="Texto cifrado:")
        self.output_cifrado = QPlainTextEdit()
        self.output_cifrado.setDisabled(True)
        self.output_cifrado.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;color:black;")

        # Button
        self.boton_cifrar = crearBoton(cifrado=True)
        self.boton_cifrar.clicked.connect(lambda: botonAfin(self.res_clave.text().split(), self.input_aCifrar, self.output_cifrado, True))

        # Texto a descifrar
        self.txt_aDescifrar = QLabel(text="Ingrese el texto a descifrar:")
        self.input_aDescifrar = QPlainTextEdit()
        self.input_aDescifrar.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;")
        # Texto descifrado
        self.txt_descifrado = QLabel(text="Texto descifrado:")
        self.output_descifrado = QPlainTextEdit()
        self.output_descifrado.setDisabled(True)
        self.output_descifrado.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;color:black;")
        # Button
        self.boton_descifrar = crearBoton(cifrado=False)
        self.boton_descifrar.clicked.connect(lambda: botonAfin(self.res_clave.text().split(), self.input_aDescifrar, self.output_descifrado, False))

        def limpiarCampos():
            self.res_clave.setText("")
            for i in [self.input_aCifrar, self.input_aDescifrar, self.output_cifrado, self.output_descifrado]:
                i.setPlainText("")

        def escogerCriptosistema():
            if str(menu.currentText()) == "Affine cipher":
                # Clave afin
                self.txt_clave.setText("Ingrese los dos digitos de la clave afin separados por un espacio:")
                limpiarCampos()
                self.boton_cifrar = crearBoton(cifrado=True)
                self.boton_descifrar = crearBoton(cifrado=False)
                self.boton_cifrar.clicked.connect(lambda: botonAfin(self.res_clave.text().split(), self.input_aCifrar, self.output_cifrado, True))
                self.boton_descifrar.clicked.connect(
                    lambda: botonAfin(self.res_clave.text().split(), self.input_aDescifrar, self.output_descifrado, False))
                gridcifrado.addWidget(self.boton_descifrar, 8, 1)
                gridcifrado.addWidget(self.boton_cifrar, 8, 0)

            elif str(menu.currentText()) == "Shift cipher":
                # Clave por desplazamiento
                self.txt_clave.setText("Ingrese el dígito de la clave por Desplazamiento:")
                limpiarCampos()
                self.boton_cifrar = crearBoton(cifrado=True)
                self.boton_descifrar = crearBoton(cifrado=False)
                self.boton_cifrar.clicked.connect(lambda: botonDesplazamiento(self.res_clave.text(), self.input_aCifrar, self.output_cifrado, True))
                self.boton_descifrar.clicked.connect(
                    lambda: botonDesplazamiento(self.res_clave.text(), self.input_aDescifrar, self.output_descifrado, False))
                gridcifrado.addWidget(self.boton_descifrar, 8, 1)
                gridcifrado.addWidget(self.boton_cifrar, 8, 0)

            elif str(menu.currentText()) == "Permutation cipher":
                self.txt_clave.setText("Ingrese los digitos de la matriz de permutación separados por un espacio:")
                limpiarCampos()
                self.boton_cifrar = crearBoton(cifrado=True)
                self.boton_descifrar = crearBoton(cifrado=False)
                self.boton_cifrar.clicked.connect(
                    lambda: botonPermutacion([len(self.res_clave.text().split()), self.res_clave.text()], self.input_aCifrar, self.output_cifrado,
                                             True))
                self.boton_descifrar.clicked.connect(
                    lambda: botonPermutacion([len(self.res_clave.text().split()), self.res_clave.text()], self.input_aDescifrar,
                                             self.output_descifrado, False))
                gridcifrado.addWidget(self.boton_descifrar, 8, 1)
                gridcifrado.addWidget(self.boton_cifrar, 8, 0)
            elif str(menu.currentText()) == "Vigenère cipher":
                self.txt_clave.setText("Ingrese la palabra clave:")
                limpiarCampos()
                self.boton_cifrar = crearBoton(cifrado=True)
                self.boton_descifrar = crearBoton(cifrado=False)
                self.boton_cifrar.clicked.connect(lambda: botonVigenere(self.res_clave.text(), self.input_aCifrar, self.output_cifrado, True))
                self.boton_descifrar.clicked.connect(
                    lambda: botonVigenere(self.res_clave.text(), self.input_aDescifrar, self.output_descifrado, False))
                gridcifrado.addWidget(self.boton_descifrar, 8, 1)
                gridcifrado.addWidget(self.boton_cifrar, 8, 0)
            elif str(menu.currentText()) == "Substitution cipher":
                self.txt_clave.setText(
                    "Ingrese la regla de sustitución (letra seguido por \":\" y la letra que la sustituye) separado por comas:")
                limpiarCampos()
                self.boton_cifrar = crearBoton(cifrado=True)
                self.boton_descifrar = crearBoton(cifrado=False)
                self.boton_cifrar.clicked.connect(lambda: botonSustitucion(self.res_clave.text(), self.input_aCifrar, self.output_cifrado, True))
                self.boton_descifrar.clicked.connect(
                    lambda: botonSustitucion(self.res_clave.text(), self.input_aDescifrar, self.output_descifrado, False))
                gridcifrado.addWidget(self.boton_descifrar, 8, 1)
                gridcifrado.addWidget(self.boton_cifrar, 8, 0)

        menu.addItems(criptosistemas)
        menu.currentTextChanged.connect(escogerCriptosistema)
        menu.setCurrentIndex(0)

        gridcifrado.addWidget(self.txt_crypto, 0, 0)
        gridcifrado.addWidget(menu, 1, 0)
        gridcifrado.addWidget(self.txt_clave, 2, 0)
        gridcifrado.addWidget(self.res_clave, 3, 0)
        gridcifrado.addWidget(self.txt_aCifrar, 4, 0)
        gridcifrado.addWidget(self.input_aCifrar, 5, 0)
        gridcifrado.addWidget(self.txt_cifrado, 6, 0)
        gridcifrado.addWidget(self.output_cifrado, 7, 0)
        gridcifrado.addWidget(self.boton_cifrar, 8, 0)
        gridcifrado.addWidget(self.txt_aDescifrar, 4, 1)
        gridcifrado.addWidget(self.input_aDescifrar, 5, 1)
        gridcifrado.addWidget(self.txt_descifrado, 6, 1)
        gridcifrado.addWidget(self.output_descifrado, 7, 1)
        gridcifrado.addWidget(self.boton_descifrar, 8, 1)

        """
        ****************-----------------Hill Tab-----------------------*********************
        """
        def botonHill(input, output_ref, encriptar):
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
                    output_ref.open_image(encoded_img_name)
                elif encriptar == False and txt_key.text() != '':
                    key = txt_key.text()
                    img_dec_vec = hill.desencriptar(img_rgb, key)
                    decoded_img_name = '{0}-descifrada.{1}'.format(img_name, img_extension)
                    img_dec_gbr = cv2.cvtColor(img_dec_vec.astype(np.uint8), cv2.COLOR_RGB2BGR)
                    cv2.imwrite(decoded_img_name, img_dec_gbr)
                    QMessageBox.information(None, 'Éxito',
                                            'Desencriptación realizada, puede encrontrar la imagen desencriptada en: ' + decoded_img_name,
                                            QMessageBox.Ok)
                    output_ref.open_image(decoded_img_name)
                    #print()
                else:
                    QMessageBox.critical(None, 'Clave no ingresada',
                                         'Seleccione el archivo que contiene la clave para descifrar la imagen (.png)',
                                         QMessageBox.Ok)
            else:
                QMessageBox.critical(None, 'Imagen no ingresada',
                                     'Arrastre una imagen para procesar o ingrese una imagen con formato válido (.jpg, .png)',
                                     QMessageBox.Ok)

        Hill = QtWidgets.QWidget()
        tabWidget.addTab(Hill, "Hill - Image")
        gridHill = QGridLayout(Hill)
        gridHill.setGeometry(QtCore.QRect(10, 10, 1030, 600))
        img_c = Template()
        img_d = Template()
        txt_img = QLabel()
        txt_img.setText("Image to encrypt / decrypted: ")
        txt_img.setAlignment(Qt.AlignCenter)
        txt_img.setStyleSheet('''
        QLabel {
            font-size: 22px;
            font-family: Segoe UI;
        }''')
        txt_img_d = QLabel()
        txt_img_d.setText("Imagen to decrypt / encrypted: ")
        txt_img_d.setAlignment(Qt.AlignCenter)
        txt_img_d.setStyleSheet('''
        QLabel {
            font-size: 22px;
            font-family: Segoe UI;
        }''')
        boton_cifrar_hill = crearBoton(cifrado=True)
        boton_descifrar_hill = crearBoton(cifrado=False)
        boton_cifrar_hill.clicked.connect(lambda: botonHill(img_c, img_d, True))
        boton_descifrar_hill.clicked.connect(lambda: botonHill(img_d, img_c, False))
        boton_limpiar = QPushButton(text="Clean")
        aux_style = """
        QPushButton {
            border-radius:5%;
            padding:5px;
            background:#9E6CFA;
            color:white;
        }
        QPushButton:hover {
            background-color:#4DB4FA;
            font: bold;
            }
            """
        boton_limpiar.setStyleSheet(aux_style)
        boton_limpiar.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        boton_limpiar.setFixedWidth(150)
        boton_limpiar.clicked.connect(lambda: clean(gridHill, img_c, img_d, boton_cifrar_hill, boton_descifrar_hill))

        def clean(layout, img_c, img_d, boton_cifrar_hill, boton_descifrar_hill):
            txt_key.setText('')
            boton_cifrar_hill.setParent(None)
            boton_descifrar_hill.setParent(None)
            img_c.setParent(None)
            img_d.setParent(None)
            img_c = Template()
            img_d = Template()
            boton_cifrar_hill = crearBoton(cifrado=True)
            boton_descifrar_hill = crearBoton(cifrado=False)
            boton_cifrar_hill.clicked.connect(lambda: botonHill(img_c, img_d, True))
            boton_descifrar_hill.clicked.connect(lambda: botonHill(img_d, img_c, False))
            gridHill.addWidget(img_c, 1, 0, 4, 1)
            gridHill.addWidget(img_d, 1, 2, 4, 1)
            gridHill.addWidget(boton_cifrar_hill, 2, 1)
            gridHill.addWidget(boton_descifrar_hill, 3, 1)

        boton_browsekey = QPushButton(text="Key")
        boton_browsekey.setStyleSheet(aux_style)
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


        """
        ****************-----------------criptanalysis Tab-----------------------*********************
        """

        criptoitems = ["Affine cipher", "Shift cipher",
                          "Hill/Permutation cipher", "Substitution cipher",
                          "Vigenère cipher"]

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
        criptanalysis = QWidget()
        tabWidget.addTab(criptanalysis, "Cryptanalysis")
        gridCripto = QVBoxLayout()
        criptanalysis.setLayout(gridCripto)
        gridCripto.setGeometry(QtCore.QRect(10, 10, 1030, 600))
        stackedLayout = QStackedLayout()
        # Afin**************************
        afin_ca = QWidget()
        afinLayout = QGridLayout()
        input_label = QLabel()
        input_label.setText("Cipher Text")
        input_criptoanalysisafin = QPlainTextEdit()
        input_criptoanalysisafin.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;")
        decript_label = QLabel()
        decript_label.setText("Key / Plain Text")
        output_descifradoafin = QPlainTextEdit()
        output_descifradoafin.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;color:black;")
        output_descifradoafin.setReadOnly(True)
        boton_submitafin = QPushButton(text="Submit")
        submit_style = """
        QPushButton {
            width: 70px;
            border-radius:5%;
            padding:5px;
            background:#52F6E0;
            font: 12pt;
            font: semi-bold;
        }
        QPushButton:hover {
            background-color: #13A5EE;
            color:white;
            font: bold;
            }
        """
        boton_submitafin.setStyleSheet(submit_style)
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
        input_label.setText("Cipher Text")
        input_criptoanalysisDesplazamiento = QPlainTextEdit()
        input_criptoanalysisDesplazamiento.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;")
        decript_label = QLabel()
        decript_label.setText("Key / Plain Text")
        output_descifradoDesplazamiento = QPlainTextEdit()
        output_descifradoDesplazamiento.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;color:black;")
        output_descifradoDesplazamiento.setReadOnly(True)
        boton_submitDesplazamiento = QPushButton(text="Submit")
        boton_submitDesplazamiento.setStyleSheet(submit_style)
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
        txt_plano.setText("Plain Text: ")
        input_plano = QPlainTextEdit()
        input_plano.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;")
        txt_cifrado = QLabel()
        txt_cifrado.setText("Cipher Text: ")
        input_cifrado = QPlainTextEdit()
        input_cifrado.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;")
        boton_getkey = QPushButton(text="Get Key")
        boton_getkey.setStyleSheet(submit_style)
        boton_getkey.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        boton_getkey.setFixedWidth(170)
        boton_getkey.clicked.connect(lambda: criptanalisisHill(input_plano, input_cifrado))

        boton_limpiar_caHill = QPushButton(text="Clean")
        boton_limpiar_caHill.setStyleSheet(aux_style)
        boton_limpiar_caHill.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        boton_limpiar_caHill.setFixedWidth(170)


        def limpiarCampos_caHill():
            res_clave.setText("")
            for i in [input_plano, input_cifrado, output_m, output_keyfound]:
                i.setPlainText("")


        boton_limpiar_caHill.clicked.connect(limpiarCampos_caHill)
        txt_m = QLabel()
        txt_m.setText("m value: ")
        output_m = QPlainTextEdit()
        output_m.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;color:black;")
        output_m.setReadOnly(True)
        txt_keyfound = QLabel()
        txt_keyfound.setText("Key: ")
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

        # Sustitución*********************************
        alphabet_string = string.ascii_uppercase
        alpha = list(alphabet_string)
        alphabet_list = [1]
        alphabet_list[0] = '-'
        alphabet_list.extend(alpha)

        sustitucion_ca = QWidget()
        sus_layout = QHBoxLayout()
        crifrado_sus_label = QLabel()
        crifrado_sus_label.setText("Cipher Text:")
        crifrado_sus = QPlainTextEdit()
        crifrado_sus.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;")
        boton_analizarsus = QPushButton(text="Analizar")
        boton_analizarsus.setFixedWidth(150)
        boton_analizarsus.clicked.connect(lambda: criptanalisisSus(crifrado_sus))
        boton_analizarsus.setStyleSheet(submit_style)
        decript_label = QLabel()
        decript_label.setText("Plain Text\n with selected substitutions:")
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
        boton_applysus = QPushButton(text="Apply")
        boton_applysus.clicked.connect(lambda: aplicar(lista_caracteres, crifrado_sus, output_descifrado_sus))
        boton_applysus.setFixedWidth(100)
        boton_applysus.setStyleSheet(submit_style)

        monfreq_eng = QLabel()
        monfreq_eng.setText('Probability of occurrence \nde english letters')
        monoeng_table = QTableWidget()
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semilight")
        font.setPointSize(8)
        monoeng_table.setFont(font)
        monoeng_table.setColumnCount(4)
        monoeng_table.setRowCount(13)
        monoeng_table.resizeRowsToContents()
        monoeng_table.setHorizontalHeaderLabels(["Letter", "Proba.", "Letter", "Proba."])
        monoeng_table.resizeRowsToContents()
        monoeng_table.resizeColumnsToContents()
        monoeng_table.verticalHeader().hide()
        header = monoeng_table.horizontalHeader()

        for row in range(1,14):
            item = alphabet_list[row]
            cell = QTableWidgetItem(item)
            cell.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            monoeng_table.setItem(row-1, 0, cell)

        for row in range(13):
            item = alphabet_list[row + 14]
            cell = QTableWidgetItem(item)
            cell.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            monoeng_table.setItem(row-1, 2, cell)

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
        difreq_eng.setText('Most frequent digrams \nin English')
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
        trifreq_eng.setText('Most frequent trigrams \nin English')
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
        monfreq_txt.setText('Monograms frequency \nin the text')
        monofreq_out = QTableWidget()
        difreq_txt = QLabel()
        difreq_txt.setText('Digrams frequency \nin the text')
        difreq_out = QTableWidget()
        trifreq_txt = QLabel()
        trifreq_txt.setText('Trigrams frequency \nin the text')
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
        d_k.setText('dₖ(y)')
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
        input_label.setText("Cipher Text")
        input_criptoanalysisVigenere = QPlainTextEdit()
        input_criptoanalysisVigenere.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;")
        decript_label = QLabel()
        decript_label.setText("Key / Plain text")
        output_descifradoVigenere = QPlainTextEdit()
        output_descifradoVigenere.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;color:black;")
        output_descifradoVigenere.setReadOnly(True)
        boton_submitVigenere = QPushButton(text="Submit")
        boton_submitVigenere.setStyleSheet(submit_style)
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
            monofreq_out.setHorizontalHeaderLabels(["Letter", "Freq."])
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
            #if len(set(j for i,j in llave.items())) < 26:
            #    txt_out.setPlainText("Esta sustitución no es válida. La función de esta sustitución no es inyectiva. Por favor inténtelo de nuevo")
            #    return
            cypher = sb.substitution(txt_in.toPlainText().strip())
            cypher.permutar(llave)
            txt_out.setPlainText(str(cypher.permutado))
            #criptanalisisSus(txt_out)


class BlockScreen(QDialog):

    def __init__(self):
        super(BlockScreen, self).__init__()
        def BlockButton(input, output_ref, encriptar, cryptosys, op_mode):
            # Set sizes
            image_file_name = input.file
            img_name = image_file_name.split('.')[0]
            img_extension = image_file_name.split('.')[1]
            if image_file_name != "":
                img = cv2.imread(image_file_name)
                row, column, depth = img.shape
                # Check for minimum width
                minWidth = (16*2) // depth + 1
                if column < minWidth:
                    print('The minimum width of the image must be {} pixels, so that IV and padding can be stored in a single additional row!'.format(minWidth))
                    sys.exit()
                # Convert original image data to bytes
                imageBytes = img.tobytes()
                paddedSize = 0
                #img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                if encriptar == True:
                    ciphertext = ''
                    print("Flag1")
                    if cryptosys == 'DES':
                        keySize = 8
                        ivSize = 8
                        key = os.urandom(keySize)
                        iv = os.urandom(ivSize)
                        if op_mode == 'ECB':
                            print("Flag3")
                            cipher = DES.des(key, mode=ECB, IV=iv, pad=None, padmode=PAD_PKCS5)
                            print("Flag4")
                            ciphertext, paddedSize = cipher.encrypt(imageBytes)
                            print("Flag5")
                        elif op_mode == 'CBC':
                            print("Flag3")
                            cipher = DES.des(key, mode=CBC, IV=iv, pad=None, padmode = PAD_PKCS5)
                            print("Flag4")
                            ciphertext, paddedSize = cipher.encrypt(imageBytes)
                            print("Flag5")
                        elif op_mode == 'OFB':
                            ciphertext = cipher.encrypt_ofb(imageBytes, iv)
                        elif op_mode == 'CTR':
                            ciphertext = cipher.encrypt_ctr(imageBytes, iv)
                    elif cryptosys == 'AES':
                        keySize = 32
                        ivSize = 16
                        key = os.urandom(keySize)
                        iv = os.urandom(ivSize)
                        cipher = AES.AES(key)
                        if op_mode == 'ECB':
                            ciphertext, paddedSize = cipher.encrypt_ecb(imageBytes, iv, key)
                        elif op_mode == 'CBC':
                            print("Flag3")
                            ciphertext, paddedSize = cipher.encrypt_cbc(imageBytes, iv, key)
                            print("Flag4")
                        elif op_mode == 'OFB':
                            ciphertext = cipher.encrypt_ofb(imageBytes, iv)
                        elif op_mode == 'CTR':
                            ciphertext = cipher.encrypt_ctr(imageBytes, iv)
                    void = column * depth - ivSize - paddedSize
                    ivCiphertextVoid = iv + ciphertext + bytes(void)
                    imageEncrypted = np.frombuffer(ivCiphertextVoid, dtype = img.dtype).reshape(row + 1, column, depth)
                    cv2.imwrite(img_name+"_encrypted"+cryptosys+op_mode+".bmp", imageEncrypted)
                    key_file = open(img_name+"_key"+cryptosys+op_mode+".txt","wb")
                    key_file.write(key)
                    key_file.close()
                    QMessageBox.information(None, 'Success',
                                            'You can find the encrypted image here: ' + img_name+"_encrypted"+cryptosys+op_mode+".bmp"+"\n"+
                                            'And the key used in the file: '+img_name+"_key"+cryptosys+op_mode+".txt",
                                            QMessageBox.Ok)
                    output_ref.open_image(img_name+"_encrypted"+cryptosys+op_mode+".bmp")
                elif encriptar == False:
                    print("Flag1")
                    key_file = open(txt_key.text(),"rb")
                    key = key_file.read()
                    key_file.close()
                    rowOrig = row - 1
                    imageOrigBytesSize = rowOrig * column * depth
                    print("Flag2")
                    if cryptosys == 'DES':
                        keySize = 8
                        ivSize = 8
                        iv = imageBytes[:ivSize]
                        paddedSize = (imageOrigBytesSize // 8 + 1) * 8 - imageOrigBytesSize
                        encrypted = imageBytes[ivSize : ivSize + imageOrigBytesSize + paddedSize]
                        encrypted_nopad = imageBytes[ivSize : ivSize + imageOrigBytesSize]
                        if op_mode == 'ECB':
                            cipher = DES.des(key, mode=ECB, IV=iv, pad=None, padmode=PAD_PKCS5)
                            decryptedImageBytes = cipher.decrypt(encrypted)
                        elif op_mode == 'CBC':
                            cipher = DES.des(key, mode=CBC, IV=iv, pad=None, padmode=PAD_PKCS5)
                            decryptedImageBytes = cipher.decrypt(encrypted)
                        elif op_mode == 'OFB':
                            cipher = DES.des(key, mode=ECB, IV=iv, pad=None, padmode=PAD_PKCS5)
                            decryptedImageBytes = cipher.decrypt(encrypted_nopad, iv)
                        elif op_mode == 'CTR':
                            cipher = DES.des(key, mode=ECB, IV=iv, pad=None, padmode=PAD_PKCS5)
                            decryptedImageBytes = cipher.decrypt_ctr(encrypted_nopad, iv)
                    elif cryptosys == 'AES':
                        keySize = 32
                        ivSize = 16
                        iv = imageBytes[:ivSize]
                        paddedSize = (imageOrigBytesSize // 16 + 1) * 16 - imageOrigBytesSize
                        encrypted = imageBytes[ivSize : ivSize + imageOrigBytesSize + paddedSize]
                        encrypted_nopad = imageBytes[ivSize : ivSize + imageOrigBytesSize]
                        cipher = AES.AES(key)
                        if op_mode == 'ECB':
                            decryptedImageBytes = cipher.decrypt_ecb(encrypted, iv)
                        elif op_mode == 'CBC':
                            decryptedImageBytes = cipher.decrypt_cbc(encrypted, iv)
                        elif op_mode == 'OFB':
                            decryptedImageBytes = cipher.decrypt_ofb(encrypted_nopad, iv)
                        elif op_mode == 'CTR':
                            decryptedImageBytes = cipher.decrypt_ctr(encrypted_nopad, iv)
                    # Convert bytes to decrypted image data
                    decryptedImage = np.frombuffer(decryptedImageBytes, img.dtype).reshape(rowOrig, column, depth)
                    print("Flag8")
                    cv2.imwrite(img_name+"_decrypted.bmp", decryptedImage)
                    QMessageBox.information(None, 'Success',
                                            'You can find the decrypted image here: ' + img_name+"_decrypted.bmp",
                                            QMessageBox.Ok)
                    output_ref.open_image(img_name+"_decrypted.bmp")
            else:
                QMessageBox.critical(None, 'There is no image',
                                     'Drop an image to process or one with a valid format (.jpg, .png)',
                                     QMessageBox.Ok)

        gridBlock = QGridLayout()
        gridBlock.setGeometry(QtCore.QRect(10, 10, 1030, 600))
        h1box = QHBoxLayout()
        h2box = QVBoxLayout()
        txt_block = QLabel()
        txt_block.setText("Select Block Cipher: ")
        label_style = '''
        QLabel {
            font-size: 18px;
            font-family: Segoe UI;
        }'''
        txt_block.setStyleSheet(label_style)
        txt_block1 = QLabel()
        txt_block1.setText("Select Operation Mode: ")
        txt_block1.setStyleSheet(label_style)
        cripto_img = ["DES", "S-DES", "3-DES","AES"]
        op_modes = ["ECB","CBC","OFB","CTR"]
        combo_img = QComboBox()
        combo_modes = QComboBox()
        comboblock_style = """
        QComboBox {
            padding:5px;
            border:1px solid #161616;
            border-radius:3%;
            font-size: 18px;
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
        """
        combo_img.setStyleSheet(comboblock_style)
        combo_modes.setStyleSheet(comboblock_style)
        combo_img.addItems(cripto_img)
        combo_modes.addItems(op_modes)
        h1box.addWidget(txt_block)
        h1box.addWidget(combo_img)
        h2box.addWidget(txt_block1)
        h2box.addWidget(combo_modes)
        img_c = Template()
        img_d = Template()
        txt_img = QLabel()
        txt_img.setText("Image to encrypt / decrypted: ")
        txt_img.setAlignment(Qt.AlignCenter)
        txt_img.setStyleSheet('''
        QLabel {
            font-size: 22px;
            font-family: Segoe UI;
        }''')
        txt_img_d = QLabel()
        txt_img_d.setText("Image to decrypt / encrypted: ")
        txt_img_d.setAlignment(Qt.AlignCenter)
        txt_img_d.setStyleSheet('''
        QLabel {
            font-size: 22px;
            font-family: Segoe UI;
        }''')
        boton_cifrar_hill = crearBoton(cifrado=True)
        boton_descifrar_hill = crearBoton(cifrado=False)
        boton_cifrar_hill.clicked.connect(lambda: BlockButton(img_c, img_d, True, str(combo_img.currentText()), str(combo_modes.currentText())))
        boton_descifrar_hill.clicked.connect(lambda: BlockButton(img_d, img_c, False, str(combo_img.currentText()), str(combo_modes.currentText())))
        boton_limpiar = QPushButton(text="Clean")
        aux_style = """
        QPushButton {
            border-radius:5%;
            padding:5px;
            background:#9E6CFA;
            color:white;
        }
        QPushButton:hover {
            background-color:#4DB4FA;
            font: bold;
            }
            """
        boton_limpiar.setStyleSheet(aux_style)
        boton_limpiar.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        boton_limpiar.setFixedWidth(150)
        boton_limpiar.clicked.connect(lambda: clean(gridBlock, img_c, img_d, boton_cifrar_hill, boton_descifrar_hill))

        def clean(layout, img_c, img_d, boton_cifrar_hill, boton_descifrar_hill):
            txt_key.setText('')
            boton_cifrar_hill.setParent(None)
            boton_descifrar_hill.setParent(None)
            img_c.setParent(None)
            img_d.setParent(None)
            img_c = Template()
            img_d = Template()
            boton_cifrar_hill = crearBoton(cifrado=True)
            boton_descifrar_hill = crearBoton(cifrado=False)
            boton_cifrar_hill.clicked.connect(lambda: BlockButton(img_c, img_d, True, str(combo_img.currentText()), str(combo_modes.currentText())))
            boton_descifrar_hill.clicked.connect(lambda: BlockButton(img_d, img_c, False, str(combo_img.currentText()), str(combo_modes.currentText())))
            gridBlock.addWidget(img_c, 2, 0, 6, 1)
            gridBlock.addWidget(img_d, 2, 2, 6, 1)
            gridBlock.addWidget(boton_cifrar_hill, 3, 1)
            gridBlock.addWidget(boton_descifrar_hill, 4, 1)

        boton_browsekey = QPushButton(text="Key")
        boton_browsekey.setStyleSheet(aux_style)
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

        self.back_button = QPushButton("Back to Main Menu")
        back_buttonStyle = """
        QPushButton {
            width: 170px;
            border-radius: 5%;
            padding: 5px;
            background: #8DD3F6;
            font: 12pt;
            font: semi-bold;
        }
        QPushButton:hover {
            background-color: #4DB4FA;
            color: white;
        }
        """
        self.back_button.setStyleSheet(back_buttonStyle)
        self.back_button.clicked.connect(lambda: widget.setCurrentIndex(0))

        gridBlock.addLayout(h1box, 0, 0)
        gridBlock.addLayout(h2box, 0, 1)
        gridBlock.addWidget(combo_img, 0, 1)
        gridBlock.addWidget(txt_img, 1, 0)
        gridBlock.addWidget(txt_img_d, 1, 2)
        gridBlock.addWidget(img_c, 2, 0, 6, 1)
        gridBlock.addWidget(img_d, 2, 2, 6, 1)
        gridBlock.addWidget(boton_cifrar_hill, 3, 1)
        gridBlock.addWidget(boton_descifrar_hill, 4, 1)
        gridBlock.addWidget(boton_limpiar, 6, 1)
        gridBlock.addWidget(boton_key, 9, 0)
        gridBlock.addWidget(txt_key2, 10, 0)
        gridBlock.addWidget(boton_browsekey, 9, 2)
        gridBlock.addWidget(txt_key, 10, 2)
        gridBlock.addWidget(self.back_button, 11, 1)
        self.setLayout(gridBlock)

"""
Interfaz & Layout
"""
# Crea la ventana
app = QApplication(sys.argv)
app.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
welcome = WelcomeScreen()
clasicos = ClasicosScreen()
bloque = BlockScreen()
widget = QtWidgets.QStackedWidget()
widget.addWidget(welcome)
widget.addWidget(clasicos)
widget.addWidget(bloque)
widget.setFixedHeight(770)
widget.setFixedWidth(1200)
widget.setStyleSheet("background: #ffffff;")
widget.setWindowTitle("Criptool")
widget.setCurrentIndex(0)
widget.show()
font = QtGui.QFont()
font.setFamily("Segoe UI SemiLight")
font.setPointSize(10)
QApplication.setFont(font)
try:
    sys.exit(app.exec_())
except:
    print("Exiting")
