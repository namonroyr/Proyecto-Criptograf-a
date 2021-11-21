import sys
import math
import numpy as np
import cv2
from egcd import egcd
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage, QPalette, QBrush, QColor
from PyQt5.QtCore import (Qt, QFile, QDate, QTime, QSize, QTimer, QRect, QRegExp, QTranslator,
                          QLocale, QLibraryInfo)
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget,  QGridLayout, QLabel, QDialog, QTableWidget, QMenu,
                             QTableWidgetItem, QAbstractItemView, QLineEdit, QPushButton, QTabWidget,
                             QActionGroup, QAction, QMessageBox, QFrame, QStyle, QGridLayout,
                             QVBoxLayout, QHBoxLayout, QLabel, QToolButton, QGroupBox,
                             QDateEdit, QComboBox, QPushButton, QVBoxLayout, QFileDialog, QPlainTextEdit, QLineEdit)
from PyQt5.QtGui import (QFont, QIcon, QPalette, QBrush, QColor, QPixmap, QRegion, QClipboard,
                         QRegExpValidator)
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QCursor
import hill

abc = {"A" : 0, "B" : 1, "C" : 2, "D" : 3, "E" : 4, "F" : 5, "G" : 6, "H" : 7, "I" : 8, "J" : 9, "K" : 10,
        "L" : 11, "M" : 12, "N" : 13, "O" : 14, "P" : 15, "Q" : 16, "R" : 17, "S" : 18, "T" : 19, "U" : 20,
        "V" : 21, "W" : 22, "X" : 23, "Y" : 24, "Z" : 25}
inv_abc = {value:key for key, value in abc.items()}

