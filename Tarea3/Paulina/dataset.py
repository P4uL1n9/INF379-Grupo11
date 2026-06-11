import requests
import pandas as pd
import time

PAISES = {
    "Chile": (-35.6751, -71.5430),
    "Argentina": (-38.4161, -63.6167),
    "Brazil": (-14.2350, -51.9253),
    "Mexico": (23.6345, -102.5528),
    "Colombia": (4.5709, -74.2973),
    "Peru": (-9.1900, -75.0152),
    "Spain": (40.4637, -3.7492),
    "France": (46.2276, 2.2137),
    "Germany": (51.1657, 10.4515),
    "Italy": (41.8719, 12.5674),
    "United Kingdom": (55.3781, -3.4360),
    "United States": (37.0902, -95.7129),
    "Canada": (56.1304, -106.3468),
    "Japan": (36.2048, 138.2529),
    "China": (35.8617, 104.1954),
    "India": (20.5937, 78.9629),
    "Russia": (61.5240, 105.3188),
    "Australia": (-25.2744, 133.7751),
    "South Africa": (-30.5595, 22.9375),
    "Nigeria": (9.0820, 8.6753)
}

ANIOS = range(2020, 2027)

def contar_novelas_por_anio(pais, anio):
    url = "https://openlibrary.org/search.json"

    params = {
        "subject": "fiction",
        "place": pais,
        "publish_year": anio,
        "limit": 1
    }

    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()

        data = response.json()

        return data.get("numFound", 0)

    except Exception as e:
        print(f"Error con {pais} en {anio}: {e}")
        return 0

resultado = []

for pais, (latitud, longitud) in PAISES.items():
    print(f"Consultando {pais}...")

    total_pais = 0

    for anio in ANIOS:
        cantidad = contar_novelas_por_anio(pais, anio)
        total_pais += cantidad
        time.sleep(0.3)

    resultado.append({
        "pais": pais,
        "latitud": latitud,
        "longitud": longitud,
        "cantidad_novelas_2020_2026": total_pais
    })

df = pd.DataFrame(resultado)

df = df.sort_values(
    by="cantidad_novelas_2020_2026",
    ascending=False
)

df.to_csv(
    "novelas_por_pais_2020_2026.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nDataset generado correctamente:")
print(df)

print(f"\nTotal de países analizados: {len(df)}")
print(f"Total de novelas encontradas: {df['cantidad_novelas_2020_2026'].sum()}")