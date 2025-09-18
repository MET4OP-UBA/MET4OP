# %% [markdown]
# # Introducción a la Distribución Normal y el Puntaje Z en Python

# **Contenidos:**
# 1.  **El Puntaje Z**: Qué es y cómo se calcula para un solo dato.
# 2.  **Simulación de Datos**: Cómo generar datos que sigan una distribución normal y ver la diferencia entre la teoría y una muestra.
# 3.  **Cálculo de Probabilidades**: Usar el puntaje z para responder preguntas como "¿qué porcentaje de la gente tiene más de X simpatía?".
# 4.  **Normalización para Comparar Grupos**: El caso de estudio de dos regiones, donde estandarizamos los datos para poder compararlos de manera justa.
# 5.  **Aplicación Práctica**: Un ejemplo concreto que muestra por qué la normalización es útil.

# %%
# Importamos las librerías que vamos a necesitar
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm

# Fijamos una semilla para que los resultados aleatorios sean siempre los mismos
np.random.seed(123)

# %% [markdown]
# ## 1. El Puntaje Z: ¿Qué es y cómo se calcula?
#
# El **puntaje Z** nos dice a cuántas desviaciones estándar se encuentra un valor específico de la media del grupo. Es la medida más básica de la posición relativa de un dato.
#
# La fórmula es: $z = \frac{(x - \mu)}{\sigma}$
#
# - $x$: El valor que queremos analizar.
# - $\mu$ (mu): La media de la población.
# - $\sigma$ (sigma): La desviación estándar de la población.
#
# **Escenario**: Analizamos la simpatía hacia un candidato político en una escala de 0 a 100. Sabemos que la simpatía promedio ($\mu$) en la población es de **55 puntos**, con una desviación estándar ($\sigma$) de **12 puntos**.
#
# **Pregunta**: ¿Qué tan común o rara es una persona con **70 puntos** de simpatía?

# %%
# Parámetros de la población (teóricos)
media_poblacional = 55
desvio_poblacional = 12

# Nuestro caso observado
valor_observado = 70

# Calculamos el puntaje Z
puntaje_z = (valor_observado - media_poblacional) / desvio_poblacional

print(f"El puntaje Z para un valor de {valor_observado} es: {puntaje_z:.2f}")
print(f"Esto significa que una simpatía de {valor_observado} está a {puntaje_z:.2f} desviaciones estándar por encima de la media.")

# %% [markdown]
# ## 2. De la Teoría a la Práctica: Simulación de Datos
#
# La distribución normal teórica es una curva perfecta. En la realidad, los datos de una muestra nunca son perfectos. Vamos a ver cómo se compara una muestra simulada con la teoría.
#
# ### 2.a. Simulación con una Muestra Pequeña (N=50)
#
# Con pocos datos, la distribución real puede ser bastante diferente de la curva teórica ideal.

# %%
# Tamaño de la muestra pequeña
N_pequeno = 50

# Generamos 50 casos que siguen una distribución Normal(μ=55, σ=12)
simulacion_pequena = np.random.normal(loc=media_poblacional, scale=desvio_poblacional, size=N_pequeno)

# Graficamos el histograma de nuestra muestra y la curva teórica
plt.figure(figsize=(8, 5))
plt.hist(simulacion_pequena, bins=10, density=True, edgecolor="black", alpha=0.7, label="Muestra Simulada (N=50)")

# Superponemos la curva de densidad de probabilidad teórica
x_grid = np.linspace(0, 100, 200)
curva_teorica = norm.pdf(x_grid, loc=media_poblacional, scale=desvio_poblacional)
plt.plot(x_grid, curva_teorica, color='red', linewidth=2, label="Distribución Teórica Ideal")

plt.title("Muestra Pequeña vs. Distribución Teórica")
plt.xlabel("Nivel de Simpatía")
plt.ylabel("Densidad")
plt.legend()
plt.show()

# %% [markdown]
# **Observación**: Fíjate cómo el histograma (los datos reales de la muestra) no se ajusta perfectamente a la curva roja (la teoría). Hay "huecos" y "picos". Esto es la **variabilidad del muestreo**.
#
# ### 2.b. Simulación con una Muestra Grande (N=10,000)
#
# Según la **Ley de los Grandes Números**, a medida que aumenta el tamaño de la muestra, la distribución de los datos se parecerá cada vez más a la distribución teórica.

# %%
# Tamaño de la muestra grande
N_grande = 10000

# Generamos 10,000 casos
simulacion_grande = np.random.normal(loc=media_poblacional, scale=desvio_poblacional, size=N_grande)

# Graficamos de nuevo
plt.figure(figsize=(8, 5))
plt.hist(simulacion_grande, bins=30, density=True, edgecolor="black", alpha=0.7, label="Muestra Simulada (N=10,000)")

# Superponemos la curva teórica
plt.plot(x_grid, curva_teorica, color='red', linewidth=2, label="Distribución Teórica Ideal")

plt.title("Muestra Grande vs. Distribución Teórica")
plt.xlabel("Nivel de Simpatía")
plt.ylabel("Densidad")
plt.legend()
plt.show()

# %% [markdown]
# **Observación**: ¡Ahora sí! Con 10,000 casos, el histograma de la muestra es un reflejo casi perfecto de la curva teórica. Esto nos da confianza para usar la teoría para calcular probabilidades.

# %% [markdown]
# ## 3. Calculando Probabilidades y Percentiles
#
# Ahora que confiamos en nuestro modelo, podemos usar la distribución normal teórica para responder preguntas sobre la probabilidad.
#
# **Preguntas:**
# a) ¿Qué porcentaje de personas tiene una simpatía **menor a 60**? `P(X < 60)`
# b) ¿Qué porcentaje de personas tiene una simpatía **mayor a 70**? `P(X > 70)`
# c) ¿Qué nivel de simpatía es necesario para estar en el **percentil 80** (es decir, superar al 80% de la gente)?

