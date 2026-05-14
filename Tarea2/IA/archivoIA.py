from pathlib import Path
import unicodedata

import pandas as pd
import plotly.express as px


BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR.parent / "data" / "ResultadosEncuestaLibros.csv"
OUTPUT_HTML = BASE_DIR / "grafico_radar_generos.html"


def normalizar(texto: str) -> str:
    """Normaliza texto para comparar nombres de columnas sin depender de tildes."""
    if pd.isna(texto):
        return ""
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


def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"No se encontró el archivo de datos en: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH, encoding="utf-8-sig")

    col_frecuencia = encontrar_columna(df, "seguido lees novelas o libros por gusto")

    # Usaremos los géneros literarios, excluyendo explícitamente los criterios de selección
    generos_objetivo = {
        "Romance",
        "Misterio / Thriller",
        "Fantasía",
        "Ciencia ficción",
        "Terror",
        "Drama",
        "Historias basadas en hechos reales",
        "No suelo leer",
    }

    normalizados_objetivo = {normalizar(nombre) for nombre in generos_objetivo}
    columnas_genero = [
        columna
        for columna in df.columns
        if normalizar(columna) in normalizados_objetivo
    ]

    if not columnas_genero:
        raise ValueError("No se encontraron columnas de géneros para construir el gráfico.")

    # Pasar de ancho a largo para agrupar
    data_larga = df[[col_frecuencia] + columnas_genero].melt(
        id_vars=[col_frecuencia],
        value_vars=columnas_genero,
        var_name="Género",
        value_name="Seleccionado",
    )

    # Filtrar aquellos que efectivamente seleccionaron la opción
    data_larga = data_larga[
        data_larga["Seleccionado"].notna()
        & (data_larga["Seleccionado"].astype(str).str.strip() != "")
    ].copy()

    data_larga["Frecuencia de lectura"] = data_larga[col_frecuencia].astype(str).str.strip()

    # Contar cuántas personas de cada frecuencia leen cada género
    conteo = (
        data_larga.groupby(["Frecuencia de lectura", "Género"])
        .size()
        .reset_index(name="Cantidad")
    )

    # Crear gráfico de Radar (Polar Line)
    fig = px.line_polar(
        conteo,
        r="Cantidad",
        theta="Género",
        color="Frecuencia de lectura",
        line_close=True,
        markers=True,
        title="Preferencias de géneros literarios según frecuencia de lectura (Gráfico de Radar)",
        color_discrete_sequence=px.colors.qualitative.Dark24
    )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, showticklabels=True),
        ),
        margin=dict(l=60, r=60, t=80, b=60),
        font=dict(size=12)
    )

    fig.write_html(OUTPUT_HTML, include_plotlyjs="cdn")

    print(f"Gráfico de radar guardado en: {OUTPUT_HTML}")
    print(f"Respuestas procesadas: {len(df)}")
    print(f"Combinaciones agregadas en el radar: {len(conteo)}")


if __name__ == "__main__":
    main()
