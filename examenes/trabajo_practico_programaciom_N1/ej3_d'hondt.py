# %%
import pandas as pd

# Toda esta sección es para armar el DataFrame con el que se va a iterar
info_correcta = False

while info_correcta != True:    # Este while es para que si ver los datos ingresados te percatás de un error, puedas volver a ingresar datos

    # Estas listas son las que se van a ir agregando con los inputs del usuario, y a partir de ellas se crea el DataFrame
    lista_cocientes = []
    lista_partidos = []
    lista_votos = []

    n_partidos = int(input("Ingrese el número de partidos: "))

    for i in range(0,n_partidos):
        lista_cocientes.append(1)                                                                                   # Como para dividir la primera iteración necesito que divida Votos / 1, agrega un 1 a la lista de Cocientes por cada partido
        partidos = str(input(f" {len(lista_cocientes)}) Ingrese el nombre del partido: "))                           
        lista_partidos.append(partidos)
        votos = int(input(f" {len(lista_cocientes)}) Ingrese la cantidad de votos de {lista_partidos[-1]}: "))
        lista_votos.append(votos)
 
    # Esta sección construye el DataFrame a partir de las listas creadas en el for anerior
    votos_d ={"Partido": lista_partidos, "Votos": lista_votos, "Cociente": lista_cocientes}
    votosDF = pd.DataFrame(votos_d)     
    print(votosDF[["Partido","Votos"]])
   
    # Y aquí dependiendo del input del usuario se repite el proceso o continúa
    x = input("Indique si la información presentada en la tabla anterior es correcta (si/no)")  
    if x == "si":
        info_correcta = True
    elif x == "no":
        info_correcta = False 


# Las bancas en juego son la cantidad de iteraciones que debe hacer
bancas_en_juego = int(input("Ingrese la cantidad de bancas a repartir: "))

# En cuanto al código, primero divide por el cociente, luego aumenta en 1 al cociente del mayor producto de la división, 
# y luego vuelve a multiplicar por el cociente para que la siguiente iteración se haga dividiendo los votos originales, en lugar de votos/cociente.
# En el medio también crea otro DF para usar su cociente para multiplicar por los votos, para que Votos no quede más grande que su número original

for i in range(0,bancas_en_juego):
    
    votosDF["Votos"] = votosDF[["Votos"]].div(votosDF["Cociente"], axis=0)           # Divide Votos por su cociente (inicialmente 1)
    
    votosDF.loc[votosDF["Votos"] == votosDF["Votos"].max() , "Cociente"] += 1        # +1 al cociente del producto max de la división

    votosDF_1 = votosDF.copy()                                                       # Crea un nuevo DF, para que multiplique su cociente
    votosDF_1.loc[votosDF_1["Votos"] == votosDF_1["Votos"].max() , "Cociente"] -= 1  # Le resta 1 al nuevo DF
    
    votosDF["Votos"] = votosDF["Votos"] * votosDF_1["Cociente"]                      # Multiplica Votos por el cociente del nuevo DF

#  Luego convertir Cociente en Bancas y restarle 1
bancas_final = votosDF.rename(columns={"Cociente": "Bancas"})
bancas_final["Bancas"] -= 1
print(bancas_final)

