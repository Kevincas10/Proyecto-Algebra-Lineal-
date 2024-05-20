import sys
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QTextEdit, QMessageBox
from PyQt6.QtCore import Qt, pyqtSignal


class MatrixInputWidget(QWidget):
    def __init__(self, rows, cols):
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
                label = QLabel()
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


class MainWindowResta(QWidget):
    window_closed = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Resta de Matrices")
        self.setGeometry(100, 100, 800, 600)

        self.layout_principal = QVBoxLayout()

        self.create_widgets()
        self.layout_widgets()
        icon = QIcon("logo.png")
        self.setWindowIcon(icon)

        self.matriz_a = None
        self.matriz_b = None

    def closeEvent(self, event):
        self.window_closed.emit()
        super().closeEvent(event)

    def create_widgets(self):
        self.label_titulo = QLabel("<h2>Resta de Matrices</h2>")
        self.label_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label_filas = QLabel("Número de filas:")
        self.input_filas = QLineEdit()

        self.label_columnas = QLabel("Número de columnas:")
        self.input_columnas = QLineEdit()

        self.button_ingresar_a = QPushButton("Ingresar Matriz A")
        self.button_ingresar_a.setStyleSheet("background-color: #008080; color: white; border: 2px solid black; border-radius: 13px;")

        self.button_ingresar_b = QPushButton("Ingresar Matriz B")
        self.button_ingresar_b.setStyleSheet("background-color: #008080; color: white; border: 2px solid black; border-radius: 13px;")
        self.button_ingresar_b.setEnabled(False)

        self.button_calcular = QPushButton("Calcular Resta")
        self.button_calcular.setStyleSheet("background-color: #008080; color: white; border: 2px solid black; border-radius: 13px;")
        self.button_calcular.setEnabled(False)

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

        layout_principal.addLayout(layout_filas)
        layout_principal.addLayout(layout_columnas)

        self.matrix_input_widget_a = None
        self.matrix_input_widget_b = None

        self.button_ingresar_a.clicked.connect(self.ingresar_matriz_a)
        self.button_ingresar_b.clicked.connect(self.ingresar_matriz_b)
        self.button_calcular.clicked.connect(self.calcular_resta)

        layout_principal.addWidget(self.button_ingresar_a)
        layout_principal.addWidget(self.button_ingresar_b)
        layout_principal.addWidget(self.button_calcular)
        layout_principal.addWidget(self.textedit_resultado)

        self.layout_principal = layout_principal

        self.setLayout(layout_principal)

    def ingresar_matriz_a(self):
        filas_texto = self.input_filas.text()
        columnas_texto = self.input_columnas.text()

        if not filas_texto or not columnas_texto:
            QMessageBox.warning(self, "Error", "Por favor ingrese el número de filas y columnas.")
            return

        try:
            filas = int(filas_texto)
            columnas = int(columnas_texto)
        except ValueError:
            QMessageBox.warning(self, "Error", "Por favor ingrese números válidos para filas y columnas.")
            return

        if filas <= 0 or columnas <= 0:
            QMessageBox.warning(self, "Error", "El número de filas y columnas debe ser mayor que cero.")
            return

        self.matrix_input_widget_a = MatrixInputWidget(filas, columnas)
        self.layout_principal.insertWidget(4, self.matrix_input_widget_a)

        self.button_ingresar_a.setEnabled(False)
        self.button_ingresar_b.setEnabled(True)

    def ingresar_matriz_b(self):
        filas_texto = self.input_filas.text()
        columnas_texto = self.input_columnas.text()

        if not filas_texto or not columnas_texto:
            QMessageBox.warning(self, "Error", "Por favor ingrese el número de filas y columnas.")
            return

        try:
            filas = int(filas_texto)
            columnas = int(columnas_texto)
        except ValueError:
            QMessageBox.warning(self, "Error", "Por favor ingrese números válidos para filas y columnas.")
            return

        if filas <= 0 or columnas <= 0:
            QMessageBox.warning(self, "Error", "El número de filas y columnas debe ser mayor que cero.")
            return

        self.matrix_input_widget_b = MatrixInputWidget(filas, columnas)
        index_boton_ingresar_b = self.layout_principal.indexOf(self.button_ingresar_b)
        self.layout_principal.insertWidget(index_boton_ingresar_b + 1, self.matrix_input_widget_b)

        self.button_ingresar_b.setEnabled(False)
        self.button_calcular.setEnabled(True)

    def calcular_resta(self):
        matriz_a_data = self.matrix_input_widget_a.get_matrix_data()
        matriz_b_data = self.matrix_input_widget_b.get_matrix_data()

        if matriz_a_data is None or matriz_b_data is None:
            return

        if len(matriz_a_data) != len(matriz_b_data) or len(matriz_a_data[0]) != len(matriz_b_data[0]):
            QMessageBox.warning(self, "Error", "Las matrices deben tener la misma dimensión para realizar la resta.")
            return

        resultado = []
        procedimiento = []
        for i in range(len(matriz_a_data)):
            fila_resultado = []
            fila_procedimiento = []
            for j in range(len(matriz_a_data[i])):
                resta = matriz_a_data[i][j] - matriz_b_data[i][j]
                fila_resultado.append(resta)
                fila_procedimiento.append(f"{matriz_a_data[i][j]} - {matriz_b_data[i][j]} = {resta}")
            resultado.append(fila_resultado)
            procedimiento.append(fila_procedimiento)

        resultado_texto = "Procedimiento de la Resta:\n"
        for i in range(len(procedimiento)):
            for j in range(len(procedimiento[i])):
                resultado_texto += f"{procedimiento[i][j]}\t"
            resultado_texto += "\n"

        resultado_texto += "\nResultado de la Resta:\n"
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
    window = MainWindowResta()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
