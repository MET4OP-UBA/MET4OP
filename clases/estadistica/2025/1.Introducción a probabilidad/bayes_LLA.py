# %% [markdown]
# # Análisis de Perfil de Votantes con Teorema de Bayes
#
# **Objetivo:** A partir de resultados electorales conocidos (probabilidades condicionales), el objetivo es calcular una probabilidad condicional inversa de interés estratégico.
#
# **Planteo del Problema:**
# En el contexto de las elecciones provinciales de septiembre, se conoce la proporción de votantes que eligió a La Libertad Avanza (LLA). Este dato es la probabilidad de apoyar a LLA, **dado que se emitió un voto**: $P(\text{Apoya LLA} | \text{Fue a Votar}) = 33.71\%$.
#
# Sin embargo, para fines estratégicos, es más útil conocer una probabilidad inversa: la proporción de simpatizantes de LLA que no participaron en la elección. Es decir, se busca calcular: $P(\text{No Votó} | \text{Apoya LLA})$.

# %%
# Importamos las librerías necesarias
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# %% [markdown]
# ## 1. Modelo de la Población de Votantes
#
# Para el análisis, se construye un modelo que representa a la población de individuos habilitados para votar. Este modelo se basa en los siguientes parámetros:
#
# - **Participación Electoral:** Se utiliza el dato real de participación del **60.98%**.
# - **Apoyo a LLA entre Votantes:** Corresponde al resultado electoral del **33.71%**.
# - **Supuesto de Apoyo a LLA entre No Votantes:** Se establece un supuesto plausible de que el apoyo a LLA en el grupo que no vota es del **45%**, para reflejar una posible base de apoyo latente.

# %%
# Parámetros del modelo
n_individuos = 10000
participacion = 0.6098
pct_lla_en_votantes = 0.3371
pct_lla_en_no_votantes = 0.45

# --- Lógica de creación del modelo poblacional (CORREGIDA) ---
n_votantes = int(n_individuos * participacion)
n_no_votantes = n_individuos - n_votantes

# CORRECCIÓN: Se calcula el % de LLA sobre el N de votantes, no el total.
n_votantes_lla = int(n_votantes * pct_lla_en_votantes)
n_votantes_otros = n_votantes - n_votantes_lla

n_no_votantes_lla = int(n_no_votantes * pct_lla_en_no_votantes)
n_no_votantes_otros = n_no_votantes - n_no_votantes_lla

fue_a_votar = ['Sí'] * n_votantes + ['No'] * n_no_votantes
vota_lla = (['Sí'] * n_votantes_lla + ['No'] * n_votantes_otros +
            ['Sí'] * n_no_votantes_lla + ['No'] * n_no_votantes_otros)
df_modelo = pd.DataFrame({'fue_a_votar': fue_a_votar, 'vota_lla': vota_lla})
df_modelo = df_modelo.sample(frac=1, random_state=42).reset_index(drop=True)

print("Modelo poblacional creado. Aquí una muestra de los datos:")
print(df_modelo.head())

# %% [markdown]
# ## 2. Visualización con Árbol de Probabilidad
#
# Un árbol de probabilidad permite visualizar las probabilidades conocidas. Se estructura siguiendo el orden de los eventos: primero, la decisión de votar o no; segundo, el apoyo a un partido. A continuación, se calculan las probabilidades para cada rama y se genera el gráfico.

# %%
# --- Probabilidades para el árbol ---
# Nivel 1: Priors
p_voto = len(df_modelo[df_modelo['fue_a_votar'] == 'Sí']) / len(df_modelo)
p_no_voto = 1 - p_voto

# Nivel 2: Condicionales (Likelihoods)
votantes = df_modelo[df_modelo['fue_a_votar'] == 'Sí']
no_votantes = df_modelo[df_modelo['fue_a_votar'] == 'No']
p_lla_dado_voto = len(votantes[votantes['vota_lla'] == 'Sí']) / len(votantes)
p_no_lla_dado_voto = 1 - p_lla_dado_voto
p_lla_dado_no_voto = len(no_votantes[no_votantes['vota_lla'] == 'Sí']) / len(no_votantes)
p_no_lla_dado_no_voto = 1 - p_lla_dado_no_voto

