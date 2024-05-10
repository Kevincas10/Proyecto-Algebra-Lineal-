import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QTextEdit, QMessageBox, QInputDialog
from PyQt6.QtCore import Qt

def sumar_matrices(matriz1, matriz2):
    if len(matriz1) != len(matriz2) or len(matriz1[0]) != len(matriz2[0]):
        return None  # Las matrices no tienen las mismas dimensiones
    resultado = []
    pasos = []
    for i in range(len(matriz1)):
        fila = []
        paso = []
        for j in range(len(matriz1[0])):
            suma = matriz1[i][j] + matriz2[i][j]
            fila.append(suma)
            paso.append(f"{matriz1[i][j]} + {matriz2[i][j]} = {suma}")
        resultado.append(fila)
        pasos.append(paso)
    return resultado, pasos

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Suma de Matrices")
        self.setGeometry(100, 100, 600, 400)  # Se aumentó el tamaño de la ventana

        self.create_widgets()
        self.layout_widgets()

        self.matriz_a = []
        self.matriz_b = []

    def create_widgets(self):
        self.label_titulo = QLabel("<h2>Suma de Matrices</h2>")
        self.label_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label_filas = QLabel("Número de filas:")
        self.input_filas = QLineEdit()

        self.label_columnas = QLabel("Número de columnas:")
        self.input_columnas = QLineEdit()

        self.button_matriz_a = QPushButton("Ingresar Matriz A")
        self.button_matriz_a.setStyleSheet("background-color: #2196F3; color: white;")  # Color azul
        self.button_matriz_b = QPushButton("Ingresar Matriz B")
        self.button_matriz_b.setStyleSheet("background-color: #2196F3; color: white;")  # Color azul
        self.button_matriz_b.setEnabled(False)

        self.button_calcular = QPushButton("Calcular")
        self.button_calcular.setStyleSheet("background-color: #2196F3; color: white;")  # Color azul
        self.button_calcular.setEnabled(False)

        self.label_resultado = QLabel("<h3>Resultado de la suma:</h3>")
        self.label_resultado.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.textedit_resultado = QTextEdit()
        self.textedit_resultado.setReadOnly(True)

    def layout_widgets(self):
        layout_principal = QVBoxLayout()

        layout_principal.addWidget(self.label_titulo)

        layout_filas = QHBoxLayout()
        layout_filas.addWidget(self.label_filas)
        layout_filas.addWidget(self.input_filas)

        layout_columnas = QHBoxLayout()
        layout_columnas.addWidget(self.label_columnas)
        layout_columnas.addWidget(self.input_columnas)

        layout_botones = QHBoxLayout()
        layout_botones.addWidget(self.button_matriz_a)
        layout_botones.addWidget(self.button_matriz_b)
        layout_botones.addWidget(self.button_calcular)

        layout_resultado = QVBoxLayout()
        layout_resultado.addWidget(self.label_resultado)
        layout_resultado.addWidget(self.textedit_resultado)

        layout_principal.addLayout(layout_filas)
        layout_principal.addLayout(layout_columnas)
        layout_principal.addLayout(layout_botones)
        layout_principal.addLayout(layout_resultado)

        self.setLayout(layout_principal)

        self.button_matriz_a.clicked.connect(self.ingresar_matriz_a)
        self.button_matriz_b.clicked.connect(self.ingresar_matriz_b)
        self.button_calcular.clicked.connect(self.calcular_suma)

    def ingresar_matriz_a(self):
        filas = int(self.input_filas.text())
        columnas = int(self.input_columnas.text())

        self.matriz_a = []
        for i in range(filas):
            fila = []
            for j in range(columnas):
                valor, ok = QInputDialog.getDouble(self, f"Matriz A [{i+1},{j+1}]", f"Ingrese el elemento [{i+1},{j+1}] de la Matriz A:")
                if not ok:
                    return
                fila.append(valor)
            self.matriz_a.append(fila)

        self.button_matriz_a.setEnabled(False)
        self.button_matriz_b.setEnabled(True)

    def ingresar_matriz_b(self):
        filas = int(self.input_filas.text())
        columnas = int(self.input_columnas.text())

        self.matriz_b = []
        for i in range(filas):
            fila = []
            for j in range(columnas):
                valor, ok = QInputDialog.getDouble(self, f"Matriz B [{i+1},{j+1}]", f"Ingrese el elemento [{i+1},{j+1}] de la Matriz B:")
                if not ok:
                    return
                fila.append(valor)
            self.matriz_b.append(fila)

        self.button_matriz_b.setEnabled(False)
        self.button_calcular.setEnabled(True)

    def calcular_suma(self):
        resultado, pasos = sumar_matrices(self.matriz_a, self.matriz_b)
        if resultado:
            resultado_texto = ""
            for paso in pasos:
                resultado_texto += ", ".join(paso) + "\n"
            resultado_texto += "\nResultado de la suma:\n"
            for fila in resultado:
                resultado_texto += str(fila) + "\n"
            self.textedit_resultado.setText(resultado_texto)
        else:
            self.textedit_resultado.setText("Las matrices no tienen las mismas dimensiones y no se pueden sumar.")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
