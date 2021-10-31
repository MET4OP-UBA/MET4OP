#%%
import numpy as np
import pandas as pd

resultCABA = pd.read_csv (                          # Resultados totales
    "datos_agrup.csv"
)


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
### Corte de boleta.
#### Restar el voto en cada partido para de categoría Diputado con el Presidencial para cualcular corte de boleta

#%%
def corte_boleta(porc_pres, porc_dip):
    """
    Resta el voto en categoría Diputado con el Presidencial 
    para cualcular corte de boleta
    """
    porc_pres = porc_pres.rename(columns={"VOTOS_TOTALES": "VOTOS_TOTALES_PRES", "VOTOS_AGRUPACION": "VOTOS_AGRUPACION_PRES", "PORCENTAJE_AGRUPACION": "PORCENTAJE_AGRUPACION_PRES"})
    porc_dip = porc_dip.rename(columns={"VOTOS_TOTALES": "VOTOS_TOTALES_DIP", "VOTOS_AGRUPACION": "VOTOS_AGRUPACION_DIP", "PORCENTAJE_AGRUPACION": "PORCENTAJE_AGRUPACION_DIP"})

    comparacion_pres_dip = pd.merge(porc_pres, porc_dip, left_index=True, right_index=True)

    comparacion_pres_dip["DIFERENCIA_DIP_PRES"] = (comparacion_pres_dip["PORCENTAJE_AGRUPACION_DIP"] - comparacion_pres_dip["PORCENTAJE_AGRUPACION_PRES"])

    return comparacion_pres_dip

#%% [markdown]
#### FIT
#%%
# Resultados del FIT en cada mesa solo para Diputado
resultCABA_dip_fit = resultCABA[(resultCABA["NOMBRE_CATEGORIA"] == "Diputados Nacionales Ciudad Autónoma de Buenos Aires") & (resultCABA["NOMBRE_AGRUPACION"] == "FRENTE DE IZQUIERDA Y DE TRABAJADORES - UNIDAD")]

#%%
# Porcentaje de Diputados Nacionales del FIT por circuito
porc_dip_circ_fit = porcentaje_circuito(resultCABA_dip_total, resultCABA_dip_fit)
porc_dip_circ_fit

#%%
# Porcentaje de Diputados Nacionales del FIT por comuna
porc_dip_comuna_fit = porcentaje_comuna(porc_dip_circ_fit)
porc_dip_comuna_fit

# %%
# Diferencia entre el voto Presidente y Diputado en FIT por COMUNA
diferencia_fit_comuna = corte_boleta(porc_pres_comuna_fit, porc_dip_comuna_fit)
diferencia_fit_comuna[["PORCENTAJE_AGRUPACION_PRES","PORCENTAJE_AGRUPACION_DIP", "DIFERENCIA_DIP_PRES"]]
# %%
# Diferencia entre el voto Presidente y Diputado en FIT por CIRCUITO
diferencia_fit_circ = corte_boleta(porc_pres_circuito_fit, porc_dip_circ_fit)
diferencia_fit_circ
#%% [markdown]
#### FdT
#%%
# Resultados del FdT en cada mesa solo para Presidente
resultCABA_pres_fdt = resultCABA[(resultCABA["NOMBRE_CATEGORIA"] == "Presidente y Vicepresidente de la República") & (resultCABA["NOMBRE_AGRUPACION"] == "FRENTE DE TODOS")]

#%%
# Porcentaje de Diputados Nacionales del FdT por circuito
porc_pres_circ_fdt = porcentaje_circuito(resultCABA_pres_total, resultCABA_pres_fdt)
porc_pres_circ_fdt

#%%
# Porcentaje de Diputados Nacionales del FdT por comuna
porc_pres_comuna_fdt = porcentaje_comuna(porc_pres_circ_fdt)
porc_pres_comuna_fdt

#%%
# Resultados del FdT en cada mesa solo para Presidente
resultCABA_dip_fdt = resultCABA[(resultCABA["NOMBRE_CATEGORIA"] == "Diputados Nacionales Ciudad Autónoma de Buenos Aires") & (resultCABA["NOMBRE_AGRUPACION"] == "FRENTE DE TODOS")]

#%%
# Porcentaje de Diputados Nacionales del FdT por circuito
porc_dip_circ_fdt = porcentaje_circuito(resultCABA_dip_total, resultCABA_dip_fdt)

