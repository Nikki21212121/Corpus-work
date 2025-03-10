import xml.etree.ElementTree as ET

def clean_annotation_values(file_path):
    # Cargar el archivo EAF como un árbol de elementos XML
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Inicializar un contador para depuración
    count_replaced = 0

    # Buscar todas las etiquetas ANNOTATION_VALUE en el documento
    for annotation_value in root.iter('ANNOTATION_VALUE'):
        # Reemplazar ':' por '<al/>' en el texto de cada etiqueta ANNOTATION_VALUE
        if annotation_value.text and ':' in annotation_value.text:
            annotation_value.text = annotation_value.text.replace(':', '<al/>')
            count_replaced += 1  # Incrementar el contador cada vez que se hace una sustitución

    # Guardar los cambios en el archivo original o en uno nuevo
    tree.write("D:\\Sara\\Curso 2024-2025\\Corpus Valesco\\Revisiones corpus\\2016.PT.15-sinpuntos.eaf")

    # Retornar el número de sustituciones hechas para depuración
    return count_replaced

# Ruta al archivo .eaf
file_path = "D:\\Sara\\Curso 2024-2025\\Corpus Valesco\\Revisiones corpus\\2016.PT.15.eaf"
result = clean_annotation_values(file_path)
print("Número de reemplazos realizados:", result)


