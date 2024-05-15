from PyQt6 import QtCore, QtGui, QtWidgets
from markov_windown import MarkovInterface


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Calculadora Algebra Lineal")
        self.resize(700, 600)
        font = QtGui.QFont()
        font.setBold(False)
        self.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("logo.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.setWindowIcon(icon)

        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(150, 20, 391, 141))
        self.label.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:20pt; font-weight:700;\">Programa Algebra Lineal. </span></p></body></html>")

        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(160, 200, 351, 281))

        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.matrices = self.create_button("Funciones entre Matrices", self.matriz)
        self.verticalLayout.addWidget(self.matrices)

        self.inversa = self.create_button("Matriz Inversa", self.matriz_inversa)
        self.verticalLayout.addWidget(self.inversa)

        self.determinante = self.create_button("Determinante de una Matriz", self.determinantes)
        self.verticalLayout.addWidget(self.determinante)

        self.rango = self.create_button("Rango de una matriz", self.rangos)
        self.verticalLayout.addWidget(self.rango)

        self.cifrado = self.create_button("Cifrado por matrices", self.cifrados)
        self.verticalLayout.addWidget(self.cifrado)

        self.cadena = self.create_button("Cadenas de Markov", self.cadenasM)
        self.verticalLayout.addWidget(self.cadena)

        self.vectores = self.create_button("Operaciones con vectores", self.vectoresO)
        self.verticalLayout.addWidget(self.vectores)

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(60, 50, 91, 81))
        self.label_2.setPixmap(QtGui.QPixmap("logo.png"))
        self.label_2.setScaledContents(True)

    def create_button(self, text, callback):
        button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        button.setStyleSheet("height: 30px; background-color: #33FFC7; color: black; border: 2px solid black; border-radius: 13px;")
        button.setText(text)
        button.clicked.connect(callback)
        return button

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


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())