#%%
# Porcentaje de Diputados Nacionales del FdT por comuna
porc_dip_comuna_fdt = porcentaje_comuna(porc_dip_circ_fdt)
# %%
# Diferencia entre el voto Presidente y Diputado en FdT por COMUNA
diferencia_fdt_comuna = corte_boleta(porc_pres_comuna_fdt, porc_dip_comuna_fdt)
diferencia_fdt_comuna[["PORCENTAJE_AGRUPACION_PRES","PORCENTAJE_AGRUPACION_DIP", "DIFERENCIA_DIP_PRES"]]
# %%
# Diferencia entre el voto Presidente y Diputado en FdT por CIRCUITO
diferencia_fdt_circ = corte_boleta(porc_pres_circ_fdt, porc_dip_circ_fdt)

#%% [markdown]
#### JxC
#%%
# Resultados del JxC en cada mesa solo para Presidente
resultCABA_pres_jxc = resultCABA[(resultCABA["NOMBRE_CATEGORIA"] == "Presidente y Vicepresidente de la República") & (resultCABA["NOMBRE_AGRUPACION"] == "JUNTOS POR EL CAMBIO")]
resultCABA_pres_jxc
#%%
# Porcentaje de Diputados Nacionales del JxC por circuito
porc_pres_circ_jxc = porcentaje_circuito(resultCABA_pres_total, resultCABA_pres_jxc)

#%%
# Porcentaje de Diputados Nacionales del JxC por comuna
porc_pres_comuna_jxc = porcentaje_comuna(porc_pres_circ_jxc)
porc_pres_comuna_jxc

#%%
# Resultados del JxC en cada mesa solo para Presidente
resultCABA_dip_jxc = resultCABA[(resultCABA["NOMBRE_CATEGORIA"] == "Diputados Nacionales Ciudad Autónoma de Buenos Aires") & (resultCABA["NOMBRE_AGRUPACION"] == "JUNTOS POR EL CAMBIO")]
resultCABA_dip_jxc
#%%
# Porcentaje de Diputados Nacionales del JxC por circuito
porc_dip_circ_jxc = porcentaje_circuito(resultCABA_dip_total, resultCABA_dip_jxc)
porc_dip_circ_jxc
#%%
# Porcentaje de Diputados Nacionales del JxC por comuna
porc_dip_comuna_jxc = porcentaje_comuna(porc_dip_circ_jxc)
porc_dip_comuna_jxc
# %%
# Diferencia entre el voto Presidente y Diputado en JxC por COMUNA
diferencia_jxc_comuna = corte_boleta(porc_pres_comuna_jxc, porc_dip_comuna_jxc)
diferencia_jxc_comuna[["PORCENTAJE_AGRUPACION_PRES","PORCENTAJE_AGRUPACION_DIP", "DIFERENCIA_DIP_PRES"]]
# %%
# Diferencia entre el voto Presidente y Diputado en JxC por CIRCUITO
diferencia_jxc_circ = corte_boleta(porc_pres_circ_jxc, porc_dip_circ_jxc)
diferencia_jxc_circ

#%% [markdown]
#### CONSENSO FEDERAL
#%%
# Resultados del cf en cada mesa solo para Presidente
resultCABA_pres_cf = resultCABA[(resultCABA["NOMBRE_CATEGORIA"] == "Presidente y Vicepresidente de la República") & (resultCABA["NOMBRE_AGRUPACION"] == "CONSENSO FEDERAL")]
resultCABA_pres_cf
#%%
# Porcentaje de Diputados Nacionales del cf por circuito
porc_pres_circ_cf = porcentaje_circuito(resultCABA_pres_total, resultCABA_pres_cf)

#%%
# Porcentaje de Diputados Nacionales del cf por comuna
porc_pres_comuna_cf = porcentaje_comuna(porc_pres_circ_cf)
porc_pres_comuna_cf

#%%
# Resultados del cf en cada mesa solo para Presidente
resultCABA_dip_cf = resultCABA[(resultCABA["NOMBRE_CATEGORIA"] == "Diputados Nacionales Ciudad Autónoma de Buenos Aires") & (resultCABA["NOMBRE_AGRUPACION"] == "CONSENSO FEDERAL")]
resultCABA_dip_cf
#%%
# Porcentaje de Diputados Nacionales del cf por circuito
porc_dip_circ_cf = porcentaje_circuito(resultCABA_dip_total, resultCABA_dip_cf)
porc_dip_circ_cf
#%%
# Porcentaje de Diputados Nacionales del cf por comuna
porc_dip_comuna_cf = porcentaje_comuna(porc_dip_circ_cf)
porc_dip_comuna_cf
# %%
# Diferencia entre el voto Presidente y Diputado en cf por COMUNA
diferencia_cf_comuna = corte_boleta(porc_pres_comuna_cf, porc_dip_comuna_cf)
diferencia_cf_comuna[["PORCENTAJE_AGRUPACION_PRES","PORCENTAJE_AGRUPACION_DIP", "DIFERENCIA_DIP_PRES"]]
# %%
# Diferencia entre el voto Presidente y Diputado en cf por CIRCUITO
diferencia_cf_circ = corte_boleta(porc_pres_circ_cf, porc_dip_circ_cf)
diferencia_cf_circ

