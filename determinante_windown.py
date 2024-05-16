import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QGridLayout, QTextEdit, QMessageBox
from PyQt6.QtCore import Qt

class DeterminantCalculator(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Calculadora de Determinante")
        self.setGeometry(100, 100, 700, 500)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.title_label = QLabel("DETERMINANTE DE UNA MATRIZ")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.layout.addWidget(self.title_label)

        self.size_layout = QHBoxLayout()
        self.size_label = QLabel("Tamaño de la matriz cuadrada:")
        self.size_input = QLineEdit()
        self.size_layout.addWidget(self.size_label)
        self.size_layout.addWidget(self.size_input)
        self.layout.addLayout(self.size_layout)

        self.generate_matrix_button = QPushButton("Generar Matriz")
        self.generate_matrix_button.clicked.connect(self.generate_matrix)
        self.layout.addWidget(self.generate_matrix_button)

        self.matrix_title_label = QLabel("Valores de la Matriz:")
        self.layout.addWidget(self.matrix_title_label)

        self.matrix_layout = QGridLayout()
        self.layout.addLayout(self.matrix_layout)

        self.calculate_button = QPushButton("Calcular Determinante")
        self.calculate_button.clicked.connect(self.calculate_determinant)
        self.layout.addWidget(self.calculate_button)

        self.result_text_edit = QTextEdit()
        self.result_text_edit.setReadOnly(True)
        self.layout.addWidget(self.result_text_edit)

    def generate_matrix(self):
        size_str = self.size_input.text()
        try:
            size = int(size_str)
            if size <= 0:
                raise ValueError("El número de filas y columnas debe ser mayor que cero.")

            self.clear_matrix_layout()

            self.matrix = []
            for i in range(size):
                row_widgets = []
                for j in range(size):
                    cell = QLineEdit()
                    cell.setFixedWidth(50)
                    row_widgets.append(cell)
                    self.matrix_layout.addWidget(cell, i, j)
                self.matrix.append(row_widgets)
        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

    def clear_matrix_layout(self):
        for i in reversed(range(self.matrix_layout.count())):
            widget = self.matrix_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

    def calculate_determinant(self):
        if not hasattr(self, 'matrix'):
            self.result_text_edit.setPlainText("Primero debe generar la matriz.")
            return

        matrix_values = []
        for row_widgets in self.matrix:
            row_values = []
            for cell in row_widgets:
                value = cell.text()
                if not value:
                    self.result_text_edit.setPlainText("Debe ingresar valores para todos los elementos de la matriz.")
                    return
                row_values.append(float(value))
            matrix_values.append(row_values)

        determinant, procedure = self.calculate_matrix_determinant(matrix_values)
        result_text = f"El determinante de la matriz es: {determinant}\n\nProcedimiento:\n{procedure}"
        self.result_text_edit.setPlainText(result_text)

    def calculate_matrix_determinant(self, matrix):
        size = len(matrix)
        if size == 1:
            return matrix[0][0], f"Determinante de matriz 1x1: {matrix[0][0]}"
        elif size == 2:
            procedure = f"Determinante de matriz 2x2: ({matrix[0][0]} * {matrix[1][1]}) - ({matrix[0][1]} * {matrix[1][0]})"
            determinant = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
            return determinant, procedure
        else:
            determinant = 0
            procedure = ""
            for col in range(size):
                sub_matrix = [row[:col] + row[col+1:] for row in matrix[1:]]
                sign = (-1) ** col
                sub_determinant, sub_procedure = self.calculate_matrix_determinant(sub_matrix)
                determinant += sign * matrix[0][col] * sub_determinant
                if col == 0:
                    procedure += f"{sign} * {matrix[0][col]} * {sub_procedure}"
                else:
                    procedure += f" + {sign} * {matrix[0][col]} * {sub_procedure}"
            procedure = f"Determinante de matriz {size}x{size}: {procedure}"
            return determinant, procedure

if __name__ == "__main__":
    app = QApplication(sys.argv)
    calculator = DeterminantCalculator()
    calculator.show()
    sys.exit(app.exec())

