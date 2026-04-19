import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Estilo visual
sns.set_theme(style="whitegrid")

# Cargar dataset (ruta robusta)
data_path = Path(__file__).resolve().parents[1] / "data" / "books_1.Best_Books_Ever.csv"
df = pd.read_csv(data_path)

# Construcción de variables necesarias para los criterios
genres_raw = df["genres"].fillna("").astype(str)
df["genre"] = genres_raw.str.extract(r"['\"]([^'\"]+)['\"]", expand=False).str.strip()
df["genre"] = df["genre"].fillna(genres_raw.str.split("|", regex=False).str[0].str.strip())
df["rating"] = pd.to_numeric(df["rating"], errors="coerce")

year_first = pd.to_numeric(
	df["firstPublishDate"].astype(str).str.extract(r"(\d{4})")[0],
	errors="coerce"
)
year_publish = pd.to_numeric(
	df["publishDate"].astype(str).str.extract(r"(\d{4})")[0],
	errors="coerce"
)
df["year"] = year_first.fillna(year_publish)

# Limpiar datos
df = df.dropna(subset=["genre", "rating", "year"])
df = df[df["genre"].str.strip() != ""]
df = df[~df["genre"].str.strip().isin(["[]", "nan", "None"])]
df["year"] = df["year"].astype(int)
df = df[(df["year"] >= 1960) & (df["year"] <= 2026)]

if df.empty:
	raise ValueError("No hay datos suficientes para construir el gráfico con género, rating y año.")

# Criterio 1: ranking por cantidad de novelas por género y década
df["decade"] = (df["year"] // 10) * 10
df = df[df["decade"] >= 1960]

# Top géneros globales para legibilidad
top_n_genres = 8
top_genres = df["genre"].value_counts().head(top_n_genres).index
df = df[df["genre"].isin(top_genres)].copy()

# Agregado por década y género
agg = (
	df.groupby(["decade", "genre"], observed=False)
	.agg(
		novels_count=("title", "size"),
		avg_rating=("rating", "mean")
	)
	.reset_index()
)

# Completar combinaciones faltantes para ranking consistente
all_decades = sorted(agg["decade"].unique())
index = pd.MultiIndex.from_product([all_decades, top_genres], names=["decade", "genre"])
agg = (
	agg.set_index(["decade", "genre"])
	.reindex(index)
	.fillna({"novels_count": 0, "avg_rating": 0})
	.reset_index()
)

# Ranking por década (1 = más novelas)
agg["rank"] = agg.groupby("decade")["novels_count"].rank(method="dense", ascending=False)

# Para marcadores: tamaño por rating promedio
valid_rating = agg["avg_rating"].where(agg["avg_rating"] > 0)
min_r = valid_rating.min() if valid_rating.notna().any() else 0
max_r = valid_rating.max() if valid_rating.notna().any() else 5

def rating_to_size(rating_value):
	if rating_value <= 0 or max_r == min_r:
		return 60
	norm = (rating_value - min_r) / (max_r - min_r)
	return 80 + norm * 260

# Gráfico: Bump chart
fig, ax = plt.subplots(figsize=(15, 9))

palette = sns.color_palette("husl", n_colors=len(top_genres))
color_map = dict(zip(top_genres, palette))

for genre in top_genres:
	sub = agg[agg["genre"] == genre].sort_values("decade")

	ax.plot(
		sub["decade"],
		sub["rank"],
		color=color_map[genre],
		linewidth=2.2,
		alpha=0.9,
		label=genre,
	)

	ax.scatter(
		sub["decade"],
		sub["rank"],
		c=sub["avg_rating"],
		cmap="viridis",
		vmin=max(1.0, min_r if min_r > 0 else 1.0),
		vmax=max_r if max_r > 0 else 5.0,
		s=sub["avg_rating"].apply(rating_to_size),
		edgecolors="white",
		linewidths=0.9,
		zorder=3,
	)

# Ajustes visuales
ax.set_title(
	"Bump chart por década: ranking de géneros (cantidad) y rating promedio",
	fontsize=14
)
ax.set_xlabel("Década")
ax.set_ylabel("Ranking de cantidad (1 = mayor)")
ax.invert_yaxis()
ax.set_xticks(all_decades)

# Colorbar de rating promedio
mappable = plt.cm.ScalarMappable(cmap="viridis")
mappable.set_array(agg["avg_rating"])
cb = plt.colorbar(mappable, ax=ax, pad=0.02)
cb.set_label("Rating promedio")

# Leyenda de líneas (géneros)
ax.legend(
	title=f"Top {top_n_genres} géneros",
	loc="upper left",
	bbox_to_anchor=(1.12, 1),
	borderaxespad=0,
)

plt.tight_layout()
output_path = Path(__file__).resolve().with_name("bumpchart_genero_decada_rating.png")
plt.savefig(output_path, dpi=300, bbox_inches="tight")

backend_name = plt.get_backend().lower()
if "agg" in backend_name:
    try:
        plt.switch_backend("TkAgg")
    except Exception:
        print(f"Gráfico guardado en: {output_path}")
        print("No se pudo abrir ventana interactiva con el backend actual.")

plt.show()
