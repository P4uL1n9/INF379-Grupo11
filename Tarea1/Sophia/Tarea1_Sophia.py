import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from pathlib import Path

# Estilo visual base
sns.set_theme(style="whitegrid")

# Cargar dataset (ruta robusta)
data_path = Path(__file__).resolve().parents[1] / "data" / "books_1.Best_Books_Ever.csv"
df = pd.read_csv(data_path)

# Rating numérico
df["rating"] = pd.to_numeric(df["rating"], errors="coerce")

# Extraer género principal
genres_raw = df["genres"].fillna("").astype(str)
df["genre"] = genres_raw.str.extract(r"['\"]([^'\"]+)['\"]", expand=False).str.strip()
df["genre"] = df["genre"].fillna(genres_raw.str.split("|", regex=False).str[0].str.strip())

# Extraer año desde firstPublishDate y, si falta, usar publishDate
year_first = pd.to_numeric(
	df["firstPublishDate"].astype(str).str.extract(r"(\d{4})")[0],
	errors="coerce",
)
year_publish = pd.to_numeric(
	df["publishDate"].astype(str).str.extract(r"(\d{4})")[0],
	errors="coerce",
)
df["year"] = year_first.fillna(year_publish)

# Limpiar datos mínimos
df = df.dropna(subset=["year", "genre"])
df = df[df["genre"].str.strip() != ""]
df = df[~df["genre"].str.strip().isin(["[]", "nan", "None"])]
df["year"] = df["year"].astype(int)
df = df[(df["year"] >= 1960) & (df["year"] <= 2026)]

if df.empty:
	raise ValueError("No hay datos suficientes para construir el gráfico por año y género.")

# Limitar cantidad de géneros para legibilidad del streamgraph
top_n_genres = 10
top_genres = df["genre"].value_counts().head(top_n_genres).index
df_top = df[df["genre"].isin(top_genres)].copy()

# Criterio 1: cantidad de novelas por año y género
count_by_year_genre = (
	df_top.groupby(["year", "genre"]).size().reset_index(name="novel_count")
)
stream_data = (
	count_by_year_genre.pivot(index="year", columns="genre", values="novel_count")
	.fillna(0)
	.sort_index()
)

# Criterio 2: rating promedio por año
rating_by_year = (
	df.dropna(subset=["rating"])
	.groupby("year")["rating"]
	.mean()
	.sort_index()
)

# Alinear años entre ambas series para superponer bien el gráfico
common_years = stream_data.index.intersection(rating_by_year.index)
stream_data = stream_data.loc[common_years]
rating_by_year = rating_by_year.loc[common_years]

if stream_data.empty or rating_by_year.empty:
	raise ValueError("No hay intersección de años suficiente para graficar streamgraph y rating promedio.")

# Graficar
fig, ax1 = plt.subplots(figsize=(15, 8))

palette = sns.color_palette("tab10", n_colors=stream_data.shape[1])
ax1.stackplot(
	stream_data.index,
	stream_data.T.values,
	labels=stream_data.columns,
	baseline="zero",  # Streamgraph clásico
	colors=palette,
	alpha=0.85,
)

ax1.set_xlabel("Año")
ax1.set_ylabel("Cantidad de novelas")
ax1.set_title("Streamgraph: cantidad de novelas por año y género + rating promedio anual")

# Eje secundario para rating promedio
ax2 = ax1.twinx()
ax2.plot(
	rating_by_year.index,
	rating_by_year.values,
	color="black",
	linewidth=2.4,
	marker="o",
	markersize=3.5,
	label="Rating promedio por año",
)
ax2.set_ylabel("Rating promedio")
ax2.set_ylim(0, 5)

# Leyendas (géneros y línea de rating)
ax1.legend(
	title=f"Top {top_n_genres} géneros",
	loc="upper left",
	bbox_to_anchor=(1.05, 1),
	borderaxespad=0,
)
ax2.legend(loc="upper left", bbox_to_anchor=(1.05, 0.55), borderaxespad=0)

plt.tight_layout()

output_path = Path(__file__).resolve().with_name("streamgraph_novelas_rating.png")
plt.savefig(output_path, dpi=300, bbox_inches="tight")

