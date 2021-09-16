# Le pedimos al usuario que ingrese un número, el cuál será el índice del primo que quiere encontrar

indice_primo = input("Por favor ingrese un numero entero: ")
try:
    indice_primo = int(indice_primo)
except:
    print("Usted no ingresó un número entero")



# Definimos un diccionario con los 6 primeros números primos, cuyas claves son los índices y sus valores son
# los números primos correspondientes a esos índices

diccionario_primos = {
    1: 2,
    2: 3,
    3: 5,
    4: 7,
    5: 11,
    6: 13
}



# Vamos a ver si ese número y su índice están en el diccionario de primos que tenemos

if indice_primo in diccionario_primos.keys():
    print(F'El primo número {indice_primo} es el {diccionario_primos[indice_primo]}')
else:
    pass #Acá vamos a poner la función y pasarle como parámetro nuestro número, pero hay que armar cosas antes



def encontrar_primo(numero_ingresado):

    contador = len(diccionario_primos)

    ultimo_primo = diccionario_primos[contador] + 1

    while contador != numero_ingresado:

        ultimo_primo += 1

        primo = True

        for valor in diccionario_primos.values():
            if ultimo_primo % valor == 0:
                primo = False
                break

        if primo == True:
            contador += 1
            diccionario_primos[contador] = ultimo_primo

    print(F'El primo número {numero_ingresado} es el {diccionario_primos[numero_ingresado]}')

    return diccionario_primos


primo_numero_x = encontrar_primo(indice_primo)
print(diccionario_primos)
