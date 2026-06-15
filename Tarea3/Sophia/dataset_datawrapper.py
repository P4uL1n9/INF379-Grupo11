import csv
import sys
from collections import Counter

csv.field_size_limit(sys.maxsize)

archivo_csv = "Tarea3/Sophia/dataset/nobel-prize-laureates.csv"
archivo_salida = "Tarea3/Sophia/datos_datawrapper.csv"

codigos_paises = []

try:
    with open(archivo_csv, mode="r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file, delimiter=";")
        for fila in reader:
            if fila.get("Category", "").strip().lower() == "literature":
                codigo = fila.get("Born country code", "").strip().upper()
                if codigo:
                    codigos_paises.append(codigo)

    conteo = Counter(codigos_paises)

    with open(archivo_salida, mode="w", encoding="utf-8", newline="") as file_out:
        writer = csv.writer(file_out)
        writer.writerow(["Codigo_Pais", "Cantidad_Premios"])
        for pais, cantidad in conteo.most_common():
            writer.writerow([pais, cantidad])

    print(f"¡Hecho! Archivo ultraliviano generado en: '{archivo_salida}'")

except Exception as e:
    print(f"Error: {e}")