#%% [markdown]
#### UNITE POR LA LIBERTAD Y LA DIGNIDAD
#%%
# Resultados del uld en cada mesa solo para Presidente
resultCABA_pres_uld = resultCABA[(resultCABA["NOMBRE_CATEGORIA"] == "Presidente y Vicepresidente de la República") & (resultCABA["NOMBRE_AGRUPACION"] == "UNITE POR LA LIBERTAD Y LA DIGNIDAD")]
resultCABA_pres_uld
#%%
# Porcentaje de Diputados Nacionales del uld por circuito
porc_pres_circ_uld = porcentaje_circuito(resultCABA_pres_total, resultCABA_pres_uld)

#%%
# Porcentaje de Diputados Nacionales del uld por comuna
porc_pres_comuna_uld = porcentaje_comuna(porc_pres_circ_uld)
porc_pres_comuna_uld

#%%
# Resultados del uld en cada mesa solo para Presidente
resultCABA_dip_uld = resultCABA[(resultCABA["NOMBRE_CATEGORIA"] == "Diputados Nacionales Ciudad Autónoma de Buenos Aires") & (resultCABA["NOMBRE_AGRUPACION"] == "UNITE POR LA LIBERTAD Y LA DIGNIDAD")]
resultCABA_dip_uld
#%%
# Porcentaje de Diputados Nacionales del uld por circuito
porc_dip_circ_uld = porcentaje_circuito(resultCABA_dip_total, resultCABA_dip_uld)
porc_dip_circ_uld
#%%
# Porcentaje de Diputados Nacionales del uld por comuna
porc_dip_comuna_uld = porcentaje_comuna(porc_dip_circ_uld)
porc_dip_comuna_uld
# %%
# Diferencia entre el voto Presidente y Diputado en uld por COMUNA
diferencia_uld_comuna = corte_boleta(porc_pres_comuna_uld, porc_dip_comuna_uld)
diferencia_uld_comuna[["PORCENTAJE_AGRUPACION_PRES","PORCENTAJE_AGRUPACION_DIP", "DIFERENCIA_DIP_PRES"]]
# %%
# Diferencia entre el voto Presidente y Diputado en uld por CIRCUITO
diferencia_uld_circ = corte_boleta(porc_pres_circ_uld, porc_dip_circ_uld)
diferencia_uld_circ

#%% [markdown]
#### BLANCO
#%%
# Resultados del blanco en cada mesa solo para Presidente
resultCABA_pres_blanco = resultCABA[(resultCABA["NOMBRE_CATEGORIA"] == "Presidente y Vicepresidente de la República") & (resultCABA["NOMBRE_AGRUPACION"] == "BLANCO")]
resultCABA_pres_blanco
#%%
# Porcentaje de Diputados Nacionales del blanco por circuito
porc_pres_circ_blanco = porcentaje_circuito(resultCABA_pres_total, resultCABA_pres_blanco)
porc_pres_circ_blanco
#%%
# Porcentaje de Diputados Nacionales del blanco por comuna
porc_pres_comuna_blanco = porcentaje_comuna(porc_pres_circ_blanco)
porc_pres_comuna_blanco

#%%
# Resultados del blanco en cada mesa solo para Presidente
resultCABA_dip_blanco = resultCABA[(resultCABA["NOMBRE_CATEGORIA"] == "Diputados Nacionales Ciudad Autónoma de Buenos Aires") & (resultCABA["NOMBRE_AGRUPACION"] == "BLANCO")]
resultCABA_dip_blanco
#%%
# Porcentaje de Diputados Nacionales del blanco por circuito
porc_dip_circ_blanco = porcentaje_circuito(resultCABA_dip_total, resultCABA_dip_blanco)
porc_dip_circ_blanco
#%%
# Porcentaje de Diputados Nacionales del blanco por comuna
porc_dip_comuna_blanco = porcentaje_comuna(porc_dip_circ_blanco)
porc_dip_comuna_blanco
# %%
# Diferencia entre el voto Presidente y Diputado en blanco por COMUNA
diferencia_blanco_comuna = corte_boleta(porc_pres_comuna_blanco, porc_dip_comuna_blanco)
diferencia_blanco_comuna[["PORCENTAJE_AGRUPACION_PRES","PORCENTAJE_AGRUPACION_DIP", "DIFERENCIA_DIP_PRES"]]
# %%
# Diferencia entre el voto Presidente y Diputado en blanco por CIRCUITO
diferencia_blanco_circ = corte_boleta(porc_pres_circ_blanco, porc_dip_circ_blanco)
diferencia_blanco_circ

