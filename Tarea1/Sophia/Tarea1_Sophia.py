import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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
	print(f"Gráfico guardado en: {output_path}")
	print("Backend no interactivo detectado; no se abrirá ventana de visualización.")
else:
	plt.show()
