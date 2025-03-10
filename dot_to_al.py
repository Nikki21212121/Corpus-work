import xml.etree.ElementTree as ET

def clean_annotation_values(file_path, output_path):
    # Cargar el archivo EAF como un árbol de elementos XML
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Buscar todas las etiquetas ANNOTATION_VALUE en el documento
    count_replaced = 0
    for annotation_value in root.iter('ANNOTATION_VALUE'):
        if annotation_value.text and ':' in annotation_value.text:
            annotation_value.text = annotation_value.text.replace(':', '<al/>')
            count_replaced += 1

    # Convertir el árbol a string
    xml_string = ET.tostring(root, encoding='unicode')

    # Eliminar espacios no deseados antes de ' />'
    xml_string = xml_string.replace(' />', '/>')

    # Guardar los cambios en el archivo de salida
    with open(output_path, 'w', encoding='UTF-8') as file:
        file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        file.write(xml_string)

    return count_replaced

# Rutas a los archivos
input_path = "D:\\Sara\\Curso 2023-2024\\Proyecto DIA XX\\problemas corpus\\2020.PT.32.eaf"
output_path = "D:\\Sara\\Curso 2023-2024\\Proyecto DIA XX\\problemas corpus\\2020.PT.32sinpuntos.eaf"
result = clean_annotation_values(input_path, output_path)
print("Número de reemplazos realizados:", result)
