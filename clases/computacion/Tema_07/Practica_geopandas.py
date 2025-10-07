#%%
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
pd.set_option('display.max_columns', None)

#%% Leo y reviso los datos electorales de las legislativas 2025
mesas = pd.read_csv('../../../dataset/elecciones_caba_2025/mesas25.csv')
#%%
print(mesas.head())
print(mesas.info())
print(mesas.describe())
print(mesas.columns)
#%% voy a eliminar intencionalmeente columnas que voy a recalcular
mesas = mesas.drop(columns=['comuna_x', 'comuna','cant_votantes','no_voto'])

#%% Vuelvo a crear las columnas que necesito
mesas['cant_votantes'] = mesas.iloc[:, 6:].sum(axis=1)
mesas['no_voto'] = mesas['electores_totales'] - mesas['cant_votantes']
print(mesas.info())
#%% Cargo el archivo.shp de los circuitos electorales
circuitos_gdf = gpd.read_file('../../../dataset/circuitos-electorales/circuitos-electorales.shp')
# %%
print(circuitos_gdf.head())
print(circuitos_gdf.info())
print(circuitos_gdf.describe())
print(circuitos_gdf.columns)
print(circuitos_gdf.plot())
#%% Ploteo los circuitos electorales
print(circuitos_gdf.plot())
# %% Arreglo nombres de columnas para hacer posible un match entre los datos
mesas['circuito'] = mesas['circuito'].astype(int)
mesas.rename(columns={'circuito': 'CIRCUITO_N'}, inplace=True)
mesas.rename(columns={'comuna_y': 'COMUNA'}, inplace=True)
#%% Agrupo los datos por circuito
circuitos = mesas.groupby('CIRCUITO_N').sum()
print(circuitos.head())
# Necesitamos resetear el indice par apoder operar con la columna de circuito
circuitos = circuitos.reset_index()
circuitos.drop(columns=['mesa','escuela','barrio','COMUNA'], inplace=True)
print(circuitos.columns)
#%% Unimos los datos electorales con los 
circuitos_merged = circuitos_gdf.merge(circuitos, on='CIRCUITO_N', how='left')
print(circuitos_merged.columns)
#%%
# Crear figura y ejes manualmente para tener más control
fig, ax = plt.subplots(figsize=(10, 10))

# Plot con mayoría de parámetros usados
circuitos_merged.plot(
    ax=ax,
    column='cant_votantes',  # columna para colorear
    cmap='YlOrRd',            # paleta de colores
    scheme='quantiles',       # método de clasificación (otros: 'equal_interval', 'natural_breaks', etc.)
    k=7,
    edgecolor='green',        # color de borde
    linewidth=1,              # grosor del borde
    alpha=1,                  # transparencia
    legend=True               # agregar leyenda
    # Otros posibles: legend_kwds={'label': 'Cantidad de votantes', 'shrink': 0.6}
)

# Título y etiquetas
ax.set_title('Cantidad de Votantes por Circuito', fontsize=14)
ax.set_xlabel('Longitud')
ax.set_ylabel('Latitud')

# Nota al pie
plt.figtext(0.5, 0.01, 'Fuente: Scraping propio - Año 2025', ha='center', fontsize=9)

# Variante: ocultar los ejes (ideal para mapas más limpios o visualizaciones puras)
# ax.set_axis_off()

plt.tight_layout()
plt.show()
# %%
circuitos_merged.columns
# %% Si observamos bien, solo estamos ploteando valores absolutos
# y seria mas util tener una medida de la relacíon entre votantes totales y votantes habilitados
# Es decir, la participacíon electoral
circuitos_merged['participacion'] = circuitos_merged['cant_votantes'] / circuitos_merged['electores_totales']
# %%
fig, ax = plt.subplots(figsize=(10, 10))
circuitos_merged.plot(
    column='participacion',
    cmap='YlOrRd',
    scheme='quantiles',
    k=7,
    legend=True,
    ax=ax,
)
ax.set_axis_off()
ax.set_title('Participacíon por Circuito', fontsize=14)
plt.tight_layout()
plt.show()
# %% Voy a añadir etiquetas a los circuitos
fig, ax = plt.subplots(figsize=(10, 10))

