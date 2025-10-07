#%% [markdown]
# # Clase de Test de Hipótesis en Python
# 

#%% [markdown]
# ## 0. Configuración Inicial
# 
# Primero, importamos las librerías necesarias y configuramos algunas opciones globales para que nuestros resultados sean más legibles.

#%%
# Imports y configuración global
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.proportion import proportions_ztest
from statsmodels.stats.oneway import anova_oneway

# --- Configuración global ---
plt.rcParams["figure.figsize"] = (8, 6)
plt.rcParams["axes.grid"] = True
sns.set_theme(style="whitegrid")
pd.set_option("display.float_format", "{:.6f}".format)
np.random.seed(42)

# --- Rutas de los archivos ---
PATH_EJ = "../data/ejercicio.xlsx"
PATH_SHOOT = "../data/fatal-police-shootings-data.csv"

# --- Opciones didácticas ---
# Opción para trabajar con una MUESTRA en el dataset 'shootings' para los TESTS
USE_SAMPLE_FOR_TESTS = True
TEST_SAMPLE_N = 1000  # Tamaño de la muestra

#%% [markdown]
# ## 1. Carga y Preparación de Datos
# 
# Cargamos los dos datasets y realizamos una limpieza básica para asegurar la calidad de los datos antes de los análisis.

#%%
# Carga y preparación de datos
try:
    EJ = pd.read_excel(PATH_EJ)
    shoot = pd.read_csv(PATH_SHOOT)
    print("✅ Datasets cargados correctamente.")
    print(f"EJ shape: {EJ.shape}")
    print(f"shoot shape: {shoot.shape}")
except FileNotFoundError as e:
    print(f"❌ Error al cargar los archivos: {e}")
    print("Asegúrate de que las rutas son correctas y los archivos existen.")
    # Creamos DataFrames vacíos para que el script no se detenga por completo
    EJ = pd.DataFrame()
    shoot = pd.DataFrame()

# --- Limpieza y tipado (Dataset EJERCICIO) ---
if not EJ.empty:
    for col in ["Edad", "TAs", "TAd"]:
        if col in EJ.columns:
            EJ[col] = pd.to_numeric(EJ[col], errors="coerce")

    for col in ["Sexo", "ACV", "ACVTIPO"]:
        if col in EJ.columns:
            EJ[col] = EJ[col].astype("category")

    # Eliminamos filas donde las variables numéricas clave son nulas
    EJ.dropna(subset=["Edad", "TAs", "TAd"], inplace=True)
    print("\nLimpieza de 'EJERCICIO' completada.")

# --- Limpieza y tipado (Dataset SHOOTINGS) ---
if not shoot.empty:
    shoot["age"] = pd.to_numeric(shoot["age"], errors="coerce")
    shoot.dropna(subset=["age"], inplace=True)
    shoot = shoot[(shoot["age"] > 0) & (shoot["age"] <= 120)].copy()

    for col in ["race", "manner_of_death"]:
        if col in shoot.columns:
            shoot[col] = shoot[col].astype("category")
    print("Limpieza de 'SHOOTINGS' completada.")

#%% [markdown]
# ## Parte A: Pruebas Paramétricas (`ejercicio.xlsx`)
# Las pruebas paramétricas asumen que los datos siguen una distribución específica (normalmente, la normal). Primero verificaremos este supuesto.

#%% [markdown]
# ### A.1. Verificación de Normalidad
# Usaremos el **gráfico Q-Q** y el **test de Shapiro-Wilk** para evaluar la normalidad.
# -   **H0 (Shapiro-Wilk):** La muestra proviene de una distribución normal.
# -   Si `p < 0.05`, rechazamos H0 y concluimos que los datos no son normales.

#%%
# Verificación de Normalidad para TAs
variable_a_testear = "TAs"

if variable_a_testear in EJ.columns:
    print(f"--- Verificando normalidad para '{variable_a_testear}' ---")
    x = EJ[variable_a_testear].dropna()

    # Gráfico Q-Q
    plt.figure()
    stats.probplot(x, dist="norm", plot=plt)
    plt.title(f"Gráfico Q-Q de Normalidad para '{variable_a_testear}'")
    plt.show()

    # Test de Shapiro-Wilk
    # Esta prueba es adecuada para muestras de hasta 5000 observaciones.
    W, p_valor = stats.shapiro(x)
    print(f"Test de Shapiro-Wilk: W={W:.4f}, p-valor={p_valor:.6f}")
    if p_valor < 0.05:
        print("Resultado: Los datos NO parecen seguir una distribución normal.")
    else:
        print("Resultado: No se puede rechazar la normalidad de los datos.")