backend_name = plt.get_backend().lower()
if "agg" in backend_name:
    try:
        plt.switch_backend("TkAgg")
    except Exception:
        print(f"Gráfico guardado en: {output_path}")
        print("No se pudo abrir ventana interactiva con el backend actual.")

plt.show()


# ================================================
# GRÁFICO ZOOM: Zona de interés (1990-2020)
# ================================================
zoom_start, zoom_end = 1990, 2020

# Filtramos solo los años relevantes
zoom_mask = (stream_data.index >= zoom_start) & (stream_data.index <= zoom_end)
stream_zoom = stream_data.loc[zoom_mask]
rating_zoom = rating_by_year.loc[rating_by_year.index.isin(stream_zoom.index)]

if not stream_zoom.empty and not rating_zoom.empty:
    fig_zoom, ax1z = plt.subplots(figsize=(14, 7))

    ax1z.stackplot(
        stream_zoom.index,
        stream_zoom.T.values,
        labels=stream_zoom.columns,
        baseline="zero",
        colors=palette,
        alpha=0.85,
    )

    ax1z.set_xlabel("Año")
    ax1z.set_ylabel("Cantidad de novelas")
    ax1z.set_title("Streamgraph ZOOM: Cantidad de novelas por año y género (1990-2020) + rating promedio anual")
    ax1z.grid(True, linestyle="--", alpha=0.4)

    # Eje secundario (rating)
    ax2z = ax1z.twinx()
    ax2z.plot(
        rating_zoom.index,
        rating_zoom.values,
        color="black",
        linewidth=2.4,
        marker="o",
        markersize=4,
        label="Rating promedio por año",
    )
    ax2z.set_ylabel("Rating promedio")
    ax2z.set_ylim(0, 5)

    # Leyendas
    ax1z.legend(
        title=f"Top {top_n_genres} géneros",
        loc="upper left",
        bbox_to_anchor=(1.05, 1),
        borderaxespad=0,
    )
    ax2z.legend(loc="upper left", bbox_to_anchor=(1.05, 0.55), borderaxespad=0)

	# === AÑOS EXACTOS DE INTERÉS (calculados automáticamente del dato) ===
    total_by_year = stream_zoom.sum(axis=1)

    # Pico 1: máximo aproximado cerca del 2005
    peak1_year = total_by_year.loc[2000:2010].idxmax()

    # Baja: mínimo entre 2005 y 2010
    dip_year = total_by_year.loc[2005:2010].idxmin()

    # Pico 2: máximo entre 2010 y 2015
    peak2_year = total_by_year.loc[2010:2015].idxmax()

    print(f"📍 Pico 1 detectado exactamente en: {peak1_year}")
    print(f"📍 Baja detectada exactamente en: {dip_year}")
    print(f"📍 Pico 2 detectado exactamente en: {peak2_year}")

    # Dibujar las 3 líneas verticales en el gráfico
    ax1z.axvline(peak1_year, color='purple', linestyle='--', linewidth=2.2, alpha=0.9, label=f'Alza 1 ({peak1_year})')
    ax1z.axvline(dip_year, color='yellow', linestyle='--', linewidth=2.2, alpha=0.9, label=f'Baja ({dip_year})')
    ax1z.axvline(peak2_year, color='purple', linestyle='--', linewidth=2.2, alpha=0.9, label=f'Alza 2 ({peak2_year})')

    # Actualizar leyenda para que incluya las líneas verticales
    ax1z.legend(
        title=f"Top {top_n_genres} géneros + puntos clave",
        loc="upper left",
        bbox_to_anchor=(1.05, 1),
        borderaxespad=0,
    )
    
	# Leyenda del rating ahora en la esquina superior derecha (dentro del gráfico)
    ax2z.legend(
        loc="upper right",
        bbox_to_anchor=(0.98, 0.95),
        borderaxespad=0,
        frameon=True,
        facecolor="white",
        edgecolor="gray",
        fontsize=9
    )

    plt.tight_layout()

    output_zoom = Path(__file__).resolve().with_name("streamgraph_novelas_rating_ZOOM_1990-2020.png")
    plt.savefig(output_zoom, dpi=300, bbox_inches="tight")
    print(f"✅ Gráfico ZOOM guardado en: {output_zoom}")

    plt.show()
else:
    print("⚠️ No hay datos suficientes para generar el gráfico zoom.")