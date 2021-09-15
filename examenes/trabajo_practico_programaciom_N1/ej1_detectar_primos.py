# No sé si sirve, pero es algo. Un programa que te diga si un número es primo o no
x = int(input("Ingrese un número natural: "))
primo = False #bandera

for i in range(2, x):
    print(i)
    if x % i != 0: # La idea es que si la división entre el X que ingresa el usuario y el rango entre 2 y x-1 siempre da resto 0, entonces es primo
        print( x, "dividido", i, "NO da resto 0") # Este paso es innecesario y se puede sacar, solo sirve para ir viendo todo el proceso que hace por cada numero que divide
        primo = True
    elif x % i == 0:
        print( x, "dividido", i, "SÍ da resto 0") # Este paso es innecesario y se puede sacar, solo sirve para ir viendo todo el proceso que hace por cada numero que divide
        primo = False
        break # El break para que a la primera que llegue a un resto 0 ya lo determine como compuesto, y no siga iterando


if primo == True:
    print("El número es primo")
elif primo == False:
    print("El número es compuesto")