import sys
import numpy as np
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QSpacerItem,
    QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class VectorAdditionApp(QWidget):
    window_closed = pyqtSignal()

    def __init__(self):
        super().__init__()
        icon = QIcon("logo.png")
        self.setWindowIcon(icon)

        self.setWindowTitle("Suma de Vectores y Gráfica")
        self.setGeometry(100, 100, 800, 600)
        self.center_window()  # Centrar la ventana

        layout = QVBoxLayout()

        logo_label = QLabel()
        pixmap = QPixmap("logo.png")
        pixmap_resized = pixmap.scaledToWidth(70)
        logo_label.setPixmap(pixmap_resized)

        # Título centrado y en negrita
        self.label_titulo = QLabel("<h1><b>Suma de vectores.</b></h1>")
        self.label_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Layout para el título y el logo
        layout_titulo_logo = QHBoxLayout()
        layout_titulo_logo.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        layout_titulo_logo.addWidget(logo_label)
        layout_titulo_logo.addWidget(self.label_titulo)
        layout_titulo_logo.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        layout.addLayout(layout_titulo_logo)

        # Layouts
        input_layout = QHBoxLayout()
        result_layout = QVBoxLayout()

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
        self.add_button.setStyleSheet("height: 30px; background-color: #008080; color: white; border: 2px solid black; border-radius: 13px;")
        input_layout.addWidget(self.add_button)

        # Matplotlib Figure
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        # Add layouts to main layout
        layout.addLayout(input_layout)
        layout.addLayout(result_layout)
        layout.addWidget(self.canvas)

        # Set main layout
        self.setLayout(layout)

    def center_window(self):
        screen_geometry = QApplication.primaryScreen().geometry()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_geometry.center())
        self.move(window_geometry.topLeft())

    def closeEvent(self, event):
        self.window_closed.emit()
        super().closeEvent(event)

    def add_vectors(self):
        vector_a_str = self.vector_a_input.text()
        vector_b_str = self.vector_b_input.text()

        try:
            x1, y1 = map(float, vector_a_str.split(','))
            x2, y2 = map(float, vector_b_str.split(','))

            # Calculamos el vector resultante como la suma de los vectores
            vector_resultante = np.array([x1 + x2, y1 + y2])

            # Calculamos la magnitud del vector usando el Teorema de Pitágoras
            magnitude = np.linalg.norm(vector_resultante)
            self.result_display.setText(f"{magnitude:.2f}")

            # Procedimiento
            procedure_text = f"Magnitud = √(({x1} + {x2})² + ({y1} + {y2})²)"
            self.procedure_display.setText(procedure_text)

            self.plot_vectors(x1, y1, x2, y2)

        except ValueError as e:
            QMessageBox.warning(self, "Error", "Por favor, ingresa coordenadas válidas separadas por comas.")

    def plot_vectors(self, x1, y1, x2, y2):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        # Dibujamos el vector resultante como una flecha desde el origen (0,0) hasta el punto (x1+x2, y1+y2)
        ax.quiver(0, 0, x1 + x2, y1 + y2, angles='xy', scale_units='xy', scale=1, color='g', label='Vector Resultante')

        # Dibujamos el punto final del vector resultante
        ax.plot(x1 + x2, y1 + y2, 'ro')  # Punto final en rojo
        ax.text(x1 + x2, y1 + y2, f'({x1 + x2}, {y1 + y2})', fontsize=9, ha='left')

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