criptosistemas = ["Criptosistema Afín", "Criptosistema por Desplazamiento", "Criptosistema por Sustitución", "Criptosistema por Permutación",
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

class PhotoLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAlignment(Qt.AlignCenter)
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
        grid = QGridLayout(self)
        grid.addWidget(self.photo, 0, 0)
        self.setAcceptDrops(True)
        self.resize(300, 450)

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
    file_ext = ['jpg','png']
    if image_file_name != "" and img_extension in file_ext:
        img, original_shape = read_image(image_file_name)
        criptosistema_Hill = hill.Hill(img)
        if encriptar == True:
            img_enc_vec = criptosistema_Hill.encriptar(img[0])
            encoded_img = img_enc_vec.reshape(original_shape)
            # writing encrypted data in image
            encoded_img_name = '{0}-encoded.{1}'.format(img_name, img_extension)
            print(encoded_img_name)
            encoded_img.astype(np.uint8)
            cv2.imwrite(encoded_img_name, encoded_img)
            QMessageBox.information(None, 'Éxito', 'Encriptación realizada, puede encrontrar la imagen encriptada en: '+encoded_img_name, QMessageBox.Ok)
        #elif encriptar == False:
            #criptosistema_Hill.desencriptar(input, output)
    else:
        QMessageBox.critical(None, 'Imagen no ingresada', 'Arrastre una imagen para procesar o ingrese una imagen con formato válido (.jpg, .png)', QMessageBox.Ok)

def crearBoton(cifrado):
    if cifrado:
        boton = QPushButton(text = "Cifrar")
    else:
        boton = QPushButton(text = "Descifrar")
    boton.setStyleSheet(
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
        """
    )
    boton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    boton.setFixedWidth(150)
    return boton

def limpiarCampos():
    res_clave.setText("")
    for i in [input_aCifrar, input_aDescifrar, output_cifrado, output_descifrado]:
        i.setPlainText("")

def read_image(image_path):
    """ Read an image and return a one hot vector of the image"""
    img = cv2.imread(image_path, 0)
    print(img)
    reshape_value = 1
    for i in img.shape:
        reshape_value *= i
    return img.reshape((1, reshape_value)), img.shape

def escogerCriptosistema():
    if str(menu.currentText()) == "Criptosistema Afín":
        # Clave afin
        for i in reversed(range(1,gridcifrado.count())):
            gridcifrado.itemAt(i).widget().deleteLater()
        txt_clave_afin = QLabel()
        txt_clave_afin.setText("Ingrese los dos digitos de la clave afin separados por un espacio:")
        res_clave_afin = QLineEdit()
        res_clave_afin.setStyleSheet("padding:5px;border:1px solid #161616;border-radius:3%;")
        res_clave_afin.setText("")
        for i in [input_aCifrar, input_aDescifrar, output_cifrado, output_descifrado]:
            i.setPlainText("")
        boton_cifrar = crearBoton(cifrado = True)
        boton_descifrar = crearBoton(cifrado = False)
        boton_cifrar.clicked.connect(lambda : botonAfin(res_clave.text().split(), input_aCifrar, output_cifrado, True))
        boton_descifrar.clicked.connect(lambda : botonAfin(res_clave.text().split(), input_aDescifrar, output_descifrado, False))
        gridcifrado.addWidget(txt_clave_afin, 1, 0)
        gridcifrado.addWidget(res_clave_afin, 2, 0)
        gridcifrado.addWidget(boton_descifrar, 7, 1)
        gridcifrado.addWidget(boton_cifrar, 7, 0)

    elif str(menu.currentText()) == "Criptosistema por Desplazamiento":
        # Clave por desplazamiento
        txt_clave.setText("Ingrese el digito de la clave por Desplazamiento:")
        res_clave.setText("")
        for i in [input_aCifrar, input_aDescifrar, output_cifrado, output_descifrado]:
            i.setPlainText("")
        boton_cifrar = crearBoton(cifrado = True)
        boton_descifrar = crearBoton(cifrado = False)
        boton_cifrar.clicked.connect(lambda : botonDesplazamiento(res_clave.text(), input_aCifrar, output_cifrado, True))
        boton_descifrar.clicked.connect(lambda : botonDesplazamiento(res_clave.text(), input_aDescifrar, output_descifrado, False))
        gridcifrado.addWidget(boton_descifrar, 7, 1)
        gridcifrado.addWidget(boton_cifrar, 7, 0)

    elif str(menu.currentText()) == "Criptosistema por Permutación":
        txt_clave.setText("Ingrese los digitos de la matriz de permutación separados por un espacio:")
        limpiarCampos()
        boton_cifrar = crearBoton(cifrado = True)
        boton_descifrar = crearBoton(cifrado = False)
        boton_cifrar.clicked.connect(lambda : botonPermutacion([len(res_clave.text().split()), res_clave.text()], input_aCifrar, output_cifrado, True))
        boton_descifrar.clicked.connect(lambda : botonPermutacion([len(res_clave.text().split()), res_clave.text()], input_aDescifrar, output_descifrado, False))
        gridcifrado.addWidget(boton_descifrar, 7, 1)
        gridcifrado.addWidget(boton_cifrar, 7, 0)


# Crea la ventana
app = QApplication(sys.argv)
app.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
window = QtWidgets.QMainWindow()
window.setWindowTitle("CriptoTool")
window.setFixedWidth(1100)
window.setFixedHeight(735)
#window.setStyleSheet("background: #ffffff;")

font = QtGui.QFont()
font.setFamily("Segoe UI SemiLight")
font.setPointSize(10)
QApplication.setFont(font)
#### Añade todos los elementos ####
#Tab
tabWidget = QtWidgets.QTabWidget(window)
tabWidget.setGeometry(QtCore.QRect(25, 55, 1050, 650))
tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
tabWidget.setObjectName("tabWidget")
cifrado = QtWidgets.QWidget()
tabWidget.addTab(cifrado, "Cifrado/Descifrado")
gridcifrado = QGridLayout(cifrado)
gridcifrado.setGeometry(QtCore.QRect(10, 10, 1030, 600))
#------------------Hill----------------------------------
Hill = QtWidgets.QWidget()
tabWidget.addTab(Hill, "Hill - Imagen")
gridHill = QGridLayout(Hill)
gridHill.setGeometry(QtCore.QRect(10, 10, 1030, 600))
img_c = Template()
gridHill.addWidget(img_c, 1, 0, 3, 1)
img_d = Template()
gridHill.addWidget(img_d, 1, 2, 3, 1)
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
#txt_result.setText("El resultado de su imagen aparece aquí: ")
boton_cifrar = crearBoton(cifrado = True)
boton_descifrar = crearBoton(cifrado = False)
boton_cifrar.clicked.connect(lambda : botonHill(img_c, True))
boton_descifrar.clicked.connect(lambda : botonHill(img_d, True))
boton_limpiar = QPushButton(text = "Limpiar")
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
"""
)
boton_limpiar.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
boton_limpiar.setFixedWidth(150)
boton_limpiar.clicked.connect(lambda: clean(gridHill))
def clean(layout):
    layout.itemAt(0).widget().deleteLater()
    layout.itemAt(1).widget().deleteLater()
    img_c = Template()
    img_d = Template()
    gridHill.addWidget(img_c, 1, 0, 3, 1)
    gridHill.addWidget(img_d, 1, 2, 3, 1)

gridHill.addWidget(txt_img, 0, 0)
gridHill.addWidget(txt_img_d, 0, 2)
gridHill.addWidget(boton_descifrar, 1, 1, -1, 1)
gridHill.addWidget(boton_cifrar, 0, 1, -1, 1)
gridHill.addWidget(boton_limpiar, 2, 1, -1, 1)

criptanalysis = QtWidgets.QWidget()
tabWidget.addTab(criptanalysis, "Criptanálisis")
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
tabWidget.setCurrentIndex(0)
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
menuSalir = QtWidgets.QMenu(menubar)
window.setMenuBar(menubar)
menuClasicos.setTitle("Criptosistemas CLÁSICOS")
menuBloque.setTitle("DE BLOQUE")
menuClaveP.setTitle("CLAVE PÚBLICA")
menuSalir.setTitle("Salir")
menubar.addAction(menuClasicos.menuAction())
menubar.addAction(menuBloque.menuAction())
menubar.addAction(menuClaveP.menuAction())
menubar.addAction(menuSalir.menuAction())

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

"""
#grid = QGridLayout()
#grid.addWidget(menu, 0, 0)

#grid.addWidget(txt_clave, 1, 0)
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

#window.setLayout(grid)
"""
window.show()
sys.exit(app.exec())
