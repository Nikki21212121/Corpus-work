import re
import xml.etree.ElementTree as ET


def extract_interventions_ordered(transcript_path):
    """
    Extrae las intervenciones de la transcripción, ignorando líneas que son exclusivamente numéricas
    o que cumplen con un patrón específico no deseado, como ciertas notas al pie.

    :param transcript_path: Ruta al archivo de transcripción.
    :return: Lista de diccionarios con el hablante y el texto de cada intervención.
    """
    interventions = []
    # Patrón para identificar hablantes e intervenciones iniciales.
    speaker_pattern = re.compile(r'^([A-Z]):\s*(.*)')
    # Patrón para identificar y omitir líneas que son exclusivamente numéricas.
    ignore_pattern = re.compile(r'^\d+\s*$')
    # Patrón adicional para identificar y omitir notas al pie no deseadas que comienzan con números.
    note_ignore_pattern = re.compile(r'^\d+\s+[A-Za-z]+')
    current_speaker = None
    current_text = ""

    with open(transcript_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            # Ignorar líneas vacías, líneas exclusivamente numéricas o notas al pie específicas.
            if not line or ignore_pattern.match(line) or note_ignore_pattern.match(line):
                continue
            match = speaker_pattern.match(line)
            if match:
                # Si hay texto acumulado para el hablante actual, añadirlo antes de procesar el nuevo.
                if current_speaker:
                    interventions.append({'speaker': current_speaker, 'text': current_text})
                current_speaker, current_text = match.groups()
            else:
                # Concatenar con la intervención actual si la línea no inicia una nueva intervención.
                current_text += " " + line

    # Añadir la última intervención recogida al finalizar el archivo.
    if current_speaker and current_text:
        interventions.append({'speaker': current_speaker, 'text': current_text})

    return interventions

# Ruta al archivo de transcripción (ajústala según sea necesario)
transcript_path = 'D:\\Sara\\Curso 2023-2024\\Proyecto DIA XX\\Conversaciones Oralia\\Conversaciones sin audio\\1994.PT.74 - IM339\\1999.PT.74 - IM.339.txt'

# Extraer las intervenciones manteniendo el orden de aparición
interventions = extract_interventions_ordered(transcript_path)

# Imprimir las intervenciones extraídas para verificar
for intervention in interventions:
    print(f"Hablante {intervention['speaker']}: {intervention['text']}")



def convert_chars_in_annotation_value(text):
    """
    Convierte los caracteres '<' y '>' a su representación en formato HTML solo dentro de las etiquetas
    <ANNOTATION_VALUE>...</ANNOTATION_VALUE>.
    """
    pattern = re.compile(r'(<ANNOTATION_VALUE>)(.*?)(</ANNOTATION_VALUE>)', re.DOTALL)

    def replace_chars(match):
        inner_text = match.group(2).replace("<", "&lt;").replace(">", "&gt;")
        return f"{match.group(1)}{inner_text}{match.group(3)}"

    return pattern.sub(replace_chars, text)


def generate_elan_format_sequential(transcript_ordered, start_time=1140, time_increment=1000):
    xml_text = "<ANNOTATION_DOCUMENT>\n<HEADER/>\n<TIME_ORDER>\n"
    time_slot_id = 1  # Iniciar el contador de TIME_SLOT_ID
    annotation_id = 1  # Iniciar el contador de ANNOTATION_ID
    current_time_value = start_time

    # Lista para guardar la información de las anotaciones en orden
    annotations_info = []

    # Generar TIME_SLOT secuenciales en la sección TIME_ORDER y recoger información para las anotaciones
    for entry in transcript_ordered:
        speaker = entry['speaker']
        text = entry['text']
        ts_start_id = time_slot_id
        ts_end_id = time_slot_id + 1
        annotations_info.append((speaker, text, ts_start_id, ts_end_id))

        # Añadir TIME_SLOT al documento XML
        xml_text += f'    <TIME_SLOT TIME_SLOT_ID="ts{ts_start_id}" TIME_VALUE="{current_time_value}" />\n'
        xml_text += f'    <TIME_SLOT TIME_SLOT_ID="ts{ts_end_id}" TIME_VALUE="{current_time_value + time_increment}" />\n'

        time_slot_id += 2  # Preparar los IDs para la próxima intervención
        current_time_value += time_increment + 500  # Asumiendo un pequeño descanso entre intervenciones

    xml_text += "</TIME_ORDER>\n"

    # Agrupar las anotaciones por hablante y generar las TIER correspondientes
    tiers = {}
    for speaker, text, ts_start_id, ts_end_id in annotations_info:
        if speaker not in tiers:
            tiers[speaker] = []
        tiers[speaker].append((text, ts_start_id, ts_end_id))

    for speaker, annotations in tiers.items():
        xml_text += f'<TIER DEFAULT_LOCALE="en" LANG_REF="spa" LINGUISTIC_TYPE_REF="phon" PARTICIPANT="{speaker}" TIER_ID="{speaker}_phon">\n'
        for text, ts_start_id, ts_end_id in annotations:
            xml_text += '    <ANNOTATION>\n'
            xml_text += f'        <ALIGNABLE_ANNOTATION ANNOTATION_ID="a{(ts_start_id + 1) // 2}" TIME_SLOT_REF1="ts{ts_start_id}" TIME_SLOT_REF2="ts{ts_end_id}">\n'
            xml_text += f'            <ANNOTATION_VALUE>{text}</ANNOTATION_VALUE>\n'
            xml_text += '        </ALIGNABLE_ANNOTATION>\n'
            xml_text += '    </ANNOTATION>\n'
        xml_text += '</TIER>\n'

    xml_text += "</ANNOTATION_DOCUMENT>"
    return xml_text

# Generar el formato ELAN considerando el orden de las intervenciones y evitar la repetición de TIER
elan_text = generate_elan_format_sequential(interventions)

# Mostrar el resultado o guardarlo en un archivo
print(elan_text)
# Esta línea se usa para guardar el resultado en un archivo, asegúrate de definir la ruta adecuada
# save_to_file(elan_text_efficient, 'output_efficient_elan.xml')


def transform_uppercase_in_annotation_value(xml_text):
    """
    Transforma palabras en mayúsculas dentro de <ANNOTATION_VALUE> a una versión etiquetada y en minúsculas.

    :param xml_text: El texto XML que contiene los elementos <ANNOTATION_VALUE>.
    :return: Texto XML transformado.
    """
    # Patrón para encontrar palabras en mayúsculas
    uppercase_pattern = re.compile(r'\b([A-ZÁÉÍÓÚÑ]+)\b')

    def replace_with_tag(match):
        word = match.group(1).lower()  # Convertir la palabra a minúsculas
        return f'<enf t="prm">{word}</enf>'  # Retornar la palabra con la etiqueta adecuada

    # Parsear el texto XML
    root = ET.fromstring(xml_text)

    # Recorrer todos los elementos <ANNOTATION_VALUE>
    for annotation_value in root.findall('.//ANNOTATION_VALUE'):
        original_text = annotation_value.text
        if original_text:
            # Transformar el texto en cada <ANNOTATION_VALUE>
            transformed_text = uppercase_pattern.sub(replace_with_tag, original_text)
            annotation_value.text = transformed_text

    # Retornar el texto XML modificado como string
    return ET.tostring(root, encoding='unicode')


# Ejemplo de uso
xml_text_example = '''
<ANNOTATION_DOCUMENT>
    <ANNOTATION>
        <ANNOTATION_VALUE>-quiero ir MAÑANA ¿me entiendes?</ANNOTATION_VALUE>
    </ANNOTATION>
    <ANNOTATION>
        <ANNOTATION_VALUE>Otro ejemplo SIN transformar.</ANNOTATION_VALUE>
    </ANNOTATION>
</ANNOTATION_DOCUMENT>
'''

transformed_xml_text = transform_uppercase_in_annotation_value(xml_text_example)
print(transformed_xml_text)


# save_to_file(elan_text_corrected, 'output_corrected_elan.xml')

# Puedes guardar el texto en un archivo si lo deseas, usando un bloque with open como en el ejemplo anterior.


def save_to_file(text, file_path):
    """
    Guarda el texto dado en el archivo especificado.

    :param text: Texto a guardar.
    :param file_path: Ruta del archivo donde se guardará el texto.
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text)
    print(f"Archivo guardado en: {file_path}")


# Aplicar la conversión solo en las partes necesarias del texto ELAN
elan_text_converted = convert_chars_in_annotation_value(elan_text)

#Aplicar conversión de mayúsculas a Énfasis
elan_filtered = transform_uppercase_in_annotation_value(elan_text_converted)

# Especifica la ruta donde deseas guardar el archivo
output_file_path = 'D:\\Sara\\Curso 2023-2024\\Proyecto DIA XX\\Conversaciones Oralia\\Conversaciones sin audio\\1994.PT.74 - IM339\\textoelan.xml'

# Usar la función save_to_file para guardar el texto ELAN generado
save_to_file(elan_filtered, output_file_path)