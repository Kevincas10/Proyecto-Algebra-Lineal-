import sys
import numpy as np
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QTextEdit, \
    QMessageBox


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
                label = QLabel(f"A[{i + 1},{j + 1}]:")
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


class ProcessWindow(QWidget):
    def __init__(self, process_text):
        super().__init__()
        self.setWindowTitle("Proceso de Cálculo")
        self.setGeometry(100, 100, 800, 600)
        self.textedit_process = QTextEdit()
        self.textedit_process.setReadOnly(True)
        self.textedit_process.setText(process_text)
        layout = QVBoxLayout()
        layout.addWidget(self.textedit_process)
        self.setLayout(layout)


class MainWindowRango(QWidget):
    window_closed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rango de Matriz")
        self.setGeometry(100, 100, 800, 600)
        self.layout_principal = QVBoxLayout()
        self.create_widgets()
        self.layout_widgets()
        self.matrix_input_widget = None

    def closeEvent(self, event):
        self.window_closed.emit()
        super().closeEvent(event)


    def create_widgets(self):
        self.label_titulo = QLabel("<h2>Rango de Matriz</h2>")
        self.label_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_rows = QLabel("Número de Filas:")
        self.input_rows = QLineEdit()
        self.label_cols = QLabel("Número de Columnas:")
        self.input_cols = QLineEdit()
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
        layout_size.addWidget(self.label_rows)
        layout_size.addWidget(self.input_rows)
        layout_size.addWidget(self.label_cols)
        layout_size.addWidget(self.input_cols)
        layout_principal.addLayout(layout_size)
        layout_principal.addWidget(self.button_ingresar_matriz)
        layout_principal.addWidget(self.button_confirmar)
        layout_principal.addWidget(self.textedit_resultado)
        self.layout_principal = layout_principal
        self.setLayout(layout_principal)

    def ingresar_matriz(self):
        rows_text = self.input_rows.text()
        cols_text = self.input_cols.text()
        if not rows_text or not cols_text:
            QMessageBox.warning(self, "Error", "Por favor ingrese el número de filas y columnas.")
            return
        try:
            rows = int(rows_text)
            cols = int(cols_text)
        except ValueError:
            QMessageBox.warning(self, "Error", "Por favor ingrese números válidos para las filas y columnas.")
            return
        if rows <= 0 or cols <= 0:
            QMessageBox.warning(self, "Error", "El número de filas y columnas debe ser mayor que cero.")
            return
        self.matrix_input_widget = MatrixInputWidget(rows, cols)
        index_button_ingresar_matriz = self.layout_principal.indexOf(self.button_ingresar_matriz)
        self.layout_principal.insertWidget(index_button_ingresar_matriz + 1, self.matrix_input_widget)
        self.button_ingresar_matriz.setEnabled(False)
        self.input_rows.setEnabled(False)
        self.input_cols.setEnabled(False)

    def mostrar_proceso(self):
        matriz_data = self.matrix_input_widget.get_matrix_data()
        if matriz_data is None:
            return
        matriz_np = np.array(matriz_data)
        filas, columnas = matriz_np.shape
        proceso_text = "Proceso para Calcular el Rango de la Matriz usando Eliminación Gaussiana:\n"
        proceso_text += f"Matriz Original:\n{matriz_np}\n\n"
        # Realizar eliminación gaussiana
        for i in range(min(filas, columnas)):
            if matriz_np[i, i] != 0:
                proceso_text += f"Dividir la fila {i + 1} por {matriz_np[i, i]}:\n"
                matriz_np[i] = matriz_np[i] / matriz_np[i, i]
                proceso_text += f"{matriz_np}\n\n"
            else:
                for k in range(i + 1, filas):
                    if matriz_np[k, i] != 0:
                        proceso_text += f"Intercambiar fila {i + 1} con fila {k + 1}:\n"
                        matriz_np[[i, k]] = matriz_np[[k, i]]
                        matriz_np[i] = matriz_np[i] / matriz_np[i, i]
                        proceso_text += f"{matriz_np}\n\n"
                        break
            for j in range(i + 1, filas):
                if matriz_np[j, i] != 0:
                    coef = matriz_np[j, i]
                    matriz_np[j] = matriz_np[j] - coef * matriz_np[i]
                    proceso_text += f"Restar {coef} veces la fila {i + 1} de la fila {j + 1}:\n"
                    proceso_text += f"{matriz_np}\n\n"
        rango = np.sum(np.any(matriz_np != 0, axis=1))
        proceso_text += f"Matriz Transformada:\n{matriz_np}\n\n"
        proceso_text += f"Rango de la Matriz: {rango}\n"
        self.textedit_resultado.setText(proceso_text)
        process_window = ProcessWindow(proceso_text)
        process_window.show()


def main():
    app = QApplication(sys.argv)
    window = MainWindowRango()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