else:
    print(f"⚠️ Columna '{variable_a_testear}' no encontrada en el DataFrame 'EJ'.")

#%% [markdown]
# ### A.2. Prueba t para una Muestra
# Compara la media de una muestra con un valor hipotético.
# -   **Ejemplo:** ¿La Tensión Arterial Sistólica (TAs) media es diferente de 120 mmHg?
# -   **H0:** $μ_{TAs} = 120$
# -   **H1:** $μ_{TAs} \neq 120$

#%%
# Prueba t para una Muestra (TAs vs 120)
variable_dependiente = "TAs"
valor_hipotetico = 120.0

if variable_dependiente in EJ.columns:
    datos = EJ[variable_dependiente].dropna()
    print(f"\n--- Prueba t para una muestra: {variable_dependiente} vs {valor_hipotetico} ---")
    print(f"Descriptivos: n={len(datos)}, media={datos.mean():.4f}, std={datos.std():.4f}")
    
    print(f"H0: La media de '{variable_dependiente}' es IGUAL a {valor_hipotetico}.")
    print(f"H1: La media de '{variable_dependiente}' es DIFERENTE a {valor_hipotetico}.")

    # El parámetro 'alternative' puede ser:
    # 'two-sided': para H1 de diferencia (≠)
    # 'less': para H1 de "menor que" (<)
    # 'greater': para H1 de "mayor que" (>)
    t_stat, p_valor = stats.ttest_1samp(datos, popmean=valor_hipotetico, alternative="less")

    print(f"\nResultados: t-statistic={t_stat:.4f}, p-valor={p_valor:.6f}")
    if p_valor < 0.05:
        print("Conclusión: Se rechaza H0. La media es significativamente diferente del valor hipotético.")
    else:
        print("Conclusión: No se rechaza H0. No hay evidencia de una diferencia significativa.")
else:
    print(f"⚠️ Columna '{variable_dependiente}' no encontrada. Se omite el test.")

#%% [markdown]
# ### A.3. Prueba t para Muestras Independientes (Welch)
# Compara las medias de dos grupos independientes. Usamos el test de Welch por defecto, ya que es más robusto si las varianzas no son iguales.
# -   **Ejemplo:** ¿La TAs es diferente entre hombres y mujeres?
# -   **H0:** $μ_{hombres} = μ_{mujeres}$
# -   **H1:** $μ_{hombres} \neq μ_{mujeres}$

#%%
# Prueba t para Muestras Independientes (TAs por Sexo)
variable_dependiente = "TAs"
variable_independiente = "Sexo"

if {variable_dependiente, variable_independiente}.issubset(EJ.columns):
    grupo_1 = EJ[EJ[variable_independiente] == 'M'][variable_dependiente].dropna()
    grupo_2 = EJ[EJ[variable_independiente] == 'F'][variable_dependiente].dropna()

    if not grupo_1.empty and not grupo_2.empty:
        print(f"\n--- Prueba t para muestras independientes: {variable_dependiente} por {variable_independiente} ---")
        print(f"Descriptivos 'M': n={len(grupo_1)}, media={grupo_1.mean():.4f}")
        print(f"Descriptivos 'F': n={len(grupo_2)}, media={grupo_2.mean():.4f}")

        print("H0: Las medias de los dos grupos son IGUALES.")
        print("H1: Las medias de los dos grupos son DIFERENTES.")
        
        # El parámetro 'alternative' puede ser 'two-sided', 'less', 'greater'
        t_stat, p_valor = stats.ttest_ind(grupo_1, grupo_2, equal_var=False, alternative="greater")
        
        print(f"\nResultados (Welch's t-test): t-statistic={t_stat:.4f}, p-valor={p_valor:.6f}")
        if p_valor < 0.05:
            print("Conclusión: Se rechaza H0. Existe una diferencia significativa entre los grupos.")
        else:
            print("Conclusión: No se rechaza H0. No hay evidencia de una diferencia significativa.")
    else:
        print("⚠️ No hay datos suficientes en uno o ambos grupos para realizar el test.")