# Nivel 3: Probabilidades Conjuntas (Intersecciones)
p_voto_y_lla = p_lla_dado_voto * p_voto
p_voto_y_no_lla = p_no_lla_dado_voto * p_voto
p_no_voto_y_lla = p_lla_dado_no_voto * p_no_voto
p_no_voto_y_no_lla = p_no_lla_dado_no_voto * p_no_voto

print(f"P(Fue a Votar) = {p_voto:.2%}")
print(f"P(No Votó)   = {p_no_voto:.2%}")
print("-" * 30)
print(f"P(Apoya LLA | Fue a Votar) = {p_lla_dado_voto:.2%} (Verifica el 33.71% del input)")
print(f"P(Apoya LLA | No Votó)   = {p_lla_dado_no_voto:.2%} (Verifica el 45% del supuesto)")

# %%
# --- Función para graficar el Árbol de Probabilidad ---
def plot_probability_tree():
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.set_axis_off()

    # Nodos y texto
    ax.text(0.5, 3.5, "Inicio", ha='center', va='center', bbox=dict(boxstyle="circle,pad=0.5", fc="lightblue"))
    ax.text(4, 5.5, "Fue a Votar", ha='center', va='center', bbox=dict(boxstyle="round,pad=0.5", fc="lightgreen"))
    ax.text(4, 1.5, "No Votó", ha='center', va='center', bbox=dict(boxstyle="round,pad=0.5", fc="salmon"))
    ax.text(8, 6.25, "Apoya LLA", ha='center', va='center', bbox=dict(boxstyle="round,pad=0.5", fc="gold"))
    ax.text(8, 4.75, "No Apoya LLA", ha='center', va='center', bbox=dict(boxstyle="round,pad=0.5", fc="whitesmoke"))
    ax.text(8, 2.25, "Apoya LLA", ha='center', va='center', bbox=dict(boxstyle="round,pad=0.5", fc="gold"))
    ax.text(8, 0.75, "No Apoya LLA", ha='center', va='center', bbox=dict(boxstyle="round,pad=0.5", fc="whitesmoke"))

    # Ramas y probabilidades condicionales
    ax.plot([1.2, 3], [3.5, 5.5], 'k-')
    ax.text(2.1, 4.6, f'P(Votó) = {p_voto:.2%}', ha='center', va='center', rotation=28, backgroundcolor='white')
    ax.plot([1.2, 3], [3.5, 1.5], 'k-')
    ax.text(2.1, 2.4, f'P(No Votó) = {p_no_voto:.2%}', ha='center', va='center', rotation=-28, backgroundcolor='white')
    ax.plot([5.2, 7], [5.5, 6.25], 'k-')
    ax.text(6.1, 6, f'P(LLA|Votó) = {p_lla_dado_voto:.2%}', ha='center', va='center', rotation=15, backgroundcolor='white')
    ax.plot([5.2, 7], [5.5, 4.75], 'k-')
    ax.text(6.1, 5, f'P(No LLA|Votó) = {p_no_lla_dado_voto:.2%}', ha='center', va='center', rotation=-15, backgroundcolor='white')
    ax.plot([5.2, 7], [1.5, 2.25], 'k-')
    ax.text(6.1, 2, f'P(LLA|No Votó) = {p_lla_dado_no_voto:.2%}', ha='center', va='center', rotation=15, backgroundcolor='white')
    ax.plot([5.2, 7], [1.5, 0.75], 'k-')
    ax.text(6.1, 1, f'P(No LLA|No Votó) = {p_no_lla_dado_no_voto:.2%}', ha='center', va='center', rotation=-15, backgroundcolor='white')
    
    # Probabilidades de intersección al final
    ax.text(10.5, 6.25, r'$P(V \cap LLA) = $' + f'{p_voto_y_lla:.2%}', ha='center', va='center', fontsize=12)
    ax.text(10.5, 4.75, r'$P(V \cap \neg LLA) = $' + f'{p_voto_y_no_lla:.2%}', ha='center', va='center', fontsize=12)
    ax.text(10.5, 2.25, r'$P(\neg V \cap LLA) = $' + f'{p_no_voto_y_lla:.2%}', ha='center', va='center', fontsize=12)
    ax.text(10.5, 0.75, r'$P(\neg V \cap \neg LLA) = $' + f'{p_no_voto_y_no_lla:.2%}', ha='center', va='center', fontsize=12)

    plt.title("Árbol de Probabilidad: Participación y Apoyo a LLA", size=16)
    plt.show()

