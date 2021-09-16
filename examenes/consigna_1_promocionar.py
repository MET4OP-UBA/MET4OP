"""Declarar una función que, dado un número x, sea capaz de sumar todos los números menores de x que sean 
múltiplos de 2 excepto aquellos que sean también múltiplos de 4. (1 punto) 
Por ejemplo: suma (10) = 2+ 6 + 10 = 18"""

def suma_acumulada(x):
    lista_numeros = [] # armo lista vacia 
    for i in range(0, x+1):
        if i%2 == 0 and i%4 != 0: # solo si los numeros son multiplos de 2 pero no de 4
            lista_numeros.append(i)
    #print(lista_numeros) # revisar!
    # falta sumar todos los numeros de la lista
    suma = 0 # valor inicial
    for n in range(0, len(lista_numeros)): # del 0 hasta x
        suma = suma + lista_numeros[n]
    return suma

# Ejemplo
suma_acumulada(1000)
