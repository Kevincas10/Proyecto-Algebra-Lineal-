import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QSpinBox, QGridLayout, QTextEdit, QMessageBox, QInputDialog, QScrollArea
from PyQt6.QtCore import Qt  # Importa la clase Qt

import numpy as np


class MarkovInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Método de Markov")
        self.resize(800, 600)  # Ajustar el tamaño de la ventana
        self.initUI()

    def initUI(self):
        self.label_transicion = QLabel("Tamaño de la matriz de transición (filas x columnas):")
        self.spin_filas_transicion = QSpinBox()
        self.spin_filas_transicion.setMinimum(1)
        self.spin_columnas_transicion = QSpinBox()
        self.spin_columnas_transicion.setMinimum(1)

        self.label_matriz = QLabel("Tamaño de la matriz a multiplicar en cada paso (filas x columnas):")
        self.spin_filas_matriz = QSpinBox()
        self.spin_filas_matriz.setMinimum(1)
        self.spin_columnas_matriz = QSpinBox()
        self.spin_columnas_matriz.setMinimum(1)

        self.label_iteraciones = QLabel("Número de iteraciones:")
        self.spin_iteraciones = QSpinBox()
        self.spin_iteraciones.setMinimum(1)

        self.btn_calcular = QPushButton("Calcular")
        self.btn_calcular.clicked.connect(self.calcular_markov)

        self.resultados_layout = QVBoxLayout()  # Layout para los resultados
        self.resultados_texto = []  # Lista para almacenar los widgets QTextEdit
        self.scroll_area = QScrollArea()  # Área de desplazamiento para los resultados
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)  # Scroll bar siempre visible

        widget_interior = QWidget()
        widget_interior.setLayout(self.resultados_layout)
        self.scroll_area.setWidget(widget_interior)

        layout = QGridLayout()
        layout.addWidget(self.label_transicion, 0, 0)
        layout.addWidget(self.spin_filas_transicion, 0, 1)
        layout.addWidget(self.spin_columnas_transicion, 0, 2)
        layout.addWidget(self.label_matriz, 1, 0)
        layout.addWidget(self.spin_filas_matriz, 1, 1)
        layout.addWidget(self.spin_columnas_matriz, 1, 2)
        layout.addWidget(self.label_iteraciones, 2, 0)
        layout.addWidget(self.spin_iteraciones, 2, 1)
        layout.addWidget(self.btn_calcular, 3, 0, 1, 3)
        layout.addWidget(self.scroll_area, 4, 0, 1, 3)

        self.setLayout(layout)

    def ingresar_matriz(self, filas, columnas, nombre_matriz):
        matriz = np.zeros((filas, columnas))
        for i in range(filas):
            for j in range(columnas):
                valor, ok = QInputDialog.getText(
                    self, f"Ingrese el elemento [{i + 1}, {j + 1}] de {nombre_matriz}",
                    f"Ingrese el elemento [{i + 1}, {j + 1}] de {nombre_matriz}:")
                if ok:
                    try:
                        valor_float = round(float(valor), 3)  # Convertir a float y redondear a 3 decimales
                        matriz[i, j] = valor_float
                    except ValueError:
                        QMessageBox.warning(self, "Valor inválido",
                                            "Ingrese un número válido.")
                        return None
                else:
                    return None
        return matriz

    def agregar_resultado(self, texto):
        resultado_texto = QTextEdit()
        resultado_texto.setReadOnly(True)
        resultado_texto.setPlainText(texto)
        self.resultados_layout.addWidget(resultado_texto)
        self.resultados_texto.append(resultado_texto)

    def calcular_markov(self):
        filas_transicion = self.spin_filas_transicion.value()
        columnas_transicion = self.spin_columnas_transicion.value()
        transicion = self.ingresar_matriz(filas_transicion, columnas_transicion, "la matriz de transición")

        filas_matriz = self.spin_filas_matriz.value()
        columnas_matriz = self.spin_columnas_matriz.value()
        matriz = self.ingresar_matriz(filas_matriz, columnas_matriz, "la matriz a multiplicar en cada paso")

        iteraciones = self.spin_iteraciones.value()

        estado_actual = matriz
        self.agregar_resultado("Método de Markov:")
        for i in range(iteraciones):
            resultado = np.dot(transicion, estado_actual)
            texto_resultado = f"Iteración {i + 1}:\nMatriz Resultante:\nFilas x Columnas: {resultado.shape[0]} x {resultado.shape[1]}\n{resultado}"
            self.agregar_resultado(texto_resultado)
            estado_actual = resultado

        self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())
        QMessageBox.information(self, "Cálculo completado", "El cálculo del método de Markov ha finalizado.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MarkovInterface()
    window.show()
    sys.exit(app.exec())
