# Sabemos que el día 1970-01-01 fue jueves. Declarar una función que pueda indicar
# cuántos jueves han sido el primer día de cada mes desde entonces. La fecha de corte
# debe de poder ser cualquiera. (1 punto)

import dateutil
from datetime import datetime
from dateutil.relativedelta import relativedelta


fecha_inicial = datetime(1970, 1, 1)

fecha_de_corte = datetime.strptime(input('Por favor ingrese una fecha de corte, escrita en números, con el formato '
                                         'año_completo/mes/día (por ejemplo 2021/1/3 o 2021/01/03): '), '%Y/%m/%d')


def contar_primeros_jueves_del_mes(fecha_inicial, fecha_de_corte):
    '''Dada una fecha de inicio y una fecha de corte, la función calcula la cantidad de primeros días del mes que
    cayeron jueves en ese intervalo de tiempo'''

    contador_de_jueves = 0
    fecha_dada = fecha_inicial

    while fecha_dada <= fecha_de_corte:
        fecha_dada += relativedelta(months=1)
        if datetime.strftime(fecha_dada, '%A') == 'Thursday':
            contador_de_jueves += 1

    return contador_de_jueves


cantidad_de_jueves = contar_primeros_jueves_del_mes(fecha_inicial, fecha_de_corte)

print(cantidad_de_jueves)

