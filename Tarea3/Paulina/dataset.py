import pandas as pd

# Datos consolidados de 50 novelas para la tarea de Visualización de Datos
datos_novelas = [
    # --- LATINOAMÉRICA ---
    {"Título": "Cien años de soledad", "Autor": "Gabriel García Márquez", "País Autor": "Colombia", "País Ambientación": "Colombia", "ISO_Alpha3": "COL", "Latitud": 4.5709, "Longitud": -74.2973, "Género": "Realismo Mágico", "Relación": "Nativo"},
    {"Título": "Pedro Páramo", "Autor": "Juan Rulfo", "País Autor": "México", "País Ambientación": "México", "ISO_Alpha3": "MEX", "Latitud": 23.6345, "Longitud": -102.5528, "Género": "Realismo Mágico", "Relación": "Nativo"},
    {"Título": "La casa de los espíritus", "Autor": "Isabel Allende", "País Autor": "Chile", "País Ambientación": "Chile", "ISO_Alpha3": "CHL", "Latitud": -35.6751, "Longitud": -71.5430, "Género": "Saga Familiar", "Relación": "Nativo"},
    {"Título": "Rayuela", "Autor": "Julio Cortázar", "País Autor": "Argentina", "País Ambientación": "Francia", "ISO_Alpha3": "FRA", "Latitud": 48.8566, "Longitud": 2.3522, "Género": "Boom Latinoamericano", "Relación": "Extranjero"},
    {"Título": "Ficciones", "Autor": "Jorge Luis Borges", "País Autor": "Argentina", "País Ambientación": "Argentina", "ISO_Alpha3": "ARG", "Latitud": -38.4161, "Longitud": -63.6167, "Género": "Fantasía Filosófica", "Relación": "Nativo"},
    {"Título": "El túnel", "Autor": "Ernesto Sabato", "País Autor": "Argentina", "País Ambientación": "Argentina", "ISO_Alpha3": "ARG", "Latitud": -34.6037, "Longitud": -58.3816, "Género": "Psicológica", "Relación": "Nativo"},
    {"Título": "La ciudad y los perros", "Autor": "Mario Vargas Llosa", "País Autor": "Perú", "País Ambientación": "Perú", "ISO_Alpha3": "PER", "Latitud": -12.0464, "Longitud": -77.0428, "Género": "Realismo", "Relación": "Nativo"},
    {"Título": "El alquimista", "Autor": "Paulo Coelho", "País Autor": "Brasil", "País Ambientación": "Egipto", "ISO_Alpha3": "EGY", "Latitud": 26.8206, "Longitud": 30.8025, "Género": "Fábula", "Relación": "Extranjero"},
    {"Título": "Los detectives salvajes", "Autor": "Roberto Bolaño", "País Autor": "Chile", "País Ambientación": "México", "ISO_Alpha3": "MEX", "Latitud": 19.4326, "Longitud": -99.1332, "Género": "Ficción", "Relación": "Extranjero"},
    {"Título": "Inés del alma mía", "Autor": "Isabel Allende", "País Autor": "Chile", "País Ambientación": "Chile", "ISO_Alpha3": "CHL", "Latitud": -33.4489, "Longitud": -70.6693, "Género": "Histórica", "Relación": "Nativo"},

    # --- EUROPA ---
    {"Título": "Don Quijote de la Mancha", "Autor": "Miguel de Cervantes", "País Autor": "España", "País Ambientación": "España", "ISO_Alpha3": "ESP", "Latitud": 40.4637, "Longitud": -3.7492, "Género": "Caballerías", "Relación": "Nativo"},
    {"Título": "Orgullo y Prejuicio", "Autor": "Jane Austen", "País Autor": "Reino Unido", "País Ambientación": "Reino Unido", "ISO_Alpha3": "GBR", "Latitud": 55.3781, "Longitud": -3.4360, "Género": "Romance", "Relación": "Nativo"},
    {"Título": "Crimen y castigo", "Autor": "Fiódor Dostoyevski", "País Autor": "Rusia", "País Ambientación": "Rusia", "ISO_Alpha3": "RUS", "Latitud": 59.9343, "Longitud": 30.3351, "Género": "Psicológica", "Relación": "Nativo"},
    {"Título": "Madame Bovary", "Autor": "Gustave Flaubert", "País Autor": "Francia", "País Ambientación": "Francia", "ISO_Alpha3": "FRA", "Latitud": 46.2276, "Longitud": 2.2137, "Género": "Realismo", "Relación": "Nativo"},
    {"Título": "Ulises", "Autor": "James Joyce", "País Autor": "Irlanda", "País Ambientación": "Irlanda", "ISO_Alpha3": "IRL", "Latitud": 53.3498, "Longitud": -6.2603, "Género": "Modernismo", "Relación": "Nativo"},
    {"Título": "Drácula", "Autor": "Bram Stoker", "País Autor": "Irlanda", "País Ambientación": "Rumanía", "ISO_Alpha3": "ROU", "Latitud": 46.7712, "Longitud": 23.6236, "Género": "Terror Gótico", "Relación": "Extranjero"},
    {"Título": "1984", "Autor": "George Orwell", "País Autor": "Reino Unido", "País Ambientación": "Reino Unido", "ISO_Alpha3": "GBR", "Latitud": 51.5074, "Longitud": -0.1278, "Género": "Distopía", "Relación": "Nativo"},
    {"Título": "Los miserables", "Autor": "Victor Hugo", "País Autor": "Francia", "País Ambientación": "Francia", "ISO_Alpha3": "FRA", "Latitud": 48.8566, "Longitud": 2.3522, "Género": "Drama Histórico", "Relación": "Nativo"},
    {"Título": "Frankenstein", "Autor": "Mary Shelley", "País Autor": "Reino Unido", "País Ambientación": "Suiza", "ISO_Alpha3": "CHE", "Latitud": 46.2044, "Longitud": 6.1432, "Género": "Terror", "Relación": "Extranjero"},
    {"Título": "Ana Karenina", "Autor": "León Tolstói", "País Autor": "Rusia", "País Ambientación": "Rusia", "ISO_Alpha3": "RUS", "Latitud": 55.7558, "Longitud": 37.6173, "Género": "Realismo", "Relación": "Nativo"},
    {"Título": "El proceso", "Autor": "Franz Kafka", "País Autor": "República Checa", "País Ambientación": "República Checa", "ISO_Alpha3": "CZE", "Latitud": 50.0755, "Longitud": 14.4378, "Género": "Existencialismo", "Relación": "Nativo"},
    {"Título": "El nombre de la rosa", "Autor": "Umberto Eco", "País Autor": "Italia", "País Ambientación": "Italia", "ISO_Alpha3": "ITA", "Latitud": 43.7696, "Longitud": 11.2558, "Género": "Misterio Histórico", "Relación": "Nativo"},
    {"Título": "Guerra y paz", "Autor": "León Tolstói", "País Autor": "Rusia", "País Ambientación": "Rusia", "ISO_Alpha3": "RUS", "Latitud": 55.7558, "Longitud": 37.6173, "Género": "Ficción Histórica", "Relación": "Nativo"},
    {"Título": "Cumbres Borrascosas", "Autor": "Emily Brontë", "País Autor": "Reino Unido", "País Ambientación": "Reino Unido", "ISO_Alpha3": "GBR", "Latitud": 53.8313, "Longitud": -1.9564, "Género": "Romance Gótico", "Relación": "Nativo"},
    {"Título": "El extranjero", "Autor": "Albert Camus", "País Autor": "Francia", "País Ambientación": "Argelia", "ISO_Alpha3": "DZA", "Latitud": 36.7538, "Longitud": 3.0588, "Género": "Existencialismo", "Relación": "Extranjero"},
    {"Título": "Ensayo sobre la ceguera", "Autor": "José Saramago", "País Autor": "Portugal", "País Ambientación": "Portugal", "ISO_Alpha3": "PRT", "Latitud": 38.7223, "Longitud": -9.1393, "Género": "Ficción Psicológica", "Relación": "Nativo"},
    {"Título": "Siddhartha", "Autor": "Hermann Hesse", "País Autor": "Alemania", "País Ambientación": "India", "ISO_Alpha3": "IND", "Latitud": 25.3176, "Longitud": 82.9739, "Género": "Filosófica", "Relación": "Extranjero"},
    {"Título": "La metamorfosis", "Autor": "Franz Kafka", "País Autor": "República Checa", "País Ambientación": "República Checa", "ISO_Alpha3": "CZE", "Latitud": 50.0755, "Longitud": 14.4378, "Género": "Absurdismo", "Relación": "Nativo"},
    {"Título": "Oliver Twist", "Autor": "Charles Dickens", "País Autor": "Reino Unido", "País Ambientación": "Reino Unido", "ISO_Alpha3": "GBR", "Latitud": 51.5074, "Longitud": -0.1278, "Género": "Drama Social", "Relación": "Nativo"},
    {"Título": "La sombra del viento", "Autor": "Carlos Ruiz Zafón", "País Autor": "España", "País Ambientación": "España", "ISO_Alpha3": "ESP", "Latitud": 41.3851, "Longitud": 2.1734, "Género": "Misterio", "Relación": "Nativo"},

    # --- NORTEAMÉRICA ---
    {"Título": "El gran Gatsby", "Autor": "F. Scott Fitzgerald", "País Autor": "Estados Unidos", "País Ambientación": "Estados Unidos", "ISO_Alpha3": "USA", "Latitud": 40.7128, "Longitud": -74.0060, "Género": "Drama", "Relación": "Nativo"},
    {"Título": "Matar a un ruiseñor", "Autor": "Harper Lee", "País Autor": "Estados Unidos", "País Ambientación": "Estados Unidos", "ISO_Alpha3": "USA", "Latitud": 31.4177, "Longitud": -87.4139, "Género": "Drama Social", "Relación": "Nativo"},
    {"Título": "El código Da Vinci", "Autor": "Dan Brown", "País Autor": "Estados Unidos", "País Ambientación": "Francia", "ISO_Alpha3": "FRA", "Latitud": 48.8566, "Longitud": 2.3522, "Género": "Thriller", "Relación": "Extranjero"},
    {"Título": "Memorias de una Geisha", "Autor": "Arthur Golden", "País Autor": "Estados Unidos", "País Ambientación": "Japón", "ISO_Alpha3": "JPN", "Latitud": 35.0116, "Longitud": 135.7681, "Género": "Ficción Histórica", "Relación": "Extranjero"},
    {"Título": "Moby Dick", "Autor": "Herman Melville", "País Autor": "Estados Unidos", "País Ambientación": "Océano Pacífico", "ISO_Alpha3": "USA", "Latitud": 0.0000, "Longitud": -140.0000, "Género": "Aventura", "Relación": "Nativo"},
    {"Título": "Las uvas de la ira", "Autor": "John Steinbeck", "País Autor": "Estados Unidos", "País Ambientación": "Estados Unidos", "ISO_Alpha3": "USA", "Latitud": 35.4676, "Longitud": -97.5164, "Género": "Realismo Social", "Relación": "Nativo"},
    {"Título": "Fahrenheit 451", "Autor": "Ray Bradbury", "País Autor": "Estados Unidos", "País Ambientación": "Estados Unidos", "ISO_Alpha3": "USA", "Latitud": 34.0522, "Longitud": -118.2437, "Género": "Distopía", "Relación": "Nativo"},
    {"Título": "En el camino", "Autor": "Jack Kerouac", "País Autor": "Estados Unidos", "País Ambientación": "Estados Unidos", "ISO_Alpha3": "USA", "Latitud": 39.7392, "Longitud": -104.9903, "Género": "Generación Beat", "Relación": "Nativo"},
    {"Título": "El resplandor", "Autor": "Stephen King", "País Autor": "Estados Unidos", "País Ambientación": "Estados Unidos", "ISO_Alpha3": "USA", "Latitud": 40.3673, "Longitud": -105.5217, "Género": "Terror", "Relación": "Nativo"},
    {"Título": "La letra escarlata", "Autor": "Nathaniel Hawthorne", "País Autor": "Estados Unidos", "País Ambientación": "Estados Unidos", "ISO_Alpha3": "USA", "Latitud": 42.5195, "Longitud": -70.8967, "Género": "Ficción Histórica", "Relación": "Nativo"},

    # --- ASIA, ÁFRICA Y OCEANÍA ---
    {"Título": "Kafka en la orilla", "Autor": "Haruki Murakami", "País Autor": "Japón", "País Ambientación": "Japón", "ISO_Alpha3": "JPN", "Latitud": 34.3427, "Longitud": 134.0466, "Género": "Realismo Mágico", "Relación": "Nativo"},
    {"Título": "Tokio Blues", "Autor": "Haruki Murakami", "País Autor": "Japón", "País Ambientación": "Japón", "ISO_Alpha3": "JPN", "Latitud": 35.6762, "Longitud": 139.6503, "Género": "Drama Romántico", "Relación": "Nativo"},
    {"Título": "Cometas en el cielo", "Autor": "Khaled Hosseini", "País Autor": "Afganistán", "País Ambientación": "Afganistán", "ISO_Alpha3": "AFG", "Latitud": 34.5553, "Longitud": 69.1779, "Género": "Drama", "Relación": "Nativo"},
    {"Título": "Hijos de la medianoche", "Autor": "Salman Rushdie", "País Autor": "India", "País Ambientación": "India", "ISO_Alpha3": "IND", "Latitud": 19.0760, "Longitud": 72.8777, "Género": "Realismo Mágico", "Relación": "Nativo"},
    {"Título": "Todo se desmorona", "Autor": "Chinua Achebe", "País Autor": "Nigeria", "País Ambientación": "Nigeria", "ISO_Alpha3": "NGA", "Latitud": 6.4541, "Longitud": 3.3813, "Género": "Ficción Histórica", "Relación": "Nativo"},
    {"Título": "Hijos de nuestro barrio", "Autor": "Naguib Mahfouz", "País Autor": "Egipto", "País Ambientación": "Egipto", "ISO_Alpha3": "EGY", "Latitud": 30.0444, "Longitud": 31.2357, "Género": "Drama Político", "Relación": "Nativo"},
    {"Título": "El dios de las pequeñas cosas", "Autor": "Arundhati Roy", "País Autor": "India", "País Ambientación": "India", "ISO_Alpha3": "IND", "Latitud": 9.5916, "Longitud": 76.5222, "Género": "Drama", "Relación": "Nativo"},
    {"Título": "La encuadernadora de libros prohibidos", "Autor": "Pip Williams", "País Autor": "Australia", "País Ambientación": "Reino Unido", "ISO_Alpha3": "GBR", "Latitud": 51.7520, "Longitud": -1.2577, "Género": "Histórica", "Relación": "Extranjero"},
    {"Título": "Desgracia", "Autor": "J.M. Coetzee", "País Autor": "Sudáfrica", "País Ambientación": "Sudáfrica", "ISO_Alpha3": "ZAF", "Latitud": -33.9249, "Longitud": 18.4241, "Género": "Drama Político", "Relación": "Nativo"},
    {"Título": "El sueño del pabellón rojo", "Autor": "Cao Xueqin", "País Autor": "China", "País Ambientación": "China", "ISO_Alpha3": "CHN", "Latitud": 39.9042, "Longitud": 116.4074, "Género": "Clásico", "Relación": "Nativo"}
]

# Crear el DataFrame de Pandas
df = pd.DataFrame(datos_novelas)

# Exportar a CSV listo para Flourish o Carto
nombre_archivo = "datasetNovelasPorPais.csv"
df.to_csv(nombre_archivo, index=False, encoding='utf-8-sig')

print(f"¡Dataset generado con éxito! Se han guardado {len(df)} registros en '{nombre_archivo}'.")