# Plot del mapa
circuitos_merged.plot(
    column='participacion',
    cmap='YlOrRd',
    scheme='quantiles',
    k=7,
    legend=True,
    ax=ax,
)

# Añadir etiquetas con valores de participación (centrados en los polígonos)
for idx, row in circuitos_merged.iterrows():
    centroid = row.geometry.centroid
    ax.text(
        centroid.x, centroid.y,
        f"{row['participacion']:.2f}",  # Redondear a 2 decimales
        fontsize=10,
        ha='center',
        va='center',
        color='black'
    )

ax.set_axis_off()
ax.set_title('Participación por Circuito', fontsize=14)
plt.tight_layout()
plt.show()

# %% Crear versión porcentual del DataFrame
# Identificamos las columnas de partidos políticos (desde 'buenos_aires_primero' en adelante)
partidos = circuitos_merged.columns[11:32]  # Desde 'buenos_aires_primero' hasta 'votos_recurridos'

# Creamos un DataFrame para los porcentajes
df_porcentual = circuitos_merged.copy()

# Calculamos el porcentaje de votos para cada partido
for partido in partidos:
    df_porcentual[f'{partido}_pct'] = (df_porcentual[partido] / df_porcentual['cant_votantes']) * 100

print("Columnas de porcentajes creadas:")
print([col for col in df_porcentual.columns if '_pct' in col])

# %% Mapa 1: 'es_ahora_buenos_aires' en escala de azules
fig, ax = plt.subplots(figsize=(12, 10))

df_porcentual.plot(
    column='es_ahora_buenos_aires_pct',
    cmap='Blues',
    scheme='quantiles',
    k=7,
    legend=True,
    ax=ax,
    edgecolor='black',
    linewidth=0.5
)

