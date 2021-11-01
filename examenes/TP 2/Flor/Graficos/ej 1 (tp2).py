#%%
import numpy as np
import pandas as pd

resultCABA = pd.read_csv (                          # Resultados totales
    "datos_agrup.csv"
)
resultCABA.head()

#%% [markdown]
### Funciones para armar tablas de porcentaje por circuito y por comuna
# La idea es que se puedan aplicar a distintas categorías y agrupaciones

#%%
def porcentaje_circuito(result_total, result_agrupacion):
    """
    Función que a partir de tablas con el caro en disputa y una agrupación en específico, 
    calcula el porcentaje por circuito electoral
    """

    # Primero suma la cantidad de votos totales por circuito
    result_total_acotado = result_total[["CODIGO_CIRCUITO", "CODIGO_MESA", "VOTOS_AGRUPACION", "NOMBRE_REGION", "NOMBRE_AGRUPACION"]]

    result_total_circuito = (result_total_acotado.groupby(["NOMBRE_REGION", "CODIGO_CIRCUITO"]).sum())

    result_total_circuito = result_total_circuito.rename(columns={"VOTOS_AGRUPACION": "VOTOS_TOTALES"})


    # Luego suma la cantidad de votos de determinada agrupacion por circuito
    result_agrupacion_acotado = result_agrupacion[["CODIGO_CIRCUITO", "CODIGO_MESA", "VOTOS_AGRUPACION", "NOMBRE_REGION", "NOMBRE_AGRUPACION"]]

    result_agrupacion_circuito = (result_agrupacion_acotado.groupby(["NOMBRE_REGION", "CODIGO_CIRCUITO"]).sum())

    # Luego hace un merge, y calcula el porcentaje diviendo votos de la agrupacion por totales
    porcentaje_circuito = pd.merge(result_total_circuito, result_agrupacion_circuito, on=["NOMBRE_REGION","CODIGO_CIRCUITO"])

    porcentaje_circuito["PORCENTAJE_AGRUPACION"] = ((porcentaje_circuito["VOTOS_AGRUPACION"] / porcentaje_circuito["VOTOS_TOTALES"]) * 100).round(2)


    return porcentaje_circuito
#%%
def porcentaje_comuna(porcentaje_circuito):
    """
    Función que en base al porcentaje por circuito
    calcula el porcentaje por comuna
    """
    porcentaje_comuna = (porcentaje_circuito.groupby("NOMBRE_REGION")["VOTOS_TOTALES", "VOTOS_AGRUPACION"].sum())
    porcentaje_comuna["PORCENTAJE_AGRUPACION"] = ((porcentaje_comuna["VOTOS_AGRUPACION"] / porcentaje_comuna["VOTOS_TOTALES"] * 100).round(2))

    return porcentaje_comuna

#%% [markdown]
### Porcentajes del FIT para categorías Presidente y Vicepresidente
#%%
# Resultados del FIT en cada mesa solo para Presidente
resultCABA_pres_fit = resultCABA[(resultCABA["NOMBRE_CATEGORIA"] == "Presidente y Vicepresidente de la República") & (resultCABA["NOMBRE_AGRUPACION"] == "FRENTE DE IZQUIERDA Y DE TRABAJADORES - UNIDAD")]
resultCABA_pres_fit.reset_index(inplace=True)

#%%
# Resultados totales en cada mesa solo para Presidente
resultCABA_pres_total = resultCABA[resultCABA["NOMBRE_CATEGORIA"] == "Presidente y Vicepresidente de la República"]
resultCABA_pres_total.reset_index(inplace=True)

#%%
# Porcentaje del FIT por circuito
porc_pres_circuito_fit = porcentaje_circuito(resultCABA_pres_total, resultCABA_pres_fit)
porc_pres_circuito_fit

#%%
# Porcentaje del FIT por comuna
porc_pres_comuna_fit = porcentaje_comuna(porc_pres_circuito_fit)
porc_pres_comuna_fit

#%%
# Resultados totales en cada mesa solo para Diputado Nacional
resultCABA_dip_total = resultCABA[resultCABA["NOMBRE_CATEGORIA"] == "Diputados Nacionales Ciudad Autónoma de Buenos Aires"]
resultCABA_dip_total.reset_index(inplace=True)


#%% [markdown]
### Comparación de los resultados del FIT para categorías Diputados Nacionales y Presidente.
#### La idea es que la diferencia entre ambos porcentajes va a dar una idea del corte de boleta

