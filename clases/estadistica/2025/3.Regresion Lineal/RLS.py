#%%
import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.stats.outliers_influence import variance_inflation_factor
from mlxtend.feature_selection import SequentialFeatureSelector as SFS
from sklearn.base import BaseEstimator, RegressorMixin


real_estate = pd.read_csv('../data/Real_estate.csv')
#%%
print(real_estate.head(2))
real_estate.info()
real_estate.describe()
real_estate.isnull().sum()

#%%
# Usamos tus variables seleccionadas
x_var = 'X2 house age' # O 'X4 number of convenience stores', 'X3 distance to the nearest MRT station'
y_var = 'Y house price of unit area'

# Paso 1: Gráfico de dispersión
plt.figure(figsize=(8, 6))
sns.scatterplot(x=real_estate[x_var], y=real_estate[y_var], s=50, color='blue')

# Etiquetas y título del gráfico
plt.title(f'Relación entre {x_var} y {y_var}', fontsize=14)
plt.xlabel(x_var, fontsize=12)
plt.ylabel(y_var, fontsize=12)
# %%
#%%
# CORRELACIÓN DE PEARSON ENTRE CADA VARIABLE PREDICTORA Y Y

# Seleccionamos solo las columnas numéricas
numeric_cols = real_estate.select_dtypes(include=[np.number])

# Calculamos la matriz de correlación
correlation_matrix = numeric_cols.corr(method='pearson')

# Imprimimos la correlación de cada variable con Y
print("Coeficiente de correlación de Pearson con 'Y house price of unit area':")
print(correlation_matrix['Y house price of unit area'].sort_values(ascending=False))

#%%
# HEATMAP DE CORRELACIÓN ENTRE TODAS LAS VARIABLES

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
plt.title('Mapa de calor de correlaciones', fontsize=14)
plt.show()

#%%
# REGRESIÓN LINEAL SIMPLE PARA CADA VARIABLE PREDICTORA

# Definimos la variable dependiente
y = real_estate['Y house price of unit area']

# Identificamos las variables predictoras (todas menos No e Y)
predictors = [col for col in real_estate.columns if col not in ['No', 'Y house price of unit area','X1 transaction date']]

# Recorremos cada variable predictora y realizamos una regresión lineal simple
for var in predictors:
    print(f'\n=========================================')
    print(f'Regresión lineal simple: {var} -> Y house price of unit area')
    print(f'=========================================')
    
    X = sm.add_constant(real_estate[var])  # Agregamos constante (intercepto)
    model = sm.OLS(y, X).fit()             # Ajustamos modelo de mínimos cuadrados
    print(model.summary())                 # Mostramos tabla de resultados

    # Gráfico de dispersión con línea de regresión
    plt.figure(figsize=(8, 6))
    sns.regplot(x=real_estate[var], y=y, ci=None, line_kws={"color": "red"})
    plt.title(f'Regresión lineal simple: {var} vs Y', fontsize=14)
    plt.xlabel(var)
    plt.ylabel('Y house price of unit area')
    plt.show()
# %% REGRESION LINEAL MULTIPLE
#%%
# EXPLICACIÓN TEÓRICA: AIC y BIC
#%%
#%%
# EXPLICACIÓN TEÓRICA: AIC y BIC

print("""
===========================================
🧠 CRITERIOS DE SELECCIÓN DE MODELOS: AIC y BIC
===========================================

📘 AIC (Akaike Information Criterion):
 - Evalúa el equilibrio entre el ajuste y la complejidad del modelo.
 - Penaliza los modelos con muchas variables.
 - Cuanto más bajo sea el AIC, mejor el modelo.

📗 BIC (Bayesian Information Criterion):
 - Similar al AIC, pero penaliza aún más la complejidad.
 - Prefiere modelos más simples.
 - Cuanto más bajo sea el BIC, mejor.

👉 Ambos se usan para decidir cuántas variables incluir en una regresión
sin sobreajustar el modelo.
""")

#%%
# PREPARACIÓN DE VARIABLES
y = real_estate['Y house price of unit area']
predictors = [col for col in real_estate.columns if col not in ['No', 'Y house price of unit area', 'X1 transaction date']]
X = real_estate[predictors]

#%%
# VERIFICACIÓN DE MULTICOLINEALIDAD (VIF)
X_const = sm.add_constant(X)
vif_data = pd.DataFrame({
    "Variable": X_const.columns,
    "VIF": [variance_inflation_factor(X_const.values, i) for i in range(X_const.shape[1])]
})
print("\n==========================================")
print("🔍 FACTOR DE INFLACIÓN DE LA VARIANZA (VIF)")
print("==========================================")
print(vif_data)

#%%
#%%
# 📊 MODELO COMPLETO
X_full = sm.add_constant(X)
model_full = sm.OLS(y, X_full).fit()
print(model_full.summary())
print(f"AIC completo: {model_full.aic:.2f}")

