# %%
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns

#Grafico votos diputados nacionales por comuna partido FIT
votos_dipnac_grafico_1 = pd.read_csv("DipNac_FIT_comuna.csv")
sns.set(style = 'darkgrid')
sns.relplot(x = 'VOTOS_FIT_DIPNAC', y = 'NOMBRE_REGION', data= votos_dipnac_grafico_1)

#Grafico votos presidenciales por comuna partido FIT
votos_pres_grafico_1 = pd.read_csv("pres_FIT_comuna.csv")
sns.set(style = 'darkgrid')
sns.relplot(x = 'VOTOS_AGRUPACION', y = 'NOMBRE_REGION', data= votos_pres_grafico_1)



# %%
#Grafico Pie Chart. Porcentajes de votos presidenciales por comunas de partido FIT
df =  pd.read_csv('pres_FIT_comuna.csv')
nombre_region = df["NOMBRE_REGION"]
porcentaje_agrupacion = df["PORCENTAJE_AGRUPACION"]
colors = ["#C0C0C0", "#000000", "#FF0000", "#800000", "#FFFF00", "#808000", "#00FF00", "#008000", "#00FFFF", "#008080","#0000FF", "#000080", "#FF00FF", "#800080", "#FFFFFF"]
explode = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)  
plt.pie(porcentaje_agrupacion, labels=nombre_region, explode=explode, colors=colors,
autopct='%1.1f%%', shadow=True, startangle=140)
plt.title("Porcentajes de voto presidenciales por comunas de partido FIT")
plt.show()
# %%
#Grafico pie chart. Porcentajes de voto diputados nacionales por comunas de partido FIT
df =  pd.read_csv("DipNac_FIT_comuna.csv")
nombre_region = df["NOMBRE_REGION"]
porcentaje_agrupacion = df["PORCENTAJE_FIT_DIPNAC"]
colors = ["#C0C0C0", "#000000", "#FF0000", "#800000", "#FFFF00", "#808000", "#00FF00", "#008000", "#00FFFF", "#008080","#0000FF", "#000080", "#FF00FF", "#800080", "#FFFFFF"]
explode = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)  
plt.pie(porcentaje_agrupacion, labels=nombre_region, explode=explode, colors=colors,
autopct='%1.1f%%', shadow=True, startangle=140)
plt.title("Porcentajes de voto a diputados por comunas de partido FIT")
plt.show()
# %%
#Gráfico de barras. Porcentaje de votos al FIT en cada comuna.
colors = ["#C0C0C0", "#000000", "#FF0000", "#800000", "#FFFF00", "#808000", "#00FF00", "#008000", "#00FFFF", "#008080","#0000FF", "#000080", "#FF00FF", "#800080", "#FFFFFF"]
df =  pd.read_csv('pres_FIT_comuna.csv')
eje_x = df["NOMBRE_REGION"]
eje_y = df["PORCENTAJE_AGRUPACION"]
plt.bar(eje_x, eje_y, color=colors)
plt.xticks(rotation=90)
plt.ylabel('Porcentajes a voto presidencial')
plt.xlabel('Comunas')
plt.title('Porcentaje de votos al FIT por comuna')

plt.show()


# %%
