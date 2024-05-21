import sys
import numpy as np
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
)
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class VectorAdditionApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Suma de Vectores y Gráfica")
        self.setGeometry(100, 100, 800, 600)

        # Layouts
        main_layout = QVBoxLayout()
        input_layout = QHBoxLayout()
        result_layout = QHBoxLayout()

        # Widgets for vector A
        self.vector_a_label = QLabel("Vector A (x1, y1):")
        self.vector_a_input = QLineEdit()

        # Widgets for vector B
        self.vector_b_label = QLabel("Vector B (x2, y2):")
        self.vector_b_input = QLineEdit()

        # Add widgets to input layout
        input_layout.addWidget(self.vector_a_label)
        input_layout.addWidget(self.vector_a_input)
        input_layout.addWidget(self.vector_b_label)
        input_layout.addWidget(self.vector_b_input)

        # Result
        self.result_label = QLabel("Magnitud del Vector Resultante:")
        self.result_display = QLabel("")

        result_layout.addWidget(self.result_label)
        result_layout.addWidget(self.result_display)

        # Procedimiento
        self.procedure_label = QLabel("Procedimiento para obtener la magnitud:")
        self.procedure_display = QLabel("")

        result_layout.addWidget(self.procedure_label)
        result_layout.addWidget(self.procedure_display)

        # Button
        self.add_button = QPushButton("Sumar y Graficar")
        self.add_button.clicked.connect(self.add_vectors)
        input_layout.addWidget(self.add_button)

        # Matplotlib Figure
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        # Add layouts to main layout
        main_layout.addLayout(input_layout)
        main_layout.addLayout(result_layout)
        main_layout.addWidget(self.canvas)

        # Set main layout
        self.setLayout(main_layout)

    def add_vectors(self):
        vector_a_str = self.vector_a_input.text()
        vector_b_str = self.vector_b_input.text()

        try:
            x1, y1 = map(float, vector_a_str.split(','))
            x2, y2 = map(float, vector_b_str.split(','))

            # Calculamos la diferencia entre los puntos
            vector = np.array([x2 - x1, y2 - y1])

            # Calculamos la magnitud del vector usando el Teorema de Pitágoras
            magnitude = np.linalg.norm(vector)
            self.result_display.setText(f"{magnitude:.2f}")

            # Procedimiento
            procedure_text = f"Magnitud = √(({x2} - {x1})² + ({y2} - {y1})²)"
            self.procedure_display.setText(procedure_text)

            self.plot_vectors(x1, y1, x2, y2)

        except ValueError as e:
            QMessageBox.warning(self, "Error", "Por favor, ingresa coordenadas válidas separadas por comas.")

    def plot_vectors(self, x1, y1, x2, y2):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        # Dibujamos el vector como una flecha desde el punto A hasta el punto B
        ax.quiver(x1, y1, x2 - x1, y2 - y1, angles='xy', scale_units='xy', scale=1, color='g',
                  label='Vector Resultante')

        # Dibujamos el punto de inicio y fin del vector
        ax.plot(x1, y1, 'bo')  # Punto de inicio en azul
        ax.text(x1, y1, f'({x1}, {y1})', fontsize=9, ha='right')

        ax.plot(x2, y2, 'ro')  # Punto de fin en rojo
        ax.text(x2, y2, f'({x2}, {y2})', fontsize=9, ha='left')

        # Dibujamos el plano cartesiano
        ax.axhline(0, color='black', linewidth=0.5)
        ax.axvline(0, color='black', linewidth=0.5)

        # Etiquetamos los ejes
        ax.set_xlabel('X')
        ax.set_ylabel('Y')

        ax.set_xlim(-10, 10)
        ax.set_ylim(-10, 10)
        ax.set_aspect('equal')
        ax.grid()
        ax.legend()

        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VectorAdditionApp()
    window.show()
    sys.exit(app.exec())
