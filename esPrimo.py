def esPrimo(x):
    divisores = 0 #Cuntos divisores tiene. Tiene que ser 2.
    contador = 1 #x=5 --- contador = 1,2,3,4,5
    while divisores < 3 and contador <= x:
        cociente = x/contador
        if cociente.is_integer() == True:
            divisores = divisores + 1
        contador = contador + 1

    if divisores > 2:
        return False
    else: 
        return True
esPrimo(100)

def buscarPrimo(x):
    valor = 0 #Cuantos numeros primos encontre hasta el momento
    iterador = 2 #Desde que numero empiezo a iterar
    while valor != x:
        resultado = esPrimo(iterador) 
        if resultado:
            valor = valor + 1
            if valor == x:
                break

        iterador = iterador + 1
    return iterador
    