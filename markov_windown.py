import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QSpinBox, QGridLayout, QTextEdit, \
    QMessageBox, QInputDialog, QScrollArea, QHBoxLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt  # Importa la clase Qt

import numpy as np


class MarkovInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Método de Markov")
        self.resize(800, 600)  # Ajustar el tamaño de la ventana
        self.initUI()

    def initUI(self):
        # Logo en la parte superior izquierda
        logo_label = QLabel()
        pixmap = QPixmap("logo.jpeg")  # Ruta a tu archivo de imagen
        pixmap_resized = pixmap.scaledToWidth(70)  # Redimensiona el logo al ancho deseado (100 en este ejemplo)
        logo_label.setPixmap(pixmap_resized)

        # Título centrado y en negrita
        x = QLabel("")
        self.label_titulo = QLabel("<h1><b>Método de Markov</b></h1>")
        self.label_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Layout para el título y el logo
        layout_titulo_logo = QHBoxLayout()
        layout_titulo_logo.addWidget(logo_label)
        layout_titulo_logo.addWidget(x)
        layout_titulo_logo.addWidget(self.label_titulo)
        layout_titulo_logo.addWidget(x)
        layout_titulo_logo.addWidget(x)

        # Layout principal
        layout_principal = QVBoxLayout()

        layout_principal.addLayout(layout_titulo_logo)

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
        self.btn_calcular.setStyleSheet(
            "background-color: blue; color: white;")  # Cambia el color del botón a azul y el texto a blanco
        self.btn_calcular.clicked.connect(self.calcular_markov)

        self.resultados_layout = QVBoxLayout()  # Layout para los resultados
        self.resultados_texto = []  # Lista para almacenar los widgets QTextEdit
        self.scroll_area = QScrollArea()  # Área de desplazamiento para los resultados
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)  # Scroll bar siempre visible

        widget_interior = QWidget()
        widget_interior.setLayout(self.resultados_layout)
        self.scroll_area.setWidget(widget_interior)

        # Layout para los controles y resultados
        layout_controles_resultados = QGridLayout()
        layout_controles_resultados.addWidget(self.label_transicion, 0, 0)
        layout_controles_resultados.addWidget(self.spin_filas_transicion, 0, 1)
        layout_controles_resultados.addWidget(self.spin_columnas_transicion, 0, 2)
        layout_controles_resultados.addWidget(self.label_matriz, 1, 0)
        layout_controles_resultados.addWidget(self.spin_filas_matriz, 1, 1)
        layout_controles_resultados.addWidget(self.spin_columnas_matriz, 1, 2)
        layout_controles_resultados.addWidget(self.label_iteraciones, 2, 0)
        layout_controles_resultados.addWidget(self.spin_iteraciones, 2, 1)
        layout_controles_resultados.addWidget(self.btn_calcular, 3, 0, 1, 3)
        layout_controles_resultados.addWidget(self.scroll_area, 4, 0, 1, 3)

        layout_principal.addLayout(layout_controles_resultados)

        self.setLayout(layout_principal)

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

    def agregar_resultado(self, texto, resaltar=False):
        resultado_texto = QTextEdit()
        resultado_texto.setReadOnly(True)
        resultado_texto.setPlainText(texto)
        if resaltar:  # Resaltar en color personalizado si es la última iteración
            resultado_texto.setStyleSheet(
                "background-color: #5353ec; color: white;")  # Fondo en #5353ec, letras blancas
        self.resultados_layout.addWidget(resultado_texto)
        self.resultados_texto.append(resultado_texto)

    def calcular_markov(self):
        filas_transicion = self.spin_filas_transicion.value()
        columnas_transicion = self.spin_columnas_transicion.value()

        # Verificar si se ha ingresado la matriz de transición antes de solicitar los valores de las matrices
        if filas_transicion == 0 or columnas_transicion == 0:
            QMessageBox.warning(self, "Datos faltantes", "Ingrese primero la matriz de transición.")
            return

        transicion = self.ingresar_matriz(filas_transicion, columnas_transicion, "la matriz de transición")

        filas_matriz = self.spin_filas_matriz.value()
        columnas_matriz = self.spin_columnas_matriz.value()
        matriz = self.ingresar_matriz(filas_matriz, columnas_matriz, "la matriz a multiplicar en cada paso")

        iteraciones = self.spin_iteraciones.value()

        estado_actual = matriz
        for i in range(iteraciones):
            resultado = np.dot(transicion, estado_actual)
            texto_resultado = f"Iteración {i + 1}:\nMatriz Resultante:\n{resultado}"
            self.agregar_resultado(texto_resultado, resaltar=i == iteraciones - 1)  # Resaltar la última iteración
            estado_actual = resultado

        self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())
        QMessageBox.information(self, "Cálculo completado", "El cálculo del método de Markov ha finalizado.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MarkovInterface()
    window.show()
    sys.exit(app.exec())