#%%
# Preparo todo para el merge: Renombro las columnas y me quedo solo con las que me interesan

diferencia_blanco_comuna = diferencia_blanco_comuna.rename(columns={"DIFERENCIA_DIP_PRES": "DIFERENCIA_BLANCO"})
diferencia_blanco_circ = diferencia_blanco_circ.rename(columns={"DIFERENCIA_DIP_PRES": "DIFERENCIA_BLANCO"})
sub_diferencia_blanco_circ = diferencia_blanco_circ["DIFERENCIA_BLANCO"]
sub_diferencia_blanco_comuna = diferencia_blanco_comuna["DIFERENCIA_BLANCO"]

diferencia_uld_comuna = diferencia_uld_comuna.rename(columns={"DIFERENCIA_DIP_PRES": "DIFERENCIA_ULD"})
diferencia_uld_circ = diferencia_uld_circ.rename(columns={"DIFERENCIA_DIP_PRES": "DIFERENCIA_ULD"})
sub_diferencia_uld_circ = diferencia_uld_circ["DIFERENCIA_ULD"]
sub_diferencia_uld_comuna = diferencia_uld_comuna["DIFERENCIA_ULD"]

diferencia_fit_comuna = diferencia_fit_comuna.rename(columns={"DIFERENCIA_DIP_PRES": "DIFERENCIA_FIT"})
diferencia_fit_circ = diferencia_fit_circ.rename(columns={"DIFERENCIA_DIP_PRES": "DIFERENCIA_FIT"})
sub_diferencia_fit_circ = diferencia_fit_circ["DIFERENCIA_FIT"]
sub_diferencia_fit_comuna = diferencia_fit_comuna["DIFERENCIA_FIT"]

diferencia_cf_comuna = diferencia_cf_comuna.rename(columns={"DIFERENCIA_DIP_PRES": "DIFERENCIA_CF"})
diferencia_cf_circ = diferencia_cf_circ.rename(columns={"DIFERENCIA_DIP_PRES": "DIFERENCIA_CF"})
sub_diferencia_cf_circ = diferencia_cf_circ["DIFERENCIA_CF"]
sub_diferencia_cf_comuna = diferencia_cf_comuna["DIFERENCIA_CF"]

diferencia_fdt_comuna = diferencia_fdt_comuna.rename(columns={"DIFERENCIA_DIP_PRES": "DIFERENCIA_FDT"})
diferencia_fdt_circ = diferencia_fdt_circ.rename(columns={"DIFERENCIA_DIP_PRES": "DIFERENCIA_FDT"})
sub_diferencia_fdt_circ = diferencia_fdt_circ["DIFERENCIA_FDT"]
sub_diferencia_fdt_comuna = diferencia_fdt_comuna["DIFERENCIA_FDT"]

diferencia_jxc_comuna = diferencia_jxc_comuna.rename(columns={"DIFERENCIA_DIP_PRES": "DIFERENCIA_JXC"})
diferencia_jxc_circ = diferencia_jxc_circ.rename(columns={"DIFERENCIA_DIP_PRES": "DIFERENCIA_JXC"})
sub_diferencia_jxc_circ = diferencia_jxc_circ["DIFERENCIA_JXC"]
sub_diferencia_jxc_comuna = diferencia_jxc_comuna["DIFERENCIA_JXC"]

# %%
# Comparación de diferencias por COMUNA

comparacion_diferencia_comuna = pd.concat([sub_diferencia_jxc_comuna, sub_diferencia_fdt_comuna, 
                                            sub_diferencia_cf_comuna, sub_diferencia_fit_comuna, sub_diferencia_blanco_comuna],
                                            axis=1)

comparacion_diferencia_comuna.head(15)
# %%
# Comparación de diferencias por CIRCUITO

comparacion_diferencia_circuito = pd.concat([sub_diferencia_jxc_circ, sub_diferencia_fdt_circ, 
                                            sub_diferencia_cf_circ, sub_diferencia_fit_circ, sub_diferencia_blanco_circ],
                                            axis=1)
                            
comparacion_diferencia_circuito
# %%
