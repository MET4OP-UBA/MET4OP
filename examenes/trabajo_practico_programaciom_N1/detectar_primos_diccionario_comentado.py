import time  # Importo el módulo "time" para poder calcular el tiempo total de ejecución del código

diccionario_primos = {1: 2} # Inicializo un diccionario como variable global, para poder usarlo y guardar los datos que
                            # se generen en la ejecusión de la función

def encontrar_primo(posicion_primo_solicitada): # Declaro la función
    '''Se ingresa un número como parámetro y la función devuelve el numero primo ubicado en la posición que se ingresó'''

    posicion_primo_solicitada = int(posicion_primo_solicitada)  # Intento convertir el valor ingresado en un int,
                                                                # lo hago acá adentro para que sea indistinto el modo
                                                                # de ingreso del valor, si no es posible se rompe el
                                                                # programa y devuelve un ValueError

    if posicion_primo_solicitada < 1:
        raise ValueError("El número que ingresó es 0 o es negativo") # Si la posición solicitada es menor a 1, el
                                                                     # programa se rompe y devuelve un ValueEror con
                                                                     # un mensaje que avisa "El número que ingresó es 0
                                                                     # o es negativo"

    if posicion_primo_solicitada in diccionario_primos.keys(): # Si la posición solicitada ya está guardada en el diccionario
        print(F'El primo número {posicion_primo_solicitada} es el {diccionario_primos[posicion_primo_solicitada]}') # Imprime este mensaje
        return diccionario_primos[posicion_primo_solicitada] # Termina con el programa y retorna el primo correspondiente

    posicion_primo = len(diccionario_primos) # Creo la variable local "posición primo" y le asigno el largo del
                                             # diccionario, es decir, la posición del último primo guardado

    siguiente_numero = diccionario_primos[posicion_primo] #Creo la variable local "siguiente número" y le asigno el
                                                          # último primo que tengo guardado en el diccionario de primos

    while posicion_primo != posicion_primo_solicitada: # Mientras la posición del primo actual sea diferente a la
                                                       # posición solicitada por el usuario

        siguiente_numero += 1 # Sumale 1 al último primo guardado, luego al siguiente del último primo guardado, y así
        es_primo = True # Partimos asumiendo que el número con el que estamos trabajando ahora ("siguiente_numero") es primo (True)

        for primo in diccionario_primos.values(): # Vamos a iterar sobre el diccionario de primos que tenemos guardado, por cada primo del diccionario
            if siguiente_numero % primo == 0: # Si el número con el que estamos trabajando dividido por el primo actual da cero
                es_primo = False # Entonces el número con el que estamos trabajando (siguiente_numero) NO es primo (False)
                break # Y se rompe el ciclo for

        if es_primo: # Si dividimos el número actual (siguiente_numero) por todos los primos y ninguno dió resto cero
                     # entonces ese número es primo (es_primo = True)
            posicion_primo += 1 # En ese caso le sumamos 1 a la última posición, para guardar el npumero primo que encontramos
            diccionario_primos[posicion_primo] = siguiente_numero #Finalmente guardamos el último primo que encontramos
                                                                  # en la posición siguiente a la última guardada

            # Y volvemos al inicio del ciclo while para comprobar si la posición_primo actual es la solicitada por el
            # usuario, si es así se termina el ciclo, imprimimos el mensaje de abajo y retornamos el número primo de la
            # posición solicitada, en caso contrario repetimos el proceso anterior con el siguiente número

    print(F'El primo número {posicion_primo_solicitada} es el {diccionario_primos[posicion_primo_solicitada]}')
    return diccionario_primos[posicion_primo_solicitada]


# En este sector del código definimos el número que vamos a usar y llamamos a la función, además iniciamos y detenemos
# el contador de tiempo para calcular cuánto tarda la ejecución de nuestra función

primo_numero_x = (input("Por favor ingrese un numero entero positivo para saber el numero primo que se encuentra en esa posición: "))

inicio = time.time()

primo_numero_x = encontrar_primo(primo_numero_x)
print(primo_numero_x)

fin = time.time()

print(fin-inicio)