else:
    print(f"⚠️ Columnas '{variable_dependiente}' o '{variable_independiente}' no encontradas. Se omite el test.")

#%% [markdown]
# ## Parte B: Pruebas No Paramétricas (`shootings`)
# Se usan cuando no se cumple el supuesto de normalidad. 

#%%
# Muestreo del dataset 'shootings'
if not shoot.empty:
    if USE_SAMPLE_FOR_TESTS and len(shoot) > TEST_SAMPLE_N:
        shoot_test = shoot.sample(TEST_SAMPLE_N, random_state=42).copy()
        print(f"Se ha tomado una muestra de {TEST_SAMPLE_N} registros de 'shootings' para los tests.")
    else:
        shoot_test = shoot.copy()
        print("Se utilizará el dataset 'shootings' completo para los tests.")
else:
    shoot_test = pd.DataFrame()
    print("⚠️ El DataFrame 'shoot' está vacío.")

#%% [markdown]
# ### B.1. Verificación de Normalidad (sobre la muestra)
# 
# Es una buena práctica verificar la normalidad sobre la muestra con la que realmente trabajaremos para justificar el uso de tests no paramétricos.

#%%
# Verificación de Normalidad para 'age' en la muestra 'shoot_test'
variable_a_testear = "age"

if not shoot_test.empty and variable_a_testear in shoot_test.columns:
    print(f"--- Verificando normalidad para '{variable_a_testear}' en la MUESTRA ---")
    x = shoot_test[variable_a_testear].dropna()

    plt.figure()
    stats.probplot(x, dist="norm", plot=plt)
    plt.title(f"Gráfico Q-Q de Normalidad para '{variable_a_testear}' (Muestra)")
    plt.show()

    W, p_valor = stats.shapiro(x)
    print(f"Test de Shapiro-Wilk: W={W:.4f}, p-valor={p_valor:.6f}")
    if p_valor < 0.05:
        print("Resultado: Los datos de la muestra NO siguen una distribución normal. Se usarán tests no paramétricos.")
    else:
        print("Resultado: No se puede rechazar la normalidad en la muestra.")
else:
    print(f"⚠️ Columna '{variable_a_testear}' no encontrada o DataFrame 'shoot_test' vacío.")

#%% [markdown]
# ### B.2. Prueba de Wilcoxon para una Muestra
# 
# Es el análogo no paramétrico de la prueba t para una muestra. Compara la **mediana** de los datos con un valor hipotético.
# - **Ejemplo**: ¿La mediana de edad (`age`) en los tiroteos es diferente de 35 años?
# - **H0**: Mediana de la edad = 35
# - **H1**: Mediana de la edad ≠ 35

#%%
# Prueba de Wilcoxon para una muestra (age vs 35)
variable_dependiente = "age"
mediana_hipotetica = 35.0

if not shoot_test.empty and variable_dependiente in shoot_test.columns:
    datos = shoot_test[variable_dependiente].dropna()
    print(f"\n--- Prueba de Wilcoxon para una muestra: {variable_dependiente} vs {mediana_hipotetica} ---")
    print(f"Descriptivos: n={len(datos)}, mediana={datos.median():.2f}")

    print(f"H0: La mediana de '{variable_dependiente}' es IGUAL a {mediana_hipotetica}.")
    print(f"H1: La mediana de '{variable_dependiente}' es DIFERENTE a {mediana_hipotetica}.")

    # El parámetro 'alternative' puede ser 'two-sided', 'less', 'greater'
    stat, p_valor = stats.wilcoxon(datos - mediana_hipotetica, alternative="two-sided")

    print(f"\nResultados: W-statistic={stat:.4f}, p-valor={p_valor:.6f}")
    if p_valor < 0.05:
        print("Conclusión: Se rechaza H0. La mediana es significativamente diferente del valor hipotético.")
    else:
        print("Conclusión: No se rechaza H0. No hay evidencia de una diferencia significativa.")
else:
    print(f"⚠️ Columna '{variable_dependiente}' no encontrada o DataFrame 'shoot_test' vacío.")
    
