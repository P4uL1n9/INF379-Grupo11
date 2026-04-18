import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar dataset
df = pd.read_csv("../data/books.csv")

# Limpiar datos básicos
df = df.dropna(subset=["year", "genre", "pages"])
df["year"] = df["year"].astype(int)

# --- CRITERIO 1: Cantidad por año y género ---
count_data = df.groupby(["year", "genre"]).size().reset_index(name="count")

# Pivot para heatmap
heatmap_data = count_data.pivot(index="genre", columns="year", values="count").fillna(0)

plt.figure(figsize=(12,6))
sns.heatmap(heatmap_data, cmap="viridis")
plt.title("Cantidad de novelas por género a lo largo del tiempo")
plt.xlabel("Año")
plt.ylabel("Género")
plt.show()