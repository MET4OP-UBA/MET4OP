# %%
import numpy as np
import pandas as pd

# Decidí hacerlo en un DF de pandas para poder operar más fácil (divisiones y multiplicaciones)

votos = {"Partido": ["JxC", "FdT", "CF","FIT", "UNITE", "AyL"],
        "Votos": [1060404, 641054, 114968, 122560, 36420, 24685],
        "Cociente": [1, 1, 1, 1, 1, 1]}

votosDF = pd.DataFrame(votos, 
                        columns=["Partido", "Votos", "Cociente"])

# Las bancas en juego son la cantidad de iteraciones que debe hacer
bancas_en_juego = 12

# La idea del método D'Hondt es que divide todos los candidatos por un cociente inicial de 1, y el valor máximo se lleva la banca
# En la siguiente iteración, el cociente del candidato que se llevó la última banca aumenta en 1. Por lo que pasaría a dividir por 2. 
# Y así sucesivamente se van aumentando los cocientes cada vez que se consigue una banca
# La cantidad de bancas es igual al cociente final -1 (porque las bancas comienzan en 0, y los cocientes comienzan en 1)

# En cuanto al código, primero divide por el cociente, luego aumenta en 1 al cociente del mayor producto de la división, 
# y luego vuelve a multiplicar por el cociente para que la siguiente iteración se haga dividiendo los votos originales, en lugar de votos/cociente.
# En el medio también crea otro DF para usar su cociente para multiplicar por los votos, para que Votos no quede más grande que su número original

for i in range(1,bancas_en_juego+1):
    
    votosDF["Votos"] = votosDF[["Votos"]].div(votosDF["Cociente"], axis=0)           # Divide Votos por su cociente (inicialmente 1)
    
    votosDF.loc[votosDF["Votos"] == votosDF["Votos"].max() , "Cociente"] += 1        # +1 al cociente del producto max de la división

    votosDF_1 = votosDF.copy()                                                       # Crea un nuevo DF, para que multiplique su cociente
    votosDF_1.loc[votosDF_1["Votos"] == votosDF_1["Votos"].max() , "Cociente"] -= 1  # Le resta 1 al nuevo DF
    
    votosDF["Votos"] = votosDF["Votos"] * votosDF_1["Cociente"]                      # Multiplica Votos por el cociente del nuevo DF

# ! Luego convertir Cociente en Bancas y restarle 1

bancas_final = votosDF.rename(columns={"Cociente": "Bancas"})
bancas_final["Bancas"] -= 1
print(bancas_final)