#%% [markdown]
# ### B.3. Prueba U de Mann-Whitney (2 Muestras)
# Alternativa no paramétrica a la prueba t para muestras independientes. Compara si las distribuciones de dos grupos son diferentes.
# -   **Ejemplo:** ¿La distribución de la edad (`age`) es diferente entre víctimas de raza blanca ('W') y negra ('B')?
# -   **H0:** Las distribuciones de edad son iguales en ambos grupos.
# -   **H1:** Las distribuciones de edad son diferentes.

#%%
# Prueba U de Mann-Whitney (age por race)
variable_dependiente = "age"
variable_independiente = "race"

if not shoot_test.empty and {variable_dependiente, variable_independiente}.issubset(shoot_test.columns):
    grupo_1 = shoot_test[shoot_test[variable_independiente] == 'W'][variable_dependiente].dropna()
    grupo_2 = shoot_test[shoot_test[variable_independiente] == 'B'][variable_dependiente].dropna()

    if not grupo_1.empty and not grupo_2.empty:
        print(f"\n--- Prueba U de Mann-Whitney: {variable_dependiente} por {variable_independiente} ---")
        print(f"Descriptivos 'W': n={len(grupo_1)}, mediana={grupo_1.median():.2f}")
        print(f"Descriptivos 'B': n={len(grupo_2)}, mediana={grupo_2.median():.2f}")
        
        print("H0: Las distribuciones de los grupos son IGUALES.")
        print("H1: Las distribuciones de los grupos son DIFERENTES.")

        # El parámetro 'alternative' puede ser 'two-sided', 'less', 'greater'
        stat, p_valor = stats.mannwhitneyu(grupo_1, grupo_2, alternative="two-sided")
        
        print(f"\nResultados: U-statistic={stat:.4f}, p-valor={p_valor:.6f}")
        if p_valor < 0.05:
            print("Conclusión: Se rechaza H0. Existe una diferencia significativa entre las distribuciones de los grupos.")
        else:
            print("Conclusión: No se rechaza H0. No hay evidencia de una diferencia significativa.")
    else:
        print("⚠️ No hay datos suficientes en uno o ambos grupos ('W', 'B') para realizar el test.")
else:
    print(f"⚠️ Columnas requeridas no encontradas o DataFrame 'shoot_test' vacío. Se omite el test.")

#%% [markdown]
# ### B.4. Prueba de Chi-Cuadrado (χ²) de Independencia
# Evalúa si existe una asociación entre dos variables categóricas.
# -   **Ejemplo:** ¿Existe una asociación entre la raza (`race`) y la forma de muerte (`manner_of_death`)?
# -   **H0:** Las variables son independientes (no hay asociación).
# -   **H1:** Las variables son dependientes (hay asociación).

#%%
# Prueba de Chi-Cuadrado (race vs manner_of_death)
variable_cat_1 = "race"
variable_cat_2 = "manner_of_death"

if not shoot_test.empty and {variable_cat_1, variable_cat_2}.issubset(shoot_test.columns):
    
    razas_comunes = ['W', 'B', 'H']
    muertes_comunes = ['shot', 'shot and Tasered']
    df_chi = shoot_test[
        shoot_test[variable_cat_1].isin(razas_comunes) &
        shoot_test[variable_cat_2].isin(muertes_comunes)
    ]

    if not df_chi.empty:
        tabla_contingencia = pd.crosstab(df_chi[variable_cat_1], df_chi[variable_cat_2])
        
        if tabla_contingencia.shape[0] > 1 and tabla_contingencia.shape[1] > 1:
            print(f"\n--- Prueba Chi-Cuadrado: {variable_cat_1} vs {variable_cat_2} ---")
            print("Tabla de Contingencia (Frecuencias Observadas):")
            print(tabla_contingencia)
            
            print("\nH0: Las variables son INDEPENDIENTES (no hay asociación).")
            print("H1: Las variables son DEPENDIENTES (hay asociación).")

            chi2_stat, p_valor, dof, expected = stats.chi2_contingency(tabla_contingencia)

            print(f"\nResultados: Chi-cuadrado={chi2_stat:.4f}, p-valor={p_valor:.6f}, gl={dof}")
            if p_valor < 0.05:
                print("Conclusión: Se rechaza H0. Existe una asociación estadísticamente significativa entre las variables.")
            else:
                print("Conclusión: No se rechaza H0. No hay evidencia de una asociación.")
        else:
            print("⚠️ La tabla de contingencia no tiene suficientes dimensiones (filas/columnas) para el test.")
    else:
        print("⚠️ No hay datos suficientes después de filtrar por categorías comunes.")