# %%
# a) Probabilidad de tener una simpatía MENOR a 60
valor_a = 60
z_a = (valor_a - media_poblacional) / desvio_poblacional
prob_a = norm.cdf(z_a)
print(f"a) La probabilidad de tener una simpatía menor a {valor_a} es: {prob_a:.4f} (o {prob_a*100:.2f}%)")

# b) Probabilidad de tener una simpatía MAYOR a 70
valor_b = 70
z_b = (valor_b - media_poblacional) / desvio_poblacional
prob_b = 1 - norm.cdf(z_b) # Usamos 1 - cdf() porque queremos el área a la DERECHA de la curva
print(f"b) La probabilidad de tener una simpatía mayor a {valor_b} es: {prob_b:.4f} (o {prob_b*100:.2f}%)")

# c) Calcular el valor que corresponde al percentil 80
percentil_80 = norm.ppf(0.80, loc=media_poblacional, scale=desvio_poblacional)
print(f"c) Para estar en el percentil 80, se necesita un nivel de simpatía de: {percentil_80:.2f}")

# %% [markdown]
# ## 4.Normalización: Comparando Grupos Diferentes
#
# **Escenario**: La simpatía por el candidato no es la misma en todo el país.
# - En la **Región Capital**, la gente es más afín: media = 60, desvío = 10.
# - En la **Región Interior**, la gente es más escéptica: media = 52, desvío = 13.
#
# Esto crea un problema: un puntaje de "65" en la Capital no significa lo mismo que un "65" en el Interior. ¿Cómo los comparamos de forma justa?
#
# **Solución**: **Normalizamos** los datos. Convertimos todos los puntajes a su respectivo puntaje Z *dentro de su propia región*. Esto nos permite comparar sus posiciones relativas en una escala común.

# %%
# Parámetros y simulación para la Región Capital
n_capital = 4000
media_capital = 60
desvio_capital = 10
simpatia_capital = np.random.normal(media_capital, desvio_capital, n_capital)

# Parámetros y simulación para la Región Interior
n_interior = 6000
media_interior = 52
desvio_interior = 13
simpatia_interior = np.random.normal(media_interior, desvio_interior, n_interior)

# Graficamos las distribuciones originales (sin normalizar)
plt.figure(figsize=(8, 5))
plt.hist(simpatia_capital, bins=30, alpha=0.7, label='Capital', density=True)
plt.hist(simpatia_interior, bins=30, alpha=0.7, label='Interior', density=True)
plt.title("Distribuciones de Simpatía Originales por Región")
plt.xlabel("Puntaje de Simpatía")
plt.ylabel("Densidad")
plt.legend()
plt.show()

# %% [markdown]
# Como se ve en el gráfico, las dos distribuciones están centradas en lugares diferentes y tienen distinta dispersión. Ahora, las normalizamos.

# %%
# Calculamos los puntajes Z para cada región por separado
z_capital = (simpatia_capital - media_capital) / desvio_capital
z_interior = (simpatia_interior - media_interior) / desvio_interior

# Graficamos las distribuciones normalizadas (puntajes Z)
plt.figure(figsize=(8, 5))
plt.hist(z_capital, bins=30, alpha=0.7, label='Capital (Z)', density=True)
plt.hist(z_interior, bins=30, alpha=0.7, label='Interior (Z)', density=True)
plt.title("Distribuciones de Simpatía Normalizadas (Puntaje Z)")
plt.xlabel("Puntaje Z")
plt.ylabel("Densidad")
plt.legend()
plt.show()

# %% [markdown]
# **Observación**: ¡Perfecto! Al convertir todo a puntajes Z, ambas distribuciones ahora se centran en 0 y tienen una desviación estándar de 1. Ahora son directamente comparables.
#
# ### 4.a. Aplicación Práctica: ¿Quién es más simpatizante?
#
# Ahora viene la parte importante. ¿Para qué hicimos esto?
#
# **Caso de estudio**:
# - **Ana**, de la Capital, tiene un puntaje de simpatía de **72**.
# - **Beto**, del Interior, tiene un puntaje de simpatía de **68**.
#
# A simple vista, Ana (72) parece más simpatizante que Beto (68). Pero, ¿es eso cierto *en relación con sus pares*? Calculemos sus puntajes Z.

# %%
# Datos de los individuos
simpatia_ana = 72
simpatia_beto = 68

# Calculamos el puntaje Z de Ana usando los parámetros de la Capital
z_ana = (simpatia_ana - media_capital) / desvio_capital

# Calculamos el puntaje Z de Beto usando los parámetros del Interior
z_beto = (simpatia_beto - media_interior) / desvio_interior

print(f"Puntaje Z de Ana (Capital): {z_ana:.2f}")
print(f"Puntaje Z de Beto (Interior): {z_beto:.2f}")

# Comparamos sus posiciones relativas
if z_beto > z_ana:
    print("\nConclusión: Aunque el puntaje absoluto de Ana es mayor, Beto es relativamente MÁS simpatizante en comparación con la gente de su propia región.")
else:
    print("\nConclusión: Ana es más simpatizante que Beto, tanto en términos absolutos como relativos a su región.")

# %% [markdown]
# **Conclusión Final**: Este ejemplo demuestra el verdadero poder de la normalización. Nos permite hacer comparaciones justas entre datos que provienen de distribuciones diferentes, enfocándonos en la posición relativa de cada individuo dentro de su propio contexto.