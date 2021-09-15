'''numero_ingresado = input("Por favor ingrese un numero entero: ")
try:
    numero_ingresado = int(numero_ingresado)
except:
    print("Usted no ingresó un número entero")

primos = {
    1: 2,
    2: 3,
    3: 5,
    4: 7,
    5: 11,
    6: 13
}

def encontrar_numero_primo(numero_ingresado):

    if numero_ingresado in primos:
        print(F"El primo número {numero_ingresado}, es el número {primos[numero_ingresado]}")

    else:'''





#______________________________________________________________________________-


'''es_primo = input("Ingrese un número natural: ")

try:
    es_primo = int(es_primo)
except:
    print("No ingresó un número natural")



def ver_si_es_primo(numero):
    #Verifica si el número es primo, dividiendolo entre los numeros enteros de 2 a si mismo -1
    primo = True # Empezamos asumiendo que el número es primo

    for numero in range(2, es_primo): # Dividimos el número por todos los números entre 2 y el número ingresado menos 1
        if es_primo % numero == 0: # Si alguna de esas divisiones da como resto 0, definimos al numero como NO primo (primo = False)
            primo = False
            break # Salimos del ciclo

    return primo'''

#----------------------------------------------------------------------------------------------------

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
    


def ver_si_es_primo(numero):
    primo = True

    if numero not in primos.values():

        for clave, valor in primos.items():

            if numero % valor == 0:
                primo = False
                break

    return primo



'''es_primo = input("Ingrese un número natural: ")

try:
    es_primo = int(es_primo)
except:
    print("No ingresó un número natural")


respuesta_es_primo = ver_si_es_primo(es_primo)

print(es_primo, respuesta_es_primo)'''


