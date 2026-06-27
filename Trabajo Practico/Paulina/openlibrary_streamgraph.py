import requests
import pandas as pd
import time

# =========================
# CONFIGURACIÓN
# =========================

START_YEAR = 1900
END_YEAR = 2026
DECADE_STEP = 10

LANGUAGE = "eng"  # eng = inglés, spa = español, fre = francés, etc.

GENRES = [
    "fantasy",
    "romance",
    "mystery",
    "horror",
    "science fiction",
    "historical fiction",
    "adventure",
    "dystopian"
]

OUTPUT_FILE = "openlibrary_generos_por_decada.csv"

# =========================
# FUNCIÓN PARA CONSULTAR OPENLIBRARY
# =========================

def get_openlibrary_count(genre, start_year, end_year, language="eng"):
    """
    Retorna la cantidad de obras encontradas en OpenLibrary
    para un género y rango de años determinado.
    """

    url = "https://openlibrary.org/search.json"

    query = (
        f'subject:"{genre}" '
        f'language:{language} '
        f'first_publish_year:[{start_year} TO {end_year}]'
    )

    params = {
        "q": query,
        "fields": "key,title,first_publish_year",
        "limit": 1
    }

    try:
        response = requests.get(url, params=params, timeout=20)
        response.raise_for_status()
        data = response.json()
        return data.get("num_found", 0)

    except requests.RequestException as e:
        print(f"Error consultando {genre} ({start_year}-{end_year}): {e}")
        return 0


# =========================
# GENERAR CSV PARA FLOURISH
# =========================

rows = []

for decade_start in range(START_YEAR, END_YEAR + 1, DECADE_STEP):
    decade_end = min(decade_start + 9, END_YEAR)

    row = {
        "Row Labels": decade_start
    }

    print(f"\nProcesando década {decade_start}-{decade_end}...")

    for genre in GENRES:
        count = get_openlibrary_count(
            genre=genre,
            start_year=decade_start,
            end_year=decade_end,
            language=LANGUAGE
        )

        pretty_genre = genre.title()
        row[pretty_genre] = count

        print(f"  {pretty_genre}: {count}")

        time.sleep(0.4)  # Para no saturar la API

    rows.append(row)

df = pd.DataFrame(rows)

df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

print("\nCSV generado correctamente:")
print(OUTPUT_FILE)
print(df)