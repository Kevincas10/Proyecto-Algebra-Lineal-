import sys
import numpy as np
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QGridLayout, QTextEdit
from PyQt6.QtCore import Qt, pyqtSignal

# Global lists to hold text conversion and key matrix
lis = []
llave = []

# Letter to number mappings
mapping = {
    'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8,
    'i': 9, 'j': 10, 'k': 11, 'l': 12, 'm': 13, 'n': 14, 'ñ': 15,
    'o': 16, 'p': 17, 'q': 18, 'r': 19, 's': 20, 't': 21, 'u': 22,
    'v': 23, 'w': 24, 'x': 25, 'y': 26, 'z': 27, ' ': 28, '0': 29,
    '1': 30, '2': 31, '3': 32, '4': 33,  '5': 34, '6': 35, '7': 36,
    '8': 37, '9': 38
}


def convertir(texto):
    lis.clear()
    for letra in texto:
        lis.append(mapping.get(letra.lower(), 'Opción Incorrecta!'))
    size()


def size():
    while len(lis) % 3 != 0:
        lis.append(28)


def matriz_inversa(matriz):
    try:
        inversa = np.linalg.inv(matriz)
        return inversa
    except np.linalg.LinAlgError:
        print("La matriz no es invertible.")


class CifradoApp(QWidget):
    window_closed = pyqtSignal()
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Cifrado de Texto')
        self.setGeometry(100, 100, 600, 400)  # Aumenta el tamaño de la ventana
        icon = QIcon("logo.png")
        self.setWindowIcon(icon)

        layout = QVBoxLayout()

        # Create a horizontal layout for the title and logo
        title_layout = QHBoxLayout()
        logo_label = QLabel(self)
        logo_pixmap = QPixmap("logo.png")
        logo_label.setPixmap(logo_pixmap.scaled(30, 30, Qt.AspectRatioMode.KeepAspectRatio))
        title_label = QLabel('Cifrado de Texto', self)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-left: 10px;")

        title_layout.addWidget(logo_label)
        title_layout.addWidget(title_label)
        title_layout.addStretch()

        layout.addLayout(title_layout)

        self.text_input = QLineEdit(self)
        self.text_input.setPlaceholderText('Ingrese el texto que desee cifrar')
        layout.addWidget(self.text_input)

        self.matrix_input = QGridLayout()
        self.matrix_labels = [[QLineEdit(self) for _ in range(3)] for _ in range(3)]

        for i in range(3):
            for j in range(3):
                self.matrix_input.addWidget(self.matrix_labels[i][j], i, j)

        layout.addLayout(self.matrix_input)

        self.encrypt_button = QPushButton('Cifrar Texto', self)
        self.encrypt_button.setStyleSheet(
            "height: 30px; background-color: #008080; color: white; border: 2px solid black; border-radius: 13px;")
        self.encrypt_button.clicked.connect(self.cifrar_texto)
        layout.addWidget(self.encrypt_button)

        self.result_output = QTextEdit(self)
        self.result_output.setReadOnly(True)
        layout.addWidget(self.result_output)

        self.setLayout(layout)
        self.center_window()

    def closeEvent(self, event):
        self.window_closed.emit()
        super().closeEvent(event)

    def cifrar_texto(self):
        texto = self.text_input.text()
        convertir(texto)

        llave.clear()
        for i in range(3):
            fila = []
            for j in range(3):
                try:
                    elemento = float(self.matrix_labels[i][j].text())
                except ValueError:
                    self.result_output.setText("Todos los elementos de la matriz deben ser números.")
                    return
                fila.append(elemento)
            llave.append(fila)

        llave_np = np.array(llave)
        num_columnas = -(-len(lis) // 3)
        matriz = np.zeros((3, num_columnas))

        for il, valor in enumerate(lis):
            fila = il % 3
            columna = il // 3
            matriz[fila, columna] = valor

        # Mostrar el proceso de cifrado
        procedimiento = f'Texto convertido a números:\n{lis}\n\n'
        procedimiento += f'Matriz de texto antes del cifrado:\n{matriz}\n\n'
        procedimiento += f'Matriz de llave:\n{llave_np}\n\n'

        matrizc = np.dot(llave_np, matriz)
        procedimiento += f'Matriz cifrada:\n{matrizc}\n\n'

        matriz_inversa_np = matriz_inversa(llave_np)
        if matriz_inversa_np is None:
            procedimiento += "La matriz de llave no es invertible.\n"
            self.result_output.setText(procedimiento)
        else:
            matriz_original = np.dot(matriz_inversa_np, matrizc)
            procedimiento += f'Matriz inversa de la llave:\n{matriz_inversa_np}\n\n'
            procedimiento += f'Matriz descifrada (texto original):\n{matriz_original}\n\n'

            # Convertir la matriz descifrada de vuelta a texto
            texto_descifrado = []
            for i in range(matriz_original.shape[1]):
                for j in range(3):
                    valor = round(matriz_original[j, i])
                    letra = next((k for k, v in mapping.items() if v == valor), '?')
                    texto_descifrado.append(letra)
            procedimiento += f'Texto descifrado:\n{"".join(texto_descifrado).strip()}\n'

            self.result_output.setText(procedimiento)

    def center_window(self):
        screen_geometry = QApplication.primaryScreen().geometry()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_geometry.center())
        self.move(window_geometry.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CifradoApp()
    ex.show()
    sys.exit(app.exec())