#%%
# 🔄 SELECCIÓN HACIA ADELANTE (FORWARD AIC)
def forward_aic(X, y):
    remaining = list(X.columns)
    selected = []
    current_score, best_new_score = np.inf, np.inf
    step = 1

    while remaining:
        scores_with_candidates = []
        for candidate in remaining:
            formula = selected + [candidate]
            X_model = sm.add_constant(X[formula])
            model = sm.OLS(y, X_model).fit()
            scores_with_candidates.append((model.aic, candidate))
        scores_with_candidates.sort(reverse=False)
        best_new_score, best_candidate = scores_with_candidates[0]

        print(f"Paso {step}: mejor variable = {best_candidate} | AIC = {best_new_score:.2f}")
        step += 1

        if best_new_score < current_score:
            remaining.remove(best_candidate)
            selected.append(best_candidate)
            current_score = best_new_score
        else:
            break
    print(f"\n✅ Variables seleccionadas (Forward): {selected}")
    return selected

forward_vars = forward_aic(X, y)

#%%
# 🔁 SELECCIÓN HACIA ATRÁS (BACKWARD AIC)
def backward_aic(X, y):
    included = list(X.columns)
    step = 1
    while True:
        X_model = sm.add_constant(X[included])
        model = sm.OLS(y, X_model).fit()
        aic_base = model.aic
        pvalues = model.pvalues.iloc[1:]
        worst_p = pvalues.max()
        worst_var = pvalues.idxmax()

        print(f"Paso {step}: AIC = {aic_base:.2f}")
        step += 1

        # Intentamos eliminar cada variable y ver si mejora el AIC
        aic_candidates = []
        for candidate in included:
            vars_try = [v for v in included if v != candidate]
            model_try = sm.OLS(y, sm.add_constant(X[vars_try])).fit()
            aic_candidates.append((model_try.aic, candidate))

        aic_candidates.sort()
        best_aic, best_removed = aic_candidates[0]

        if best_aic < aic_base:
            print(f"Eliminando {best_removed}, nuevo AIC = {best_aic:.2f}")
            included.remove(best_removed)
        else:
            break

    print(f"\n✅ Variables seleccionadas (Backward): {included}")
    return included

backward_vars = backward_aic(X, y)

#%%
# ⚖️ SELECCIÓN PASO A PASO (STEPWISE AIC)
def stepwise_aic(X, y):
    included = []
    step = 1
    while True:
        changed = False

        # Forward step
        excluded = list(set(X.columns) - set(included))
        new_aic = pd.Series(index=excluded, dtype=float)
        for new_var in excluded:
            model = sm.OLS(y, sm.add_constant(X[included + [new_var]])).fit()
            new_aic[new_var] = model.aic
        best_p = new_aic.min()
        best_var = new_aic.idxmin()
        if len(new_aic) and best_p < sm.OLS(y, sm.add_constant(X[included])).fit().aic:
            included.append(best_var)
            changed = True
            print(f"Paso {step} - Se agrega {best_var}, AIC = {best_p:.2f}")
            step += 1

        # Backward step
        model = sm.OLS(y, sm.add_constant(X[included])).fit()
        aic_before = model.aic
        worst_p = model.pvalues.iloc[1:].max()
        worst_var = model.pvalues.iloc[1:].idxmax()
        if worst_p > 0.05:
            model_drop = sm.OLS(y, sm.add_constant(X[[v for v in included if v != worst_var]])).fit()
            if model_drop.aic < aic_before:
                included.remove(worst_var)
                changed = True
                print(f"Paso {step} - Se elimina {worst_var}, AIC = {model_drop.aic:.2f}")
                step += 1

        if not changed:
            break

    print(f"\n✅ Variables seleccionadas (Stepwise): {included}")
    return included

stepwise_vars = stepwise_aic(X, y)

#%%
# 📊 COMPARACIÓN FINAL DE MODELOS
models = {
    'Completo': model_full,
    'Forward': sm.OLS(y, sm.add_constant(X[forward_vars])).fit(),
    'Backward': sm.OLS(y, sm.add_constant(X[backward_vars])).fit(),
    'Stepwise': sm.OLS(y, sm.add_constant(X[stepwise_vars])).fit(),
}

comparison = pd.DataFrame({
    'Modelo': list(models.keys()),
    'AIC': [m.aic for m in models.values()],
    'BIC': [m.bic for m in models.values()],
    'R2_ajustado': [m.rsquared_adj for m in models.values()]
})

print("\n📊 COMPARACIÓN FINAL ENTRE MODELOS (criterio AIC)")
print(comparison.sort_values('AIC'))

plt.figure(figsize=(8,5))
sns.barplot(data=comparison.melt(id_vars='Modelo', value_vars=['AIC','BIC','R2_ajustado']), 
            x='Modelo', y='value', hue='variable')
plt.title('Comparación de criterios AIC, BIC y R² ajustado entre modelos')
plt.show()