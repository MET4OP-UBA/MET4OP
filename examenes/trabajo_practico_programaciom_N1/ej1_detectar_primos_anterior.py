
def ver_si_es_primo(numero_ingresado):
    '''Verifica si el número es primo, dividiendolo entre los numeros enteros de 2 a si mismo -1'''
    primo = True # Empezamos asumiendo que el número es primo

    for numero in range(2, numero_ingresado): # Dividimos el número por todos los números entre 2 y el número ingresado menos 1
        if numero_ingresado % numero == 0: # Si alguna de esas divisiones da como resto 0, definimos al numero como NO primo (primo = False)
            primo = False
            break # Salimos del ciclo

    return primo

# Defino una variable en la que voy a meter al número que estoy llamando
es_primo = input("Ingrese un número natural: ")


# Lo que ingrese por input es un string, así que intento transformarlo a int, y si falla tiro una excepción

try:
    es_primo = int(es_primo)
except:
    print("No ingresó un número natural")


# Le aplico la función "ver si es primo" al número ingresado e imprimo por pantalla el número + True, si es primo
# y el número + False, si no es primo

respuesta_es_primo = ver_si_es_primo(es_primo)

print(es_primo, respuesta_es_primo)