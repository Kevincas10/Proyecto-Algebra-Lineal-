import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QTextEdit, QMessageBox
from PyQt6.QtCore import Qt


class MatrixInputWidget(QWidget):
    def __init__(self, rows, cols):  # Corregido: __init__ en lugar de _init_
        super().__init__()

        self.rows = rows
        self.cols = cols
        self.create_widgets()
        self.layout_widgets()

    def create_widgets(self):
        self.labels = []
        self.inputs = []
        for i in range(self.rows):
            row_labels = []
            row_inputs = []
            for j in range(self.cols):
                label = QLabel(f"({i + 1}, {j + 1})")
                input_box = QLineEdit()
                row_labels.append(label)
                row_inputs.append(input_box)
            self.labels.append(row_labels)
            self.inputs.append(row_inputs)

    def layout_widgets(self):
        layout = QVBoxLayout()

        for i in range(self.rows):
            hbox = QHBoxLayout()
            for j in range(self.cols):
                hbox.addWidget(self.labels[i][j])
                hbox.addWidget(self.inputs[i][j])
            layout.addLayout(hbox)

        self.setLayout(layout)

    def get_matrix_data(self):
        matrix_data = []
        for i in range(self.rows):
            row_data = []
            for j in range(self.cols):
                value = self.inputs[i][j].text()
                try:
                    value = float(value)
                except ValueError:
                    QMessageBox.warning(self, "Error", "Por favor ingrese solo números en la matriz.")
                    return None
                row_data.append(value)
            matrix_data.append(row_data)
        return matrix_data


