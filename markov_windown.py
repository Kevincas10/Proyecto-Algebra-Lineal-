import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QSpinBox, QGridLayout,
    QTextEdit, QMessageBox, QScrollArea, QHBoxLayout, QTableWidget, QTableWidgetItem
)
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt, pyqtSignal

import numpy as np



class MarkovInterface(QWidget):
    window_closed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Método de Markov")
        self.resize(800, 600)
        self.initUI()
        icon = QIcon("logo.png")
        self.setWindowIcon(icon)


    def initUI(self):
        # Logo en la parte superior izquierda
        logo_label = QLabel()
        pixmap = QPixmap("logo.png")
        pixmap_resized = pixmap.scaledToWidth(70)
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
        self.btn_calcular.setStyleSheet("background-color: #008080; color: white; border: 2px solid black;  border-radius: 3px")
        self.btn_calcular.clicked.connect(self.calcular_markov)

        self.btn_configurar_tablas = QPushButton("Configurar Tablas")
        self.btn_configurar_tablas.setStyleSheet("background-color: #008080; color: white; border: 2px solid black;  border-radius: 3px")
        self.btn_configurar_tablas.clicked.connect(self.configurar_tablas)

        self.table_transicion = QTableWidget()
        self.table_matriz = QTableWidget()

        self.resultados_layout = QVBoxLayout()
        self.resultados_texto = []
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        widget_interior = QWidget()
        widget_interior.setLayout(self.resultados_layout)
        self.scroll_area.setWidget(widget_interior)

        layout_controles_resultados = QGridLayout()
        layout_controles_resultados.addWidget(self.label_transicion, 0, 0)
        layout_controles_resultados.addWidget(self.spin_filas_transicion, 0, 1)
        layout_controles_resultados.addWidget(self.spin_columnas_transicion, 0, 2)
        layout_controles_resultados.addWidget(self.label_matriz, 1, 0)
        layout_controles_resultados.addWidget(self.spin_filas_matriz, 1, 1)
        layout_controles_resultados.addWidget(self.spin_columnas_matriz, 1, 2)
        layout_controles_resultados.addWidget(self.label_iteraciones, 2, 0)
        layout_controles_resultados.addWidget(self.spin_iteraciones, 2, 1)
        layout_controles_resultados.addWidget(self.btn_configurar_tablas, 3, 0, 1, 3)
        layout_controles_resultados.addWidget(self.table_transicion, 4, 0, 1, 3)
        layout_controles_resultados.addWidget(self.table_matriz, 5, 0, 1, 3)
        layout_controles_resultados.addWidget(self.btn_calcular, 6, 0, 1, 3)
        layout_controles_resultados.addWidget(self.scroll_area, 7, 0, 1, 3)

        layout_principal.addLayout(layout_controles_resultados)
        self.setLayout(layout_principal)

    def closeEvent(self, event):
        self.window_closed.emit()
        super().closeEvent(event)

    def configurar_tablas(self):
        filas_transicion = self.spin_filas_transicion.value()
        columnas_transicion = self.spin_columnas_transicion.value()
        self.table_transicion.setRowCount(filas_transicion)
        self.table_transicion.setColumnCount(columnas_transicion)

        filas_matriz = self.spin_filas_matriz.value()
        columnas_matriz = self.spin_columnas_matriz.value()
        self.table_matriz.setRowCount(filas_matriz)
        self.table_matriz.setColumnCount(columnas_matriz)

    def obtener_matriz(self, table):
        filas = table.rowCount()
        columnas = table.columnCount()
        matriz = np.zeros((filas, columnas))
        for i in range(filas):
            for j in range(columnas):
                item = table.item(i, j)
                if item and item.text():
                    try:
                        matriz[i, j] = float(item.text())
                    except ValueError:
                        QMessageBox.warning(self, "Valor inválido", f"Ingrese un número válido en la posición ({i+1}, {j+1}).")
                        return None
        return matriz

    def agregar_resultado(self, texto, resaltar=False):
        resultado_texto = QTextEdit()
        resultado_texto.setReadOnly(True)
        resultado_texto.setPlainText(texto)
        if resaltar:
            resultado_texto.setStyleSheet("background-color: #5353ec; color: white;")
        self.resultados_layout.addWidget(resultado_texto)
        self.resultados_texto.append(resultado_texto)

    def calcular_markov(self):
        transicion = self.obtener_matriz(self.table_transicion)
        if transicion is None:
            return

        matriz = self.obtener_matriz(self.table_matriz)
        if matriz is None:
            return

        iteraciones = self.spin_iteraciones.value()
        estado_actual = matriz

        for i in range(iteraciones):
            resultado = np.dot(transicion, estado_actual)
            texto_resultado = f"Iteración {i + 1}:\nMatriz Resultante:\n{resultado}"
            self.agregar_resultado(texto_resultado, resaltar=i == iteraciones - 1)
            estado_actual = resultado

        self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())
        QMessageBox.information(self, "Cálculo completado", "El cálculo del método de Markov ha finalizado.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MarkovInterface()
    window.show()
    sys.exit(app.exec())
