import sys
import numpy as np
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QTextEdit, QMessageBox
)

class MatrixInputWidget(QWidget):
    def __init__(self, size):
        super().__init__()

        self.size = size
        self.create_widgets()
        self.layout_widgets()

    def create_widgets(self):
        self.labels = []
        self.inputs = []
        for i in range(self.size):
            row_labels = []
            row_inputs = []
            for j in range(self.size):
                label = QLabel(f"A[{i + 1},{j + 1}]:")
                input_box = QLineEdit()
                row_labels.append(label)
                row_inputs.append(input_box)
            self.labels.append(row_labels)
            self.inputs.append(row_inputs)

    def layout_widgets(self):
        layout = QVBoxLayout()

        for i in range(self.size):
            hbox = QHBoxLayout()
            for j in range(self.size):
                hbox.addWidget(self.labels[i][j])
                hbox.addWidget(self.inputs[i][j])
            layout.addLayout(hbox)

        self.setLayout(layout)

    def get_matrix_data(self):
        matrix_data = []
        for i in range(self.size):
            row_data = []
            for j in range(self.size):
                value = self.inputs[i][j].text()
                try:
                    value = float(value)
                except ValueError:
                    QMessageBox.warning(self, "Error", "Por favor ingrese solo números en la matriz.")
                    return None
                row_data.append(value)
            matrix_data.append(row_data)
        return matrix_data


class ProcessWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Proceso de Cálculo")
        self.setGeometry(100, 100, 800, 600)

        self.textedit_process = QTextEdit()
        self.textedit_process.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.textedit_process)

        self.setLayout(layout)

    def set_process_text(self, process_text):
        self.textedit_process.setText(process_text)


class MainWindowInversa(QWidget):
    window_closed = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Inversa de Matriz Cuadrada")
        self.setGeometry(100, 100, 800, 600)

        self.layout_principal = QVBoxLayout()

        self.create_widgets()
        self.layout_widgets()

        self.matrix_input_widget = None

    def closeEvent(self, event):
        self.window_closed.emit()
        super().closeEvent(event)


    def create_widgets(self):
        self.label_titulo = QLabel("<h2>Inversa de Matriz Cuadrada</h2>")
        self.label_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label_size = QLabel("Tamaño de la Matriz Cuadrada:")
        self.input_size = QLineEdit()

        self.button_ingresar_matriz = QPushButton("Ingresar Matriz")
        self.button_ingresar_matriz.setStyleSheet("background-color: #2196F3; color: white;")
        self.button_ingresar_matriz.clicked.connect(self.ingresar_matriz)

        self.button_confirmar = QPushButton("Confirmar")
        self.button_confirmar.setStyleSheet("background-color: #4CAF50; color: white;")
        self.button_confirmar.clicked.connect(self.mostrar_proceso)

        self.textedit_resultado = QTextEdit()
        self.textedit_resultado.setReadOnly(True)

    def layout_widgets(self):
        layout_principal = QVBoxLayout()

        layout_principal.addWidget(self.label_titulo)

        layout_size = QHBoxLayout()
        layout_size.addWidget(self.label_size)
        layout_size.addWidget(self.input_size)

        layout_principal.addLayout(layout_size)
        layout_principal.addWidget(self.button_ingresar_matriz)
        layout_principal.addWidget(self.button_confirmar)
        layout_principal.addWidget(self.textedit_resultado)

        self.layout_principal = layout_principal
        self.setLayout(layout_principal)

    def ingresar_matriz(self):
        size_text = self.input_size.text()

        if not size_text:
            QMessageBox.warning(self, "Error", "Por favor ingrese el tamaño de la matriz.")
            return

        try:
            size = int(size_text)
        except ValueError:
            QMessageBox.warning(self, "Error", "Por favor ingrese un número válido para el tamaño de la matriz.")
            return

        if size <= 0:
            QMessageBox.warning(self, "Error", "El tamaño de la matriz debe ser mayor que cero.")
            return

        self.matrix_input_widget = MatrixInputWidget(size)
        index_button_ingresar_matriz = self.layout_principal.indexOf(self.button_ingresar_matriz)
        self.layout_principal.insertWidget(index_button_ingresar_matriz + 1, self.matrix_input_widget)

        self.button_ingresar_matriz.setEnabled(False)
        self.input_size.setEnabled(False)

    def mostrar_proceso(self):
        matriz_data = self.matrix_input_widget.get_matrix_data()

        if matriz_data is None:
            return

        try:
            matriz_np = np.array(matriz_data)
            inversa_np = np.linalg.inv(matriz_np)
        except np.linalg.LinAlgError:
            QMessageBox.warning(self, "Error", "La matriz no es invertible.")
            return

        process_text = "Proceso para Calcular la Inversa de la Matriz:\n"
        process_text += "Matriz Original:\n" + self.format_matrix(matriz_np) + "\n\n"

        augmented_matrix = np.hstack((matriz_np, np.eye(matriz_np.shape[0])))
        process_text += "Matriz Aumentada:\n" + self.format_matrix(augmented_matrix) + "\n\n"

        # Aplicando eliminación Gaussiana
        n = len(matriz_np)
        for i in range(n):
            # Escalar la fila para hacer que el elemento diagonal sea 1
            diag_element = augmented_matrix[i, i]
            augmented_matrix[i] = augmented_matrix[i] / diag_element
            process_text += f"Escalando fila {i + 1} para hacer que el elemento diagonal sea 1:\n" + self.format_matrix(augmented_matrix) + "\n\n"

            # Hacer que todos los demás elementos en la columna i sean 0
            for j in range(n):
                if i != j:
                    factor = augmented_matrix[j, i]
                    augmented_matrix[j] = augmented_matrix[j] - factor * augmented_matrix[i]
                    process_text += f"Haciendo cero el elemento en la posición ({j + 1}, {i + 1}):\n" + self.format_matrix(augmented_matrix) + "\n\n"

        inversa_np = augmented_matrix[:, n:]
        process_text += "Matriz Inversa:\n" + self.format_matrix(inversa_np) + "\n"

        self.textedit_resultado.setText(f"{process_text}\nResultado Final:\n{self.format_matrix(inversa_np)}")

    def format_matrix(self, matrix):
        return "\n".join(["\t".join(map("{:.4f}".format, row)) for row in matrix])

def main():
    app = QApplication(sys.argv)
    window = MainWindowInversa()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
