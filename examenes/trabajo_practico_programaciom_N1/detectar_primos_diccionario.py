import time

diccionario_primos = {1: 2}

def encontrar_primo(posicion_primo_solicitada):
    '''Se ingresa un número como parámetro y la función devuelve el numero primo ubicado en la posición que se ingresó'''

    posicion_primo_solicitada = int(posicion_primo_solicitada)

    if posicion_primo_solicitada < 1:
        raise ValueError("El número que ingresó es 0 o es negativo")

    if posicion_primo_solicitada in diccionario_primos.keys():
        print(F'El primo número {posicion_primo_solicitada} es el {diccionario_primos[posicion_primo_solicitada]}')
        return diccionario_primos[posicion_primo_solicitada]

    posicion_primo = len(diccionario_primos)
    siguiente_numero = diccionario_primos[posicion_primo]

    while posicion_primo != posicion_primo_solicitada:

        siguiente_numero += 1
        es_primo = True

        for primo in diccionario_primos.values():
            if siguiente_numero % primo == 0:
                es_primo = False
                break

        if es_primo:
            posicion_primo += 1
            diccionario_primos[posicion_primo] = siguiente_numero

    print(F'El primo número {posicion_primo_solicitada} es el {diccionario_primos[posicion_primo_solicitada]}')
    return diccionario_primos[posicion_primo_solicitada]

inicio = time.time()

primo_numero_x = encontrar_primo(input("Por favor ingrese un numero entero positivo para saber el numero primo que se encuentra en esa posición: "))
print(primo_numero_x)


fin = time.time()

print(fin-inicio)