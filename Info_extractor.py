from pympi.Elan import Eaf
import pandas as pd

# Cargar el archivo .eaf
file_path = "D:\\Sara\\2023-2024\\Proyecto DIA XX\\Copia de seguridad Val.Es.Co\\Prototípicas\\segmentadas\\prueba para Python.eaf"  # Ajusta la ruta según tu archivo
eaf_obj = Eaf(file_path)

# Imprimir la estructura básica del archivo .eaf
print("Tiers disponibles en el archivo:")
for tier in eaf_obj.get_tier_names():
    print(tier)

# Mostrar algunas anotaciones de ejemplo de cada Tier
for tier in eaf_obj.get_tier_names():
    print(f"\nAnotaciones para el Tier {tier}:")
    annotations = eaf_obj.get_annotation_data_for_tier(tier)
    for annotation in annotations:  # Mostrar las primeras 5 anotaciones
        print(annotation)


