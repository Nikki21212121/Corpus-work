import pandas as pd
import matplotlib.pyplot as plt

# Leer los datos desde el archivo Excel
file_path = 'D:\\Sara\\2023-2024\\Libro datos del español\\Pruebas TimeLine\\ED\\DatosEDTIMELINE.xlsx'
data = pd.read_excel(file_path)

# Definir colores
colors = {'SAM': 'blue', 'SAI': 'blue', 'SAT': 'blue', 'SSD': 'red', 'SSS': 'red', 'SSTop': 'red', 'SS/SA':'red', 'SAX':'blue', 'SSX':'red'}

# Crear una columna para los colores basados en tipo_subacto
data['color'] = data['tipo_subacto'].map(colors)

# Configurar el gráfico
fig, ax = plt.subplots(figsize=(10, 5))

# Agrupar los datos por id_conversación
grouped = data.groupby('id_conversación')

# Añadir los subactos al gráfico
y_ticks = []
y_labels = []
y_position = 0

for conv_id, group in grouped:
    y_ticks.append(y_position + 5)
    y_labels.append(f"{conv_id}")
    for _, row in group.iterrows():
        start = row['Comienzo relativo']
        duration = row['duración']
        color = row['color']
        ax.broken_barh([(start, duration)], (y_position, 9), facecolors=color)
    y_position += 10

# Configurar ejes
ax.set_xlabel('Tiempo (ms)')
ax.set_ylabel('Conversaciones')
ax.set_yticks(y_ticks)
ax.set_yticklabels(y_labels)
ax.grid(True)


plt.savefig('TimeLineED 30segundos.svg', format='svg')


# Mostrar el gráfico
plt.show()