else:
    print(f"⚠️ Columnas requeridas no encontradas o DataFrame 'shoot_test' vacío. Se omite el test.")
    
#%% [markdown]
# ## Parte C: Pruebas para Muestras Apareadas (Datos Ficticios)
# 
# Estas pruebas se usan cuando las mediciones se toman dos veces sobre el mismo sujeto, por ejemplo, "antes" y "después" de una intervención. Los datos están "apareados" o "relacionados".
# 
# Crearemos un set de datos ficticio que simula el nivel de estrés de 30 personas antes y después de un taller de meditación.

#%%
# Creación de datos ficticios para muestras apareadas
np.random.seed(42)
datos_apareados = {
    'id_sujeto': range(1, 31),
    'estres_antes': np.random.normal(loc=75, scale=10, size=30).round(1)
}
df_apareados = pd.DataFrame(datos_apareados)

# Aseguramos que 'estres_despues' sea en general menor que 'estres_antes'
df_apareados['estres_despues'] = df_apareados['estres_antes'] - np.random.normal(loc=10, scale=5, size=30)
df_apareados['estres_despues'] = df_apareados['estres_despues'].round(1).clip(0, 100)

print("--- Datos Ficticios para Muestras Apareadas ---")
print(df_apareados.head())
print("\nDescriptivos:")
print(df_apareados[['estres_antes', 'estres_despues']].describe())

#%% [markdown]
# ### C.1. Prueba t para Muestras Apareadas (Paramétrica)
# 
# Compara las medias de dos mediciones relacionadas. Asume que las **diferencias** entre los pares siguen una distribución normal.
# - **Ejemplo**: ¿El nivel de estrés medio disminuyó significativamente después del taller?
# - **H0**: La media de las diferencias entre "antes" y "después" es cero ($μ_{diferencia} = 0$).
# - **H1**: La media de las diferencias no es cero ($μ_{diferencia} \neq 0$).

#%%
# Prueba t para muestras apareadas
antes = df_apareados['estres_antes']
despues = df_apareados['estres_despues']

print("\n--- Prueba t para Muestras Apareadas ---")
print("H0: La media del estrés ANTES es igual a la media del estrés DESPUÉS.")
print("H1: Las medias son diferentes.")

# El parámetro 'alternative' puede ser 'two-sided', 'less', 'greater'
# 'greater' aquí significaría: H1: media(antes) > media(despues)
t_stat, p_valor = stats.ttest_rel(antes, despues, alternative="two-sided")

print(f"\nResultados: t-statistic={t_stat:.4f}, p-valor={p_valor:.6f}")
if p_valor < 0.05:
    print("Conclusión: Se rechaza H0. Hay una diferencia estadísticamente significativa en el nivel de estrés.")
else:
    print("Conclusión: No se rechaza H0. No hay evidencia de una diferencia significativa.")

#%% [markdown]
# ### C.2. Prueba de Wilcoxon para Muestras Apareadas (No Paramétrica)
# 
# Es la alternativa no paramétrica. No asume normalidad en las diferencias, sino que trabaja con los rangos de estas diferencias.
# - **Ejemplo**: ¿Hubo un cambio significativo en el nivel de estrés (mediana) después del taller?
# - **H0**: La mediana de las diferencias entre "antes" y "después" es cero.
# - **H1**: La mediana de las diferencias no es cero.

#%%
# Prueba de Wilcoxon para muestras apareadas
antes = df_apareados['estres_antes']
despues = df_apareados['estres_despues']

print("\n--- Prueba de Wilcoxon para Muestras Apareadas ---")
print("H0: La mediana de las diferencias entre ANTES y DESPUÉS es cero.")
print("H1: La mediana de las diferencias es diferente de cero.")

# El parámetro 'alternative' puede ser 'two-sided', 'less', 'greater'
stat, p_valor = stats.wilcoxon(antes, despues, alternative="two-sided")

print(f"\nResultados: W-statistic={stat:.4f}, p-valor={p_valor:.6f}")
if p_valor < 0.05:
    print("Conclusión: Se rechaza H0. Hay un cambio estadísticamente significativo en el nivel de estrés.")
else:
    print("Conclusión: No se rechaza H0. No hay evidencia de un cambio significativo.")
# %%