#%%
# Resultados del FIT en cada mesa solo para Presidente
resultCABA_dip_fit = resultCABA[(resultCABA["NOMBRE_CATEGORIA"] == "Diputados Nacionales Ciudad Autónoma de Buenos Aires") & (resultCABA["NOMBRE_AGRUPACION"] == "FRENTE DE IZQUIERDA Y DE TRABAJADORES - UNIDAD")]
resultCABA_dip_fit.reset_index(inplace=True)

#%%
# Porcentaje de Diputados Nacionales del FIT por circuito
porc_dip_circ_fit = porcentaje_circuito(resultCABA_dip_total, resultCABA_dip_fit)
porc_dip_circ_fit

#%%
# Porcentaje de Diputados Nacionales del FIT por comuna
porc_dip_comuna_fit = porcentaje_comuna(porc_dip_circ_fit)
porc_dip_comuna_fit

#%%
# Renombro columnas para que sea más legible la tabla que compara resultados legislativos con presidenciales
porc_pres_comuna_fit = porc_pres_comuna_fit.rename(columns={"VOTOS_TOTALES": "VOTOS_TOTALES_PRES", "VOTOS_AGRUPACION": "VOTOS_FIT_PRES", "PORCENTAJE_AGRUPACION": "PORCENTAJE_FIT_PRES"})
porc_dip_comuna_fit = porc_dip_comuna_fit.rename(columns={"VOTOS_TOTALES": "VOTOS_TOTALES_DIP", "VOTOS_AGRUPACION": "VOTOS_FIT_DIP", "PORCENTAJE_AGRUPACION": "PORCENTAJE_FIT_DIP"})

#%%
# Merge de ambas tablas
comparacion_fit_pres_dip = pd.merge(porc_pres_comuna_fit, porc_dip_comuna_fit, left_index=True, right_index=True)
comparacion_fit_pres_dip

#%%
# Porcentaje de Corte de Boleta entre Diputados Nacionales y Presidente
comparacion_fit_pres_dip["DIFERENCIA_DIP_PRES"] = (comparacion_fit_pres_dip["PORCENTAJE_FIT_DIP"] - comparacion_fit_pres_dip["PORCENTAJE_FIT_PRES"])
comparacion_fit_pres_dip.sort_values(by=["DIFERENCIA_DIP_PRES"], ascending=False) 

#%% [markdown]
### Comparación con el voto en blanco en la categorías presidente

#%%
# Armo el DF con votos en blanco para presidente
resultCABA_pres_blanco = resultCABA[(resultCABA["NOMBRE_CATEGORIA"] == "Presidente y Vicepresidente de la República") & (resultCABA["NOMBRE_AGRUPACION"] == "BLANCO")]
resultCABA_pres_blanco.reset_index(inplace=True)

#%%
# FUnción para obtener el porcentaje por circuito
porc_pres_circuito_blanco = porcentaje_circuito(resultCABA_pres_total, resultCABA_pres_blanco)
porc_pres_circuito_blanco
#%%
# Función para obtener porcentaje por Comuna
porc_pres_comuna_blanco = porcentaje_comuna(porc_pres_circuito_blanco)
porc_pres_comuna_blanco

#%%
# Cambo los nombres para hacer más legible
porc_pres_comuna_blanco = porc_pres_comuna_blanco.rename(columns={"VOTOS_TOTALES": "VOTOS_TOTALES_PRES", "VOTOS_AGRUPACION": "VOTOS_BLANCO_PRES", "PORCENTAJE_AGRUPACION": "PORCENTAJE_BLANCO_PRES"})
porc_pres_comuna_blanco

#%%
# Esta es la comparación entre voto en blanco para presidente y voto para el FIT en diputados. 
# Como comparación es menos útil que la anterior, no tengo como saber qué porcentaje del voto en blanco fue al FIT en diputados
# Por lo que no sé cuanto valdría la pena ir a buscar al voto
# Pero teniendo en cuenta la postura del FIT de en ballotage llamar al voto en blanco, puede llegar a ser un número interesante de votos para buscar
comparacion_blanco_pres_fit_dip = pd.merge(porc_pres_comuna_blanco, porc_dip_comuna_fit, left_index=True, right_index=True)
comparacion_blanco_pres_fit_dip
#%%
# Pendiente: 
# - Ver como georeferenciar las tablas (quiza hacer un mapa)
# - Hacer algunos graficos copados
# - Comparar el voto legislativo con el voto en blanco en presidente
