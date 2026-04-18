import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

# Estilo visual
sns.set_theme(style="whitegrid")

# Cargar dataset (ruta robusta)
data_path = Path(__file__).resolve().parents[1] / "data" / "books_1.Best_Books_Ever.csv"
df = pd.read_csv(data_path)

# Construcción de variables necesarias para los criterios
df["pages"] = pd.to_numeric(
    df["pages"].astype(str).str.extract(r"(\d+)")[0],
    errors="coerce"
)
genres_raw = df["genres"].fillna("").astype(str)
df["genre"] = genres_raw.str.extract(r"['\"]([^'\"]+)['\"]", expand=False).str.strip()
df["genre"] = df["genre"].fillna(genres_raw.str.split("|", regex=False).str[0].str.strip())
df["rating"] = pd.to_numeric(df["rating"], errors="coerce")

# Limpiar datos
df = df.dropna(subset=["genre", "pages", "rating"])
df = df[df["genre"].str.strip() != ""]
df = df[~df["genre"].str.strip().isin(["[]", "nan", "None"])]

if df.empty:
    raise ValueError("No hay datos suficientes para construir el gráfico con género, rating y páginas.")

# Bins de rating para eje X
rating_bins = [0, 3.0, 3.5, 4.0, 4.5, 5.1]
rating_labels = ["0-3.0", "3.0-3.5", "3.5-4.0", "4.0-4.5", "4.5-5.0"]

df["rating_bin"] = pd.cut(
    df["rating"],
    bins=rating_bins,
    labels=rating_labels,
    right=False,
    include_lowest=True
)
df = df.dropna(subset=["rating_bin"])

# Reducir ruido visual: top 12 géneros con más novelas
count_data = (
    df.groupby(["genre", "rating_bin"], observed=False)
    .size()
    .reset_index(name="count")
)

top_genres = count_data.groupby("genre")["count"].sum().nlargest(12).index
df = df[df["genre"].isin(top_genres)].copy()

# Datos para la matriz híbrida
bubble_data = (
    df.groupby(["genre", "rating_bin"], observed=False)
    .agg(
        count=("title", "size"),
        avg_pages=("pages", "mean"),
    )
    .reset_index()
)

bubble_data = bubble_data[bubble_data["count"] > 0].copy()

bubble_data["rating_bin"] = pd.Categorical(
    bubble_data["rating_bin"],
    categories=rating_labels,
    ordered=True
)

# Ordenar géneros por frecuencia total
genre_order = (
    bubble_data.groupby("genre")["count"]
    .sum()
    .sort_values(ascending=False)
    .index
)

bubble_data["genre"] = pd.Categorical(
    bubble_data["genre"],
    categories=genre_order,
    ordered=True
)

# Matrices para heatmap y burbujas
avg_pages_matrix = (
    bubble_data.pivot(index="genre", columns="rating_bin", values="avg_pages")
    .reindex(index=genre_order, columns=rating_labels)
)

count_matrix = (
    bubble_data.pivot(index="genre", columns="rating_bin", values="count")
    .reindex(index=genre_order, columns=rating_labels)
    .fillna(0)
)

fig, ax1 = plt.subplots(figsize=(14, 8))

# Heatmap: páginas promedio
sns.heatmap(
    avg_pages_matrix,
    ax=ax1,
    cmap="YlOrRd",
    linewidths=0.8,
    linecolor="white",
    cbar_kws={"label": "Páginas promedio"},
    mask=avg_pages_matrix.isna(),
)

# Preparar burbujas
counts_flat = count_matrix.to_numpy().flatten()
non_zero_counts = counts_flat[counts_flat > 0]
max_count = non_zero_counts.max() if non_zero_counts.size > 0 else 1

x_positions = []
y_positions = []
sizes = []
count_labels = []

for row_idx, genre in enumerate(count_matrix.index):
    for col_idx, rating_bin in enumerate(count_matrix.columns):
        count_value = count_matrix.loc[genre, rating_bin]
        if count_value > 0:
            x_positions.append(col_idx + 0.5)
            y_positions.append(row_idx + 0.5)
            sizes.append((np.sqrt(count_value / max_count)) * 1300 + 80)
            count_labels.append(int(count_value))

# Burbujas
ax1.scatter(
    x_positions,
    y_positions,
    s=sizes,
    facecolors="#1f2937",
    edgecolors="#f9fafb",
    linewidths=1.5,
    alpha=0.85,
)

# Etiquetas dentro de burbujas
for x_pos, y_pos, label in zip(x_positions, y_positions, count_labels):
    ax1.text(
        x_pos,
        y_pos,
        str(label),
        ha="center",
        va="center",
        fontsize=7,
        color="white",
        fontweight="bold",
    )

ax1.set_title(
    "Matriz híbrida: género vs rango de rating (cantidad y páginas promedio)",
    fontsize=14
)
ax1.set_xlabel("Rango de rating")
ax1.set_ylabel("Género principal")

# Leyenda de tamaños (a la izquierda, fuera del gráfico)
if non_zero_counts.size > 0:
    size_levels = sorted({
        int(v) for v in np.quantile(non_zero_counts, [0.25, 0.5, 0.75]).round() if v >= 1
    })

    if size_levels:
        size_handles = [
            ax1.scatter(
                [],
                [],
                s=(np.sqrt(level / max_count)) * 1300 + 80,
                facecolors="#1f2937",
                edgecolors="#f9fafb",
                linewidths=1.2,
                alpha=0.85
            )
            for level in size_levels
        ]

        ax1.legend(
            size_handles,
            [str(level) for level in size_levels],
            title="Cantidad novelas",
            loc="upper left",
            bbox_to_anchor=(-0.27, 1.0),
            frameon=True,
            borderaxespad=0.0
        )

plt.subplots_adjust(left=0.25)

plt.tight_layout()
output_path = Path(__file__).resolve().with_name("matriz_hibrida_genero_rating.png")
plt.savefig(output_path, dpi=300, bbox_inches="tight")

backend_name = plt.get_backend().lower()
if "agg" in backend_name:
    try:
        plt.switch_backend("TkAgg")
    except Exception:
        print(f"Gráfico guardado en: {output_path}")
        print("No se pudo abrir ventana interactiva con el backend actual.")

plt.show()