class MainWindow(QWidget):
    def __init__(self):  # Corregido: __init__ en lugar de _init_
        super().__init__()

        self.setWindowTitle("Multiplicación de Matrices")
        self.setGeometry(100, 100, 800, 600)

        self.create_widgets()
        self.layout_widgets()

        self.matrix_input_widget_a = None
        self.matrix_input_widget_b = None

    def create_widgets(self):
        self.label_titulo = QLabel("<h2>Multiplicación de Matrices</h2>")
        self.label_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label_filas_a = QLabel("Número de filas Matriz A:")
        self.input_filas_a = QLineEdit()

        self.label_columnas_a = QLabel("Número de columnas Matriz A:")
        self.input_columnas_a = QLineEdit()

        self.label_filas_b = QLabel("Número de filas Matriz B:")
        self.input_filas_b = QLineEdit()

        self.label_columnas_b = QLabel("Número de columnas Matriz B:")
        self.input_columnas_b = QLineEdit()

        self.button_ingresar_a = QPushButton("Ingresar Matriz A")
        self.button_ingresar_a.setStyleSheet("background-color: #2196F3; color: white;")
        self.button_ingresar_a.clicked.connect(self.mostrar_matriz_a)

        self.button_ingresar_b = QPushButton("Ingresar Matriz B")
        self.button_ingresar_b.setStyleSheet("background-color: #2196F3; color: white;")
        self.button_ingresar_b.clicked.connect(self.mostrar_matriz_b)

        self.button_calcular = QPushButton("Calcular Multiplicación")
        self.button_calcular.setStyleSheet("background-color: #2196F3; color: white;")
        self.button_calcular.setEnabled(False)
        self.button_calcular.clicked.connect(self.calcular_multiplicacion)

        self.textedit_resultado = QTextEdit()
        self.textedit_resultado.setReadOnly(True)

    def layout_widgets(self):
        self.layout_principal = QVBoxLayout()

        self.layout_principal.addWidget(self.label_titulo)

        layout_filas_a = QHBoxLayout()
        layout_filas_a.addWidget(self.label_filas_a)
        layout_filas_a.addWidget(self.input_filas_a)

        layout_columnas_a = QHBoxLayout()
        layout_columnas_a.addWidget(self.label_columnas_a)
        layout_columnas_a.addWidget(self.input_columnas_a)

        layout_filas_b = QHBoxLayout()
        layout_filas_b.addWidget(self.label_filas_b)
        layout_filas_b.addWidget(self.input_filas_b)

        layout_columnas_b = QHBoxLayout()
        layout_columnas_b.addWidget(self.label_columnas_b)
        layout_columnas_b.addWidget(self.input_columnas_b)

        layout_buttons = QHBoxLayout()
        layout_buttons.addWidget(self.button_ingresar_a)
        layout_buttons.addWidget(self.button_ingresar_b)
        layout_buttons.addWidget(self.button_calcular)

        self.layout_principal.addLayout(layout_filas_a)
        self.layout_principal.addLayout(layout_columnas_a)
        self.layout_principal.addLayout(layout_filas_b)
        self.layout_principal.addLayout(layout_columnas_b)
        self.layout_principal.addLayout(layout_buttons)
        self.layout_principal.addWidget(self.textedit_resultado)

        self.setLayout(self.layout_principal)

    def mostrar_matriz_a(self):
        filas_texto = self.input_filas_a.text()
        columnas_texto = self.input_columnas_a.text()

        if not filas_texto or not columnas_texto:
            QMessageBox.warning(self, "Error", "Por favor ingrese el número de filas y columnas de la Matriz A.")
            return

        try:
            filas = int(filas_texto)
            columnas = int(columnas_texto)
        except ValueError:
            QMessageBox.warning(self, "Error", "Por favor ingrese números válidos para filas y columnas de la Matriz A.")
            return

        if filas <= 0 or columnas <= 0:
            QMessageBox.warning(self, "Error", "El número de filas y columnas de la Matriz A debe ser mayor que cero.")
            return

        if self.matrix_input_widget_a:
            self.layout_principal.removeWidget(self.matrix_input_widget_a)
            self.matrix_input_widget_a.deleteLater()

        self.matrix_input_widget_a = MatrixInputWidget(filas, columnas)
        self.layout_principal.insertWidget(5, self.matrix_input_widget_a)

        self.button_ingresar_a.setEnabled(False)

    def mostrar_matriz_b(self):
        filas_texto = self.input_filas_b.text()
        columnas_texto = self.input_columnas_b.text()

        if not filas_texto or not columnas_texto:
            QMessageBox.warning(self, "Error", "Por favor ingrese el número de filas y columnas de la Matriz B.")
            return

        try:
            filas = int(filas_texto)
            columnas = int(columnas_texto)
        except ValueError:
            QMessageBox.warning(self, "Error", "Por favor ingrese números válidos para filas y columnas de la Matriz B.")
            return

        if filas <= 0 or columnas <= 0:
            QMessageBox.warning(self, "Error", "El número de filas y columnas de la Matriz B debe ser mayor que cero.")
            return

        if self.matrix_input_widget_b:
            self.layout_principal.removeWidget(self.matrix_input_widget_b)
            self.matrix_input_widget_b.deleteLater()

        self.matrix_input_widget_b = MatrixInputWidget(filas, columnas)
        index_a = self.layout_principal.indexOf(self.matrix_input_widget_a)
        self.layout_principal.insertWidget(index_a + 1, self.matrix_input_widget_b)

        self.button_ingresar_b.setEnabled(False)
        self.button_calcular.setEnabled(True)

    def calcular_multiplicacion(self):
        filas_a_texto = self.input_filas_a.text()
        columnas_a_texto = self.input_columnas_a.text()
        filas_b_texto = self.input_filas_b.text()
        columnas_b_texto = self.input_columnas_b.text()

        try:
            filas_a = int(filas_a_texto)
            columnas_a = int(columnas_a_texto)
            filas_b = int(filas_b_texto)
            columnas_b = int(columnas_b_texto)
        except ValueError:
            QMessageBox.warning(self, "Error", "Por favor ingrese números válidos para las dimensiones de las matrices.")
            return

        if columnas_a != filas_b:
            QMessageBox.warning(self, "Error", "Las matrices no se pueden multiplicar. Las columnas de A deben ser iguales a las filas de B.")
            return

        matriz_a_data = self.matrix_input_widget_a.get_matrix_data()
        matriz_b_data = self.matrix_input_widget_b.get_matrix_data()

        if matriz_a_data is None or matriz_b_data is None:
            return

        resultado = []
        for i in range(len(matriz_a_data)):
            fila_resultado = []
            for j in range(len(matriz_b_data[0])):
                suma = 0
                for k in range(len(matriz_a_data[0])):
                    suma += matriz_a_data[i][k] * matriz_b_data[k][j]
                fila_resultado.append(suma)
            resultado.append(fila_resultado)

        resultado_texto = "Resultado de la Multiplicación:\n"
        resultado_texto += f"{self.format_matrix(resultado)}\n"

        self.textedit_resultado.setText(resultado_texto)

    def format_matrix(self, matrix):
        if not matrix:
            return ""
        rows = len(matrix)
        cols = len(matrix[0])
        formatted = ""
        for i in range(rows):
            for j in range(cols):
                formatted += f"{matrix[i][j]}\t"
            formatted += "\n"
        return formatted


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
