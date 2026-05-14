from pathlib import Path
import unicodedata

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data"
DATA_PATH = DATA_DIR / "ResultadosEncuestaLibros.csv"
OUTPUT_CSV = DATA_DIR / "sunburst_criterios_data.csv"


def normalizar(texto: str) -> str:
	"""Normaliza texto para comparar nombres de columnas sin depender de tildes."""
	return (
		unicodedata.normalize("NFKD", str(texto))
		.encode("ascii", "ignore")
		.decode("ascii")
		.lower()
		.strip()
	)


def encontrar_columna(df: pd.DataFrame, fragmento: str) -> str:
	fragmento_norm = normalizar(fragmento)
	for columna in df.columns:
		if fragmento_norm in normalizar(columna):
			return columna
	raise KeyError(f"No se encontró una columna que contenga: {fragmento}")


def valor_limpio(valor) -> str:
	if pd.isna(valor):
		return ""
	return str(valor).strip()


if not DATA_PATH.exists():
	raise FileNotFoundError(f"No se encontró el archivo de datos en: {DATA_PATH}")


df = pd.read_csv(DATA_PATH, encoding="utf-8-sig")

col_frecuencia = encontrar_columna(df, "seguido lees novelas o libros por gusto")
col_paginas = encontrar_columna(df, "rango de cantidad de paginas")

criterios_objetivo = {
	"La portada",
	"Recomendaciones de amigos o redes sociales",
	"La trama/sinopsis",
	"El autor",
	"Las reseñas o calificaciones",
	"Película, si es que tiene",
}

columnas_criterio = [
	columna
	for columna in df.columns
	if normalizar(columna) in {normalizar(nombre) for nombre in criterios_objetivo}
]

if not columnas_criterio:
	raise ValueError("No se encontraron columnas de criterios para construir el gráfico.")

data_larga = df[[col_frecuencia, col_paginas] + columnas_criterio].melt(
	id_vars=[col_frecuencia, col_paginas],
	value_vars=columnas_criterio,
	var_name="Criterio",
	value_name="Seleccionado",
)

data_larga = data_larga[
	data_larga["Seleccionado"].notna()
	& (data_larga["Seleccionado"].astype(str).str.strip() != "")
].copy()

respuestas_con_criterio = df[columnas_criterio].notna().any(axis=1) & (
	df[columnas_criterio].astype(str).apply(lambda serie: serie.str.strip()).ne("").any(axis=1)
)

data_larga["Frecuencia de lectura"] = data_larga[col_frecuencia].map(valor_limpio)
data_larga["Rango de páginas"] = data_larga[col_paginas].map(valor_limpio)
data_larga["Criterio"] = data_larga["Criterio"].map(valor_limpio)

conteo = (
	data_larga.groupby(["Frecuencia de lectura", "Criterio", "Rango de páginas"])
	.size()
	.reset_index(name="Cantidad")
)

OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
conteo.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")

print(f"CSV guardado en: {OUTPUT_CSV}")
print(f"Respuestas originales: {len(df)}")
print(f"Respuestas con al menos un criterio: {int(respuestas_con_criterio.sum())}")
print(f"Registros largos de criterio: {len(data_larga)}")
print(f"Combinaciones agregadas: {len(conteo)}")