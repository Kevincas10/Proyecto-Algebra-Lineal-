from PyQt6 import QtCore, QtGui, QtWidgets
from markov_windown import MarkovInterface


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Calculadora Algebra Lineal")
        MainWindow.resize(700, 600)
        font = QtGui.QFont()
        font.setBold(False)
        MainWindow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("logo.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        MainWindow.setWindowIcon(icon)

        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(150, 20, 391, 141))
        self.label.setObjectName("label")

        self.verticalLayoutWidget = QtWidgets.QWidget(parent=self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(160, 200, 351, 281))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.matrices = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.matrices.setEnabled(True)
        self.matrices.setStyleSheet("height: 30px; background-color: #33FFC7; color: black; border: 2x solid black; border-radius: 13px;")
        self.matrices.setObjectName("matrices")
        self.matrices.clicked.connect(self.matriz)
        self.verticalLayout.addWidget(self.matrices)

        self.inversa = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.inversa.setStyleSheet("height: 30px; background-color: #33FFC7; color: black; border: 2x solid black; border-radius: 13px;")
        self.inversa.setObjectName("inversa")
        self.inversa.clicked.connect(self.matriz_inversa)
        self.verticalLayout.addWidget(self.inversa)

        self.determinante = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.determinante.setStyleSheet("height: 30px; background-color: #33FFC7; color: black; border: 2x solid black; border-radius: 13px;")
        self.determinante.setObjectName("determinante")
        self.determinante.clicked.connect(self.determinantes)
        self.verticalLayout.addWidget(self.determinante)

        self.rango = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.rango.setStyleSheet("height: 30px; background-color: #33FFC7; color: black; border: 2x solid black; border-radius: 13px;")
        self.rango.setObjectName("rango")
        self.rango.clicked.connect(self.rangos)
        self.verticalLayout.addWidget(self.rango)

        self.cifrado = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.cifrado.setStyleSheet("height: 30px; background-color: #33FFC7; color: black; border: 2x solid black; border-radius: 13px;")
        self.cifrado.setObjectName("cifrado")
        self.cifrado.clicked.connect(self.cifrados)
        self.verticalLayout.addWidget(self.cifrado)

        self.cadena = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.cadena.setStyleSheet("height: 30px; background-color: #33FFC7; color: black; border: 2x solid black; border-radius: 13px;")
        self.cadena.setObjectName("Cadenas de Markov")
        self.cadena.clicked.connect(self.cadenasM)
        self.verticalLayout.addWidget(self.cadena)

        self.vectores = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.vectores.setStyleSheet("height: 30px; background-color: #33FFC7; color: black; border: 2x solid black; border-radius: 13px;")
        self.vectores.setObjectName("vectores")
        self.vectores.clicked.connect(self.vectoresO)
        self.verticalLayout.addWidget(self.vectores)

        self.label_2 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(60, 50, 91, 81))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("logo.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def reopen_mainwindow(self):
        self.show()

    def matriz(self):
        print('funciones entre matrices.')

    def matriz_inversa(self):
        print('Matriz inversa')

    def determinantes(self):
        print('Determinante.')

    def rangos(self):
        print('Rango de una matriz')


    def cifrados(self):
        print('cifrado')

    def cadenasM(self):
        self.hide()
        self.cadenasMarkov = MarkovInterface()
        self.cadenasMarkov.show()
        self.cadenasMarkov.window_closed.connect(self.reopen_mainwindow)

    def vectoresO(self):
        print('Operaciones entre vectores.')

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:20pt; font-weight:700;\">Programa Algebra Lineal. </span></p></body></html>"))
        self.matrices.setText(_translate("MainWindow", "Funciones entre Matrices"))
        self.inversa.setText(_translate("MainWindow", "Matriz Inversa"))
        self.determinante.setText(_translate("MainWindow", "Determinante de una Matriz "))
        self.rango.setText(_translate("MainWindow", "Rango de una matriz."))
        self.cifrado.setText(_translate("MainWindow", "Cifrado por matrices."))
        self.cadena.setText(_translate("MainWindow", "Cadenas de Markov"))
        self.vectores.setText(_translate("MainWindow", "Operaciones con vectores "))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
