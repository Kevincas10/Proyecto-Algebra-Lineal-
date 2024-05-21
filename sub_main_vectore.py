from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import pyqtSignal

from restamatriz_windown import MainWindowResta
from sumamatriz_windown import MainWindowSuma


class MainWindowVectores(QtWidgets.QMainWindow):
    window_closed = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Operaciones con vectores")
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
        self.label.setText(
            "<html><head/><body><p align=\"center\"><span style=\" font-size:20pt; font-weight:700;\"> Operaciones con vectores. </span></p></body></html>")

        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(160, 200, 351, 281))

        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.matrices = self.create_button("Suma de vectores.", self.matrizsuma)
        self.verticalLayout.addWidget(self.matrices)

        self.inversa = self.create_button("Producto de vectores.", self.matrizresta)
        self.verticalLayout.addWidget(self.inversa)

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(60, 50, 91, 81))
        self.label_2.setPixmap(QtGui.QPixmap("logo.png"))
        self.label_2.setScaledContents(True)

    def closeEvent(self, event):
        self.window_closed.emit()
        super().closeEvent(event)

    def create_button(self, text, callback):
        button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        button.setStyleSheet(
            "height: 30px; background-color: #008080; color: white; border: 2px solid black; border-radius: 13px;")
        button.setText(text)
        button.clicked.connect(callback)
        return button

    def reopen_mainwindow(self):
        self.show()

    def matrizsuma(self):
        self.hide()
        self.matrizR = MainWindowSuma()
        self.matrizR.show()
        self.matrizR.window_closed.connect(self.reopen_mainwindow)

    def matrizresta(self):
        self.hide()
        self.matrizR = MainWindowResta()
        self.matrizR.show()
        self.matrizR.window_closed.connect(self.reopen_mainwindow)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindowVectores()
    mainWindow.show()
    sys.exit(app.exec())
