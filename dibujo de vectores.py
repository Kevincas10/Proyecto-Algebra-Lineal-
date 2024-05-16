import matplotlib.pyplot as plt
import numpy as np

# Definir los vectores
vector1 = np.array([4, 3])
vector2 = np.array([4, 1])

# Crear una figura y un conjunto de ejes
fig, ax = plt.subplots()

# Origen de los vectores
origin = np.array([0, 0])

# Graficar los vectores
ax.quiver(*origin, *vector1, scale=1, scale_units='xy', angles='xy', color=['r'], label='Vector 1')
ax.quiver(*origin, *vector2, scale=1, scale_units='xy', angles='xy', color=['b'], label='Vector 2')

# Establecer límites de los ejes
ax.set_xlim(0, 5)
ax.set_ylim(0, 5)

# Agregar una cuadrícula
ax.grid()

# Agregar leyenda
ax.legend()

# Configurar los ejes para que tengan la misma escala
ax.set_aspect('equal')

# Mostrar el gráfico
plt.show()
