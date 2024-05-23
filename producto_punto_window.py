import sys

from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt, pyqtSignal


def producto_punto(vector1, vector2):
    if len(vector1) != len(vector2):
        raise ValueError("Los vectores deben tener la misma longitud.")
    producto = sum(a * b for a, b in zip(vector1, vector2))
    return producto


class ProductoPuntoApp(QWidget):
    window_closed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()
        icon = QIcon("logo.png")
        self.setWindowIcon(icon)

    def initUI(self):
        self.setWindowTitle('Multiplicación de Vectores')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        logo_label = QLabel()
        pixmap = QPixmap("logo.png")
        pixmap_resized = pixmap.scaledToWidth(70)
        logo_label.setPixmap(pixmap_resized)

        # Título centrado y en negrita
        self.label_titulo = QLabel("<h1><b>Multiplicacion de vectores</b></h1>")
        self.label_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Layout para el título y el logo
        layout_titulo_logo = QHBoxLayout()
        layout_titulo_logo.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        layout_titulo_logo.addWidget(logo_label)
        layout_titulo_logo.addWidget(self.label_titulo)
        layout_titulo_logo.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        layout.addLayout(layout_titulo_logo)

        self.vector1_label = QLabel('Ingrese el primer vector:')
        layout.addWidget(self.vector1_label)
        self.vector1_inputs = [QLineEdit(self) for _ in range(3)]
        vector1_layout = QHBoxLayout()
        for input_field in self.vector1_inputs:
            input_field.setFixedWidth(50)
            vector1_layout.addWidget(input_field)
        layout.addLayout(vector1_layout)

        self.vector2_label = QLabel('Ingrese el segundo vector:')
        layout.addWidget(self.vector2_label)
        self.vector2_inputs = [QLineEdit(self) for _ in range(3)]
        vector2_layout = QHBoxLayout()
        for input_field in self.vector2_inputs:
            input_field.setFixedWidth(50)
            vector2_layout.addWidget(input_field)
        layout.addLayout(vector2_layout)

        self.calculate_button = QPushButton('Calcular Producto Punto')
        self.calculate_button.clicked.connect(self.calcular_producto_punto)
        self.calculate_button.setStyleSheet("height: 30px; background-color: #008080; color: white; border: 2px solid black; border-radius: 13px;")
        layout.addWidget(self.calculate_button)

        self.result_output = QTextEdit()
        self.result_output.setReadOnly(True)
        layout.addWidget(self.result_output)

        self.setLayout(layout)
        self.center_window()

    def closeEvent(self, event):
        self.window_closed.emit()
        super().closeEvent(event)

    def calcular_producto_punto(self):
        try:
            vector1 = [float(field.text()) for field in self.vector1_inputs]
            vector2 = [float(field.text()) for field in self.vector2_inputs]

            procedimiento = []
            for a, b in zip(vector1, vector2):
                procedimiento.append(f"{a} * {b} = {a * b}")

            resultado = producto_punto(vector1, vector2)
            procedimiento.append(f"\nEl producto punto de los vectores es: {resultado}")

            self.result_output.setText("\n".join(procedimiento))
        except ValueError:
            self.result_output.setText("Todos los componentes del vector deben ser números.")

    def center_window(self):
        screen_geometry = QApplication.primaryScreen().geometry()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_geometry.center())
        self.move(window_geometry.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ProductoPuntoApp()
    ex.show()
    sys.exit(app.exec())