ax.set_axis_off()
ax.set_title('Porcentaje de Votos - Es Ahora Buenos Aires', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.show()

# %% Mapa 2: 'la_libertad_avanza' en escala de violetas
fig, ax = plt.subplots(figsize=(12, 10))

df_porcentual.plot(
    column='la_libertad_avanza_pct',
    cmap='Purples',
    scheme='natural_breaks',
    k=7,
    legend=True,
    ax=ax,
    edgecolor='black',
    linewidth=0.5
)

ax.set_axis_off()
ax.set_title('Porcentaje de Votos - La Libertad Avanza', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.show()

# %% Mapa 3: Partido con porcentaje máximo en cada circuito
# Encontramos el partido con mayor porcentaje en cada circuito
partidos_pct = [col for col in df_porcentual.columns if '_pct' in col]

# Creamos columnas para el partido ganador y su porcentaje
df_porcentual['partido_ganador'] = df_porcentual[partidos_pct].idxmax(axis=1)
df_porcentual['porcentaje_max'] = df_porcentual[partidos_pct].max(axis=1)

# Limpiamos el nombre del partido (quitamos '_pct')
df_porcentual['partido_ganador'] = df_porcentual['partido_ganador'].str.replace('_pct', '')

# Creamos un diccionario de colores para cada partido
colores_partidos = {
    'buenos_aires_primero': '#F1C40F',
    'coalición_cívica_-_afirmación_para_una_república_igualitaria': '#AAB7B8',
    'confluencia_-_por_la_igualdad_y_la_soberanía': '#AAB7B8',
    'el_movimiento': '#AAB7B8',
    'es_ahora_buenos_aires': '#3498DB',
    'evolución': '#F1948A',
    'frente_patriota_federal': '#AAB7B8',
    'frente_de_izquierda_y_de_trabajadores_-_unidad': '#C0392B',
    'la_izquierda_en_la_ciudad': '#AAB7B8',
    'la_libertad_avanza': '#8E44AD',
    'movimiento_plural': '#AAB7B8',
    'movimiento_de_integración_y_desarrollo': '#AAB7B8',
    'principios_y_valores': '#AAB7B8',
    'seamos_libres': '#AAB7B8',
    'unión_porteña_libertaria': '#AAB7B8',
    'unión_del_centro_democrático': '#AAB7B8',
    'volvamos_buenos_aires': '#AAB7B8',
    'voto_en_blanco': '#D5DBDB',
    'votos_de_identidad_impugnada': '#E8DAEF'
}


# Asignamos colores a cada circuito
df_porcentual['color'] = df_porcentual['partido_ganador'].map(colores_partidos)

# Creamos el mapa
fig, ax = plt.subplots(figsize=(15, 12))

# Plot del mapa con colores por partido ganador
df_porcentual.plot(
    color=df_porcentual['color'],
    ax=ax,
    edgecolor='white',
    linewidth=0.5
)

# Crear leyenda personalizada
legend_elements = [Patch(facecolor=color, label=partido.replace('_', ' ').title()) 
                  for partido, color in colores_partidos.items() 
                  if partido in df_porcentual['partido_ganador'].values]

ax.legend(handles=legend_elements, bbox_to_anchor=(1.05, 1), loc='upper left')

ax.set_axis_off()
ax.set_title('Partido con Mayor Porcentaje de Votos por Circuito', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.show()

# %% Dissolve por comuna desde circuitos_merged (datos absolutos)
# Hacemos dissolve por comuna sumando los votos absolutos de cada partido
df_por_comuna = circuitos_merged.dissolve(by='COMUNA', aggfunc='sum')

# Recalculamos los porcentajes después del dissolve
for partido in partidos:
    df_por_comuna[f'{partido}_pct'] = (df_por_comuna[partido] / df_por_comuna['cant_votantes']) * 100

print("Comunas disponibles:", df_por_comuna.index.tolist())
print("Columnas de porcentajes por comuna creadas")


# %% Mapa facetado 2x2 con los 4 partidos principales
fig, axes = plt.subplots(2, 2, figsize=(20, 16))
axes = axes.flatten()

# Configuración de cada partido
partidos_config = [
    {
        'columna': 'evolución_pct',
        'titulo': 'Evolución',
        'cmap': 'Reds',
        'posicion': 0
    },
    {
        'columna': 'es_ahora_buenos_aires_pct',
        'titulo': 'Es Ahora Buenos Aires',
        'cmap': 'Blues',
        'posicion': 1
    },
    {
        'columna': 'buenos_aires_primero_pct',
        'titulo': 'Buenos Aires Primero',
        'cmap': 'YlOrBr',
        'posicion': 2
    },
    {
        'columna': 'la_libertad_avanza_pct',
        'titulo': 'La Libertad Avanza',
        'cmap': 'Purples',
        'posicion': 3
    }
]

# Crear cada subplot
for config in partidos_config:
    ax = axes[config['posicion']]
    
    df_por_comuna.plot(
        column=config['columna'],
        cmap=config['cmap'],
        scheme='quantiles',
        k=7,
        legend=True,
        ax=ax,
        edgecolor='white',
        linewidth=0.5
    )
    
    for idx, row in df_por_comuna.iterrows():
        centroid = row.geometry.centroid
        ax.text(
            centroid.x, centroid.y,
            f"C{idx}",
            fontsize=10,
            ha='center',
            va='center',
            color='white',
            fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.2", facecolor='black', alpha=0.7)
        )
    
    ax.set_axis_off()
    ax.set_title(config['titulo'], fontsize=14, fontweight='bold')

plt.suptitle('Porcentaje de Votos por Comuna - Partidos Principales', fontsize=18, fontweight='bold')
plt.tight_layout()
plt.show()

# %% Mapa 1: Evolución
fig, ax = plt.subplots(figsize=(15, 12))

df_por_comuna.plot(
    column='evolución_pct',
    cmap='Reds',
    scheme='quantiles',
    k=7,
    legend=True,
    ax=ax,
    edgecolor='white',
    linewidth=0.5
)

for idx, row in df_por_comuna.iterrows():
    centroid = row.geometry.centroid
    ax.text(
        centroid.x, centroid.y,
        f"{row['evolución_pct']:.1f}%",
        fontsize=10,
        ha='center',
        va='center',
        color='white',
        fontweight='bold',
        bbox=dict(boxstyle="round,pad=0.3", facecolor='black', alpha=0.8)
    )

ax.set_axis_off()
ax.set_title('Porcentaje de Votos por Comuna - Evolución', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.show()

# %% Mapa 2: Es Ahora Buenos Aires
fig, ax = plt.subplots(figsize=(15, 12))

df_por_comuna.plot(
    column='es_ahora_buenos_aires_pct',
    cmap='Blues',
    scheme='quantiles',
    k=7,
    legend=True,
    ax=ax,
    edgecolor='white',
    linewidth=0.5
)

for idx, row in df_por_comuna.iterrows():
    centroid = row.geometry.centroid
    ax.text(
        centroid.x, centroid.y,
        f"{row['es_ahora_buenos_aires_pct']:.1f}%",
        fontsize=10,
        ha='center',
        va='center',
        color='white',
        fontweight='bold',
        bbox=dict(boxstyle="round,pad=0.3", facecolor='black', alpha=0.8)
    )

ax.set_axis_off()
ax.set_title('Porcentaje de Votos por Comuna - Es Ahora Buenos Aires', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.show()

# %% Mapa 3: Buenos Aires Primero
fig, ax = plt.subplots(figsize=(15, 12))

df_por_comuna.plot(
    column='buenos_aires_primero_pct',
    cmap='YlOrBr',
    scheme='quantiles',
    k=7,
    legend=True,
    ax=ax,
    edgecolor='white',
    linewidth=0.5
)

for idx, row in df_por_comuna.iterrows():
    centroid = row.geometry.centroid
    ax.text(
        centroid.x, centroid.y,
        f"{row['buenos_aires_primero_pct']:.1f}%",
        fontsize=10,
        ha='center',
        va='center',
        color='white',
        fontweight='bold',
        bbox=dict(boxstyle="round,pad=0.3", facecolor='black', alpha=0.8)
    )

ax.set_axis_off()
ax.set_title('Porcentaje de Votos por Comuna - Buenos Aires Primero', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.show()

# %% Mapa 4: La Libertad Avanza
fig, ax = plt.subplots(figsize=(15, 12))

df_por_comuna.plot(
    column='la_libertad_avanza_pct',
    cmap='Purples',
    scheme='quantiles',
    k=7,
    legend=True,
    ax=ax,
    edgecolor='white',
    linewidth=0.5
)

for idx, row in df_por_comuna.iterrows():
    centroid = row.geometry.centroid
    ax.text(
        centroid.x, centroid.y,
        f"{row['la_libertad_avanza_pct']:.1f}%",
        fontsize=10,
        ha='center',
        va='center',
        color='white',
        fontweight='bold',
        bbox=dict(boxstyle="round,pad=0.3", facecolor='black', alpha=0.8)
    )

ax.set_axis_off()
ax.set_title('Porcentaje de Votos por Comuna - La Libertad Avanza', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.show()
#%%Cargo un shape de barrios
barrios_gdf = gpd.read_file('../../../dataset/barrios_caba/caba_barrios.geojson')
#%% Cargo datos reales de precio dle metro cuadrado en dolares al 2ndo trim 2025
precios_m2 = {
    'Agronomía': None,
    'Almagro': 2.399,
    'Balvanera': 2.070,
    'Barracas': 2.060,
    'Belgrano': 3.154,
    'Boca': 1.555,
    'Boedo': 2.092,
    'Caballito': 2.490,
    'Chacarita': 2.740,
    'Coghlan': 2.666,
    'Colegiales': 3.005,
    'Constitución': 2.000,
    'Flores': 2.171,
    'Floresta': 2.069,
    'La Paternal': None,
    'Liniers': 2.024,
    'Mataderos': 2.038,
    'Monte Castro': 2.180,
    'Montserrat': 2.245,
    'Nueva Pompeya': None,
    'Núñez': 3.197,
    'Palermo': 3.155,
    'Parque Avellaneda': None,
    'Parque Chacabuco': 2.365,
    'Parque Chas': 2.527,
    'Parque Patricios': 1.796,
    'Puerto Madero': 5.865,
    'Recoleta': 2.811,
    'Retiro': 2.425,
    'Saavedra': 2.726,
    'San Cristóbal': 2.008,
    'San Nicolás': 2.043,
    'San Telmo': 2.336,
    'Vélez Sarsfield': 1.851,
    'Versalles': None,
    'Villa Crespo': 2.573,
    'Villa del Parque': 2.399,
    'Villa Devoto': 2.501,
    'Villa Gral. Mitre': 2.245,
    'Villa Lugano': None,
    'Villa Luro': 2.149,
    'Villa Ortúzar': 2.570,
    'Villa Pueyrredón': 2.389,
    'Villa Real': None,
    'Villa Riachuelo': None,
    'Villa Santa Rita': 2.162,
    'Villa Soldati': None,
    'Villa Urquiza': 2.728
}
# %%
precios_m2_df = pd.DataFrame(precios_m2.items(), columns=['BARRIO', 'PRECIO_M2'])
#%%
import unicodedata

precios_m2_df['BARRIO'] = precios_m2_df['BARRIO'].str.upper()
precios_m2_df['BARRIO'] = precios_m2_df['BARRIO'].apply(
    lambda x: ''.join(
        c for c in unicodedata.normalize('NFD', x)
        if unicodedata.category(c) != 'Mn'
    )
)
# %%
barrios_merged = barrios_gdf.merge(precios_m2_df, on='BARRIO', how='left')

barrios_merged.plot(column='PRECIO_M2', cmap='viridis', scheme='fisher_jenks', k=5, legend=True,
    edgecolor='black',
    linewidth=0.5,
    missing_kwds={
        'color': 'none',         # sin color de relleno
        'edgecolor': 'black',    # con borde negro
        'hatch': '///',          # opcional: rayado para marcar NA
        'label': 'Sin dato'      # aparece en la leyenda si hay legend=True
    }
)

# %% Spatial Join entre circuitos y barrios
# OPERACIÓN ESPACIAL: Spatial Join
# Un spatial join combina dos GeoDataFrames basándose en su relación espacial.
# En este caso, vamos a usar el centroide de cada circuito para determinar en qué barrio se encuentra.
# Asegurar que ambos GeoDataFrames estén en el mismo CRS
print("CRS antes de la conversión:")
print("Circuitos:", circuitos_merged.crs)
print("Barrios:", barrios_merged.crs)
print('--------------------------------')

# Asegurarse de que ambos estén en el mismo sistema de coordenadas
barrios_merged = barrios_merged.to_crs(circuitos_merged.crs)

# Crear centroides de los circuitos
circuitos_centroides = circuitos_merged.copy()
circuitos_centroides['geometry'] = circuitos_centroides.geometry.centroid

# Realizar spatial join: barrios que contienen cada centroide de circuito
barrios_con_circuitos = gpd.sjoin(
    barrios_merged[['BARRIO', 'PRECIO_M2', 'geometry']],
    circuitos_centroides,
    how='left',
    predicate='contains'
)

# %% Recalcular porcentajes con los datos actualizados
# Identificamos las columnas de partidos políticos
partidos = barrios_con_circuitos.columns[11:32]  # Desde 'buenos_aires_primero' hasta 'votos_recurridos'

# Calculamos el porcentaje de votos para cada partido
for partido in partidos:
    barrios_con_circuitos[f'{partido}_pct'] = (barrios_con_circuitos[partido] / barrios_con_circuitos['cant_votantes']) * 100

# Calculamos el porcentaje de no voto
barrios_con_circuitos['no_voto_pct'] = (barrios_con_circuitos['no_voto'] / barrios_con_circuitos['electores_totales']) * 100

print("Porcentajes recalculados para circuitos con datos de barrios")
print(f"Columnas de porcentajes: {[col for col in barrios_con_circuitos.columns if '_pct' in col]}")

# %% Visualizaciones cruzadas: Buenos Aires Primero vs Precio m2
# Mapa 1: Buenos Aires Primero por circuito con etiquetas de porcentaje
fig, ax = plt.subplots(figsize=(15, 12))

barrios_con_circuitos.plot(
    column='buenos_aires_primero_pct',
    cmap='YlOrBr',
    scheme='quantiles',
    k=7,
    legend=True,
    ax=ax,
    edgecolor='white',
    linewidth=0.5
)

# Agregamos etiquetas con el porcentaje de Buenos Aires Primero
for idx, row in barrios_con_circuitos.iterrows():
    centroid = row.geometry.centroid
    ax.text(
        centroid.x, centroid.y,
        f"{row['buenos_aires_primero_pct']:.2f}%",
        fontsize=8,
        ha='center',
        va='center',
        color='white',
        fontweight='bold',
        bbox=dict(boxstyle="round,pad=0.2", facecolor='black', alpha=0.7)
    )

ax.set_axis_off()
ax.set_title('Porcentaje de Votos - Buenos Aires Primero por Circuito', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.show()

# %% Mapa 2: Precio m2 por barrio (incluyendo geometrías sin datos)
fig, ax = plt.subplots(figsize=(15, 12))

# Plot de todos los barrios, incluyendo los sin datos
barrios_con_circuitos.plot(
    column='PRECIO_M2',
    cmap='RdBu_r',
    scheme='quantiles',
    k=7,
    legend=True,
    ax=ax,
    edgecolor='white',
    linewidth=0.5,
    missing_kwds={
        'color': 'lightgray',    # color gris para valores faltantes
        'edgecolor': 'black',    # borde negro
        'hatch': '///',          # rayado para marcar NA
        'label': 'Sin dato'      # aparece en la leyenda
    }
)

ax.set_axis_off()
ax.set_title('Precio m2 (USD) por Circuito - Basado en Barrio', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.show()

# %% Análisis cruzado: Scatter plot Buenos Aires Primero vs Precio m2
fig, ax = plt.subplots(figsize=(12, 8))

# Datos para el scatter plot
datos_scatter = barrios_con_circuitos[barrios_con_circuitos['PRECIO_M2'].notna()]

ax.scatter(datos_scatter['PRECIO_M2'], datos_scatter['buenos_aires_primero_pct'], 
          alpha=0.6, s=50, c='orange', edgecolors='black', linewidth=0.5)

ax.set_xlabel('Precio m2 (USD)', fontsize=12)
ax.set_ylabel('Porcentaje de Votos - Buenos Aires Primero', fontsize=12)
ax.set_title('Relación entre Precio m2 y Buenos Aires Primero por Circuito', fontsize=14, fontweight='bold')

# Agregamos línea de tendencia
import numpy as np
z = np.polyfit(datos_scatter['PRECIO_M2'], datos_scatter['buenos_aires_primero_pct'], 1)
p = np.poly1d(z)
ax.plot(datos_scatter['PRECIO_M2'], p(datos_scatter['PRECIO_M2']), "r--", alpha=0.8)

# Agregamos coeficiente de correlación
correlacion = datos_scatter['PRECIO_M2'].corr(datos_scatter['buenos_aires_primero_pct'])
ax.text(0.05, 0.95, f'Correlación: {correlacion:.3f}', 
        transform=ax.transAxes, fontsize=12, 
        bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))

plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# %%
