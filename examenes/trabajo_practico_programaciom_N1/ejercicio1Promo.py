#1. Declarar una función que, dado un número x, sea capaz de sumar todos los números
#menores de x que sean múltiplos de 2 excepto aquellos que sean también múltiplos
#de 4. (1 punto) Por ejemplo: suma (10) = 2 + 6 + 10 = 18

def suma_numeros_menores_x(numero):
    acumulador = 0
    for num in range(1,numero+1): #numero+1 para que incluye al ultimo
        if i%2==0 and not(i%4==0): #si el numero es divisor de 2, el residuo es 0, y no divisor de 4
            acumulador= acumulador + num #0+i y despues reemplaza a 0 por el proximo numero cuando se cumpla condicion de arriba
    print("El resultado es: ", acumulador)
        
numero=int(input("Ingrese número: "))
suma_numeros_menores_x(numero)