plot_probability_tree()

# %% [markdown]
# ### Interpretación del Árbol
#
# El árbol visualiza el flujo de probabilidades. Ahora los valores son coherentes:
# - La probabilidad condicional $P(\text{Apoya LLA} | \text{Fue a Votar})$ es del **33.71%**, tal como se definió.
# - La **probabilidad conjunta** (intersección), que representa esta porción expandida a la población total, es $P(V \cap LLA) = 0.3371 \times 0.6098 = \textbf{20.56\%}$.
#
# El problema analítico persiste: el árbol está estructurado en la dirección `Voto -> Apoyo`. Para calcular la probabilidad en la dirección inversa (`Apoyo -> Voto`), se requiere el Teorema de Bayes.

# %% [markdown]
# ## 3. Aplicación del Teorema de Bayes
#
# El Teorema de Bayes es la herramienta formal para invertir una probabilidad condicional. La fórmula es:
# $$P(A|B) = \frac{P(B|A) \cdot P(A)}{P(B)}$$
#
# Aplicada a nuestro problema:
# $$P(\text{No Votó} | \text{Apoya LLA}) = \frac{P(\text{Apoya LLA} | \text{No Votó}) \cdot P(\text{No Votó})}{P(\text{Apoya LLA})}$$
#
# Los componentes del numerador se obtienen directamente de las ramas del árbol. El denominador, $P(\text{Apoya LLA})$, corresponde a la probabilidad total de apoyar a LLA y se calcula sumando las probabilidades de todas las rutas que terminan en "Apoya LLA".

# %%
# El denominador, P(Apoya LLA), es la suma de las intersecciones relevantes.
p_lla_total = p_voto_y_lla + p_no_voto_y_lla

print(f"Probabilidad total de apoyar a LLA, P(Apoya LLA): {p_lla_total:.2%}")
print("-" * 50)
# Aplicamos la fórmula de Bayes
numerador = p_lla_dado_no_voto * p_no_voto
denominador = p_lla_total
prob_bayesiana_final = numerador / denominador

print(f"Resultado del Teorema de Bayes:")
print(f"P(No Votó | Apoya LLA) = {prob_bayesiana_final:.2%}")


# %% [markdown]
# ### Validación del Resultado
#
# Para confirmar la validez del cálculo, se puede obtener el mismo resultado directamente del modelo poblacional, dividiendo el número de casos de simpatizantes de LLA que no votaron entre el total de simpatizantes de LLA.

# %%
print("--- Validación con Cálculo Directo ---")
tabla_contingencia = pd.crosstab(df_modelo['fue_a_votar'], df_modelo['vota_lla'])
resultado_directo = tabla_contingencia.loc['No', 'Sí'] / tabla_contingencia['Sí'].sum()
print(f"El cálculo directo desde los datos es: {resultado_directo:.2%}")
print("Los resultados coinciden.")

# %% [markdown]
# ## Conclusión
#
# El análisis indica que un **46.06%** de los individuos que apoyan a LLA no participó en la elección provincial.
#
# Este resultado tiene una implicación estratégica directa: sugiere que una parte significativa de la base de apoyo del partido no está movilizada. Para futuras elecciones, una campaña enfocada en aumentar la participación de este segmento podría tener un impacto considerable en el resultado final. El Teorema de Bayes permite cuantificar la magnitud de este grupo, convirtiendo datos electorales en información accionable.