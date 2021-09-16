# Le pedimos al usuario que ingrese un número, el cuál será el índice del primo que quiere encontrar

indice_primo = input("Por favor ingrese un numero entero positivo para saber el numero primo que se encuentra en esa posición: ")

try:
    indice_primo = int(indice_primo)

except:
    indice_primo = 0


diccionario_primos = {
        1: 2,
        2: 3,
        3: 5,
        4: 7,
        5: 11,
        6: 13
    }

def encontrar_primo(numero_ingresado):

    if numero_ingresado < 1:
        print("Usted no ingresó un número entero positivo")

    elif numero_ingresado in diccionario_primos.keys():
        print(F'El primo número {indice_primo} es el {diccionario_primos[indice_primo]}')

    else:

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