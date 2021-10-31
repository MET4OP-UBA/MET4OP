#%%
import numpy as np
import pandas as pd

resultCABA = pd.read_csv (                          # Resultados totales
    "datos_agrup.csv"
)


#%% [markdown]
### Funciones para armar Medias y Desvío Estandar de cada circuito por mesa, 
### y de cada comuna por circuito 

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
# Esperanza por mesa en cada circuito

def media_std_circuito(result_agrupacion):
    """
    Función que a partir de tablas con el caro en disputa y una agrupación en específico, 
    calcula el porcentaje por circuito electoral
    """

    # Primero calcula la media del circuito 
    result_agrupacion_acotado = result_agrupacion[["CODIGO_CIRCUITO", "CODIGO_MESA", "VOTOS_AGRUPACION", "NOMBRE_REGION", "NOMBRE_AGRUPACION"]]
    media_circuito = (result_agrupacion_acotado.groupby(["NOMBRE_REGION", "CODIGO_CIRCUITO"]).mean().round(2))
    media_circuito = media_circuito.rename(columns={"VOTOS_AGRUPACION": "MEDIA_MESAS"})

    # Luego calcula la std
    std_circuito = (result_agrupacion_acotado.groupby(["NOMBRE_REGION", "CODIGO_CIRCUITO"]).std().round(2))
    std_circuito = std_circuito.rename(columns={"VOTOS_AGRUPACION": "STD_MESAS"})
    
    # Luego Merge de ambas DF
    media_std_circuito = pd.merge(media_circuito, std_circuito, on=["NOMBRE_REGION", "CODIGO_CIRCUITO"])

    return media_std_circuito
#%%
def media_std_comuna(result_agrupacion):
    """
    Función que en base al porcentaje por circuito
    calcula el porcentaje por comuna
    """
    result_agrupacion_acotado = result_agrupacion[["CODIGO_CIRCUITO", "CODIGO_MESA", "VOTOS_AGRUPACION", "NOMBRE_REGION", "NOMBRE_AGRUPACION"]]
    
    # Primero calcula la media del circuito 
    media_comuna = (result_agrupacion_acotado.groupby(["NOMBRE_REGION"]).mean().round(2))
    media_comuna = media_comuna.rename(columns={"VOTOS_AGRUPACION": "MEDIA_CIRCUITOS"})
    media_comuna = media_comuna[["MEDIA_CIRCUITOS"]]

    # Luego calcula la std
    std_comuna = (result_agrupacion_acotado.groupby(["NOMBRE_REGION"]).std().round(2))
    std_comuna = std_comuna.rename(columns={"VOTOS_AGRUPACION": "STD_CIRCUITOS"})
    std_comuna = std_comuna[["STD_CIRCUITOS"]]
    
    # Luego Merge de ambas DF
    media_std_comuna = pd.merge(media_comuna, std_comuna, on=["NOMBRE_REGION"])

    return media_std_comuna


#%%
media_std_pres_fit_circuito = media_std_circuito(resultCABA_pres_fit)
media_std_pres_fit_circuito
# %%
media_std_pres_fit_comuna = media_std_comuna(resultCABA_pres_fit)
media_std_pres_fit_comuna
# %%
