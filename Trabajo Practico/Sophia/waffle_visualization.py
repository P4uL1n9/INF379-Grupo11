
# =============================================================================
# Waffle Chart: Idiomas de TODOS los libros del dataset
# Dataset REAL: Goodreads Best Books Ever
# =============================================================================

import pandas as pd
import matplotlib.pyplot as plt
from pywaffle import Waffle
import os
import glob

# 1. Leer el dataset real descargado
cache_dir = os.path.expanduser("~/.cache/kagglehub/datasets/thedevastator/comprehensive-overview-of-52478-goodreads-best-b")
csv_files = glob.glob(os.path.join(cache_dir, '**', '*.csv'), recursive=True)

if not csv_files:
    print("Error: No se encontró el dataset.")
    exit(1)

dataset_path = csv_files[0]
print(f"Leyendo datos reales de: {dataset_path}")

df = pd.read_csv(dataset_path)

# 2. Limpiar datos (Se eliminan nulos, pero se mantienen TODOS los registros)
df = df.dropna(subset=['numRatings', 'language'])

# 3. CREAR EL ARCHIVO CSV CON TODOS LOS DATOS
csv_output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'todos_los_libros_goodreads.csv')
df.to_csv(csv_output_path, index=False)
print(f"\nArchivo CSV generado exitosamente en: {csv_output_path}")

# Mapear idiomas para mejor lectura
language_map = {
    'English': 'Inglés',
    'Spanish': 'Español',
    'French': 'Francés',
    'German': 'Alemán'
}
df['language_es'] = df['language'].map(lambda x: language_map.get(x, x))

lang_counts = df['language_es'].value_counts()

# --- LÓGICA DE FILTRADO POR PORCENTAJE (< 1%) ---
total_libros = lang_counts.sum()
umbral_porcentaje = 0.01  # 1%

# Separar los que son mayores o iguales al 1% y los que son menores
idiomas_mayores = lang_counts[lang_counts / total_libros >= umbral_porcentaje]
suma_idiomas_menores = lang_counts[lang_counts / total_libros < umbral_porcentaje].sum()

# Construir el diccionario final para el Waffle Chart
data_waffle = idiomas_mayores.to_dict()
if suma_idiomas_menores > 0:
    data_waffle['Otros'] = suma_idiomas_menores

print(f"\nResultados procesados para el catálogo completo ({total_libros} libros):")
for k, v in data_waffle.items():
    print(f"{k}: {v} libros ({v/total_libros*100:.2f}%)")

# --- ASIGNACIÓN DINÁMICA DE COLORES ---
# Paleta de colores vivos para los idiomas principales
paleta_colores = ['#1A237E', '#26A69A', '#FF7043', '#C2185B', '#AB47BC', '#00838F', '#D4E157']
colors = []
color_idx = 0

for idioma in data_waffle.keys():
    if idioma == 'Otros':
        colors.append('#9E9E9E')  # Gris fijo para la categoría "Otros"
    else:
        colors.append(paleta_colores[color_idx % len(paleta_colores)])
        color_idx += 1

# 4. Generar el Waffle Chart
fig = plt.figure(
    FigureClass=Waffle,
    rows=10,
    columns=10,
    values=data_waffle,
    colors=colors,
    legend={'loc': 'upper left', 'bbox_to_anchor': (1.05, 1), 'fontsize': 12, 'frameon': False},
    title={
        'label': 'Diversidad Lingüística en Goodreads\nIdiomas de publicación de todos los libros del dataset',
        'loc': 'left', 
        'fontsize': 16, 
        'fontweight': 'bold', 
        'pad': 20, 
        'color': '#333333'
    },
    labels=[f"{k} ({v/sum(data_waffle.values())*100:.1f}%)" for k, v in data_waffle.items()],
    figsize=(11, 6)
)

fig.patch.set_facecolor('#FAFAFA')

# Nota al pie adaptada para la totalidad de los datos
plt.text(
    0, -0.15,
    'Cada cuadrado representa el 1% del total global de libros. Fuente real: Goodreads Best Books Ever.',
    fontsize=10, color='#666666', fontstyle='italic',
    transform=plt.gca().transAxes
)

# Guardar
output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'waffle_idiomas_total.png')
plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#FAFAFA')

output_path_hq = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'waffle_idiomas_total_HQ.png')
plt.savefig(output_path_hq, dpi=600, bbox_inches='tight', facecolor='#FAFAFA')

print("\nVisualización completa de todo el dataset ejecutada con éxito.")