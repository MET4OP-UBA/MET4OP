"""
ANÁLISIS DE REGRESIÓN LINEAL SIMPLE Y MÚLTIPLE
Dataset: Indicadores Políticos y Aprobación Gubernamental

Este script demuestra:
1. Regresión Lineal Simple
2. Regresión Lineal Múltiple
3. Selección de variables (eliminando variables irrelevantes)
4. Evaluación de modelos (R², R² ajustado, AIC, BIC, p-valores)
5. Diagnóstico de supuestos de regresión
"""

#%%
# ============================================================================
# 1. LIBRERÍAS Y CONFIGURACIÓN
# ============================================================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Configuración de visualización
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# ============================================================================
# 1. CARGA Y EXPLORACIÓN DE DATOS
# ============================================================================

# Cargar el dataset
df = pd.read_csv('datos_politicos.csv.gz')

print("="*80)
print("EXPLORACIÓN INICIAL DEL DATASET")
print("="*80)
print(f"\nDimensiones: {df.shape[0]} filas x {df.shape[1]} columnas")
print(f"\nColumnas:\n{df.columns.tolist()}")
print(f"\nPrimeras filas:")
print(df.head())
print(f"\nEstadísticas descriptivas:")
print(df.describe())
print(f"\nValores nulos:")
print(df.isnull().sum())

#%%
# ============================================================================
# 2. PREPARACIÓN DE DATOS (sin variables binarias)
# ============================================================================

print("\n" + "="*80)
print("PREPARACIÓN DE DATOS")
print("="*80)

# Seleccionar solo variables numéricas
df_numeric = df.select_dtypes(include=[np.number]).copy()

print(f"\nVariables numéricas incluidas ({len(df_numeric.columns)}):")
print(df_numeric.columns.tolist())

# Variable dependiente (Y)
y = df_numeric['aprobacion_gobierno']

# Variables independientes (todas las demás numéricas excepto Y)
X_vars = [col for col in df_numeric.columns if col != 'aprobacion_gobierno']
X = df_numeric[X_vars]

print(f"\nVariable dependiente: aprobacion_gobierno")
print(f"Variables independientes ({len(X_vars)}): {X_vars}")

#%%
# ============================================================================
# SCATTERPLOTS DE TODAS LAS VARIABLES VS APROBACIÓN GUBERNAMENTAL
# ============================================================================

print("\n" + "="*80)
print("SCATTERPLOTS DE VARIABLES INDEPENDIENTES VS VARIABLE DEPENDIENTE")
print("="*80)

num_vars = X.columns
n_cols = 3
n_rows = int(np.ceil(len(num_vars) / n_cols))

fig, axes = plt.subplots(n_rows, n_cols, figsize=(16, 5 * n_rows))
axes = axes.flatten()

for i, col in enumerate(num_vars):
    axes[i].scatter(X[col], y, alpha=0.6, edgecolors='k', s=40)
    axes[i].set_xlabel(col)
    axes[i].set_ylabel('Aprobación Gubernamental')
    axes[i].set_title(f'{col} vs Aprobación', fontsize=12, fontweight='bold')
    axes[i].grid(True, alpha=0.3)

# Eliminar ejes vacíos
for j in range(i + 1, len(axes)):
    fig.delaxes(axes[j])

plt.tight_layout()
plt.show()

#%%
# ============================================================================
# 3. MATRIZ DE CORRELACIÓN
# ============================================================================

print("\n" + "="*80)
print("ANÁLISIS DE CORRELACIÓN")
print("="*80)

# Calcular correlaciones con la variable dependiente
correlaciones = df_numeric.corr()['aprobacion_gobierno'].drop('aprobacion_gobierno').sort_values(ascending=False)

print("\nCorrelaciones con aprobacion_gobierno:")
print(correlaciones)

# Visualizar matriz de correlación
plt.figure(figsize=(14, 10))
correlation_matrix = df_numeric.corr()
sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0, 
            square=True, linewidths=1, cbar_kws={"shrink": 0.8})
plt.title('Matriz de Correlación - Variables Políticas', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.show()

#%%
# ============================================================================
# 4. REGRESIÓN LINEAL SIMPLE
# ============================================================================

print("\n" + "="*80)
print("REGRESIÓN LINEAL SIMPLE")
print("="*80)

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import statsmodels.api as sm

# Seleccionar la variable con mayor correlación
mejor_var = correlaciones.abs().idxmax()
print(f"\nVariable con mayor correlación: {mejor_var} (r = {correlaciones[mejor_var]:.4f})")

# Modelo de regresión simple
X_simple = df_numeric[[mejor_var]].values
y_values = y.values

modelo_simple = LinearRegression()
modelo_simple.fit(X_simple, y_values)

# Predicciones
y_pred_simple = modelo_simple.predict(X_simple)

# Métricas
r2_simple = r2_score(y_values, y_pred_simple)
rmse_simple = np.sqrt(mean_squared_error(y_values, y_pred_simple))
mae_simple = mean_absolute_error(y_values, y_pred_simple)

print(f"\nEcuación: aprobacion_gobierno = {modelo_simple.intercept_:.4f} + {modelo_simple.coef_[0]:.4f} * {mejor_var}")
print(f"\nMétricas del modelo simple:")
print(f"  R² = {r2_simple:.4f}")
print(f"  RMSE = {rmse_simple:.4f}")
print(f"  MAE = {mae_simple:.4f}")

# Estadísticos adicionales con statsmodels
X_simple_sm = sm.add_constant(X_simple)
modelo_simple_sm = sm.OLS(y_values, X_simple_sm).fit()

print(f"\nResumen del modelo simple:")
print(modelo_simple_sm.summary())

# Visualización
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Dispersión y línea de regresión
axes[0].scatter(X_simple, y_values, alpha=0.6, edgecolors='k', s=50)
axes[0].plot(X_simple, y_pred_simple, color='red', linewidth=2, label='Línea de regresión')
axes[0].set_xlabel(mejor_var)
axes[0].set_ylabel('Aprobación Gobierno (%)')
axes[0].set_title(f'Regresión Simple: R² = {r2_simple:.4f}', fontsize=14, fontweight='bold')
axes[0].legend()

# Residuos
residuos_simple = y_values - y_pred_simple
axes[1].scatter(y_pred_simple, residuos_simple, alpha=0.6, edgecolors='k', s=50)
axes[1].axhline(y=0, color='red', linestyle='--', linewidth=2)
axes[1].set_xlabel('Valores Predichos')
axes[1].set_ylabel('Residuos')
axes[1].set_title('Gráfico de Residuos', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.show()

#%%
# ============================================================================
# 5. REGRESIÓN LINEAL MÚLTIPLE - MODELO COMPLETO
# ============================================================================

print("\n" + "="*80)
print("REGRESIÓN LINEAL MÚLTIPLE - MODELO COMPLETO")
print("="*80)

X_multiple = sm.add_constant(X)
modelo_completo = sm.OLS(y, X_multiple).fit()

print(f"\nModelo con {len(X_vars)} variables independientes")
print(modelo_completo.summary())

# Variables no significativas
vars_no_sig = modelo_completo.pvalues[modelo_completo.pvalues > 0.05].drop('const', errors='ignore')
print(f"\nVariables NO significativas (p > 0.05):")
for var, pval in vars_no_sig.items():
    print(f"  - {var}: p-value = {pval:.4f}")

#%%
# ============================================================================
# 6. REGRESIÓN MÚLTIPLE - MODELO REDUCIDO
# ============================================================================

print("\n" + "="*80)
print("REGRESIÓN MÚLTIPLE - MODELO REDUCIDO")
print("="*80)

vars_significativas = modelo_completo.pvalues[modelo_completo.pvalues <= 0.05].drop('const', errors='ignore').index.tolist()

print(f"\nVariables significativas seleccionadas ({len(vars_significativas)}):")
print(vars_significativas)

X_reducido = X[vars_significativas]
X_reducido_sm = sm.add_constant(X_reducido)
modelo_reducido = sm.OLS(y, X_reducido_sm).fit()

print(modelo_reducido.summary())

#%%
# ============================================================================
# 7. COMPARACIÓN DE MODELOS
# ============================================================================

print("\n" + "="*80)
print("COMPARACIÓN DE MODELOS")
print("="*80)

comparacion = pd.DataFrame({
    'Modelo': ['Simple', 'Múltiple Completo', 'Múltiple Reducido'],
    'N° Variables': [1, len(X_vars), len(vars_significativas)],
    'R²': [r2_simple, modelo_completo.rsquared, modelo_reducido.rsquared],
    'R² Ajustado': [modelo_simple_sm.rsquared_adj, modelo_completo.rsquared_adj, modelo_reducido.rsquared_adj],
    'AIC': [modelo_simple_sm.aic, modelo_completo.aic, modelo_reducido.aic],
    'BIC': [modelo_simple_sm.bic, modelo_completo.bic, modelo_reducido.bic],
    'RMSE': [rmse_simple, np.sqrt(mean_squared_error(y, modelo_completo.fittedvalues)), 
             np.sqrt(mean_squared_error(y, modelo_reducido.fittedvalues))]
})

print("\n", comparacion.to_string(index=False))

#%%
# ============================================================================
# 8. DIAGNÓSTICO DE SUPUESTOS - MODELO REDUCIDO
# ============================================================================

print("\n" + "="*80)
print("DIAGNÓSTICO DE SUPUESTOS - MODELO REDUCIDO")
print("="*80)

y_pred_reducido = modelo_reducido.fittedvalues
residuos_reducido = modelo_reducido.resid
residuos_std = modelo_reducido.resid_pearson

# Normalidad
stat_shapiro, p_shapiro = stats.shapiro(residuos_reducido)
print(f"\nTest Shapiro-Wilk: estadístico = {stat_shapiro:.4f}, p-value = {p_shapiro:.4f}")

# Homocedasticidad
from statsmodels.stats.diagnostic import het_breuschpagan
bp_test = het_breuschpagan(residuos_reducido, X_reducido_sm)
print(f"\nTest Breusch-Pagan: estadístico = {bp_test[0]:.4f}, p-value = {bp_test[1]:.4f}")

# Autocorrelación
from statsmodels.stats.stattools import durbin_watson
dw_stat = durbin_watson(residuos_reducido)
print(f"\nDurbin-Watson = {dw_stat:.4f}")

# Multicolinealidad
from statsmodels.stats.outliers_influence import variance_inflation_factor
vif_data = pd.DataFrame()
vif_data["Variable"] = X_reducido.columns
vif_data["VIF"] = [variance_inflation_factor(X_reducido.values, i) for i in range(X_reducido.shape[1])]
print(vif_data)

# Gráficos de diagnóstico
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

axes[0, 0].scatter(y_pred_reducido, residuos_reducido, alpha=0.6, edgecolors='k')
axes[0, 0].axhline(y=0, color='red', linestyle='--', linewidth=2)
axes[0, 0].set_title('Residuos vs Valores Ajustados')

stats.probplot(residuos_reducido, dist="norm", plot=axes[0, 1])
axes[0, 1].set_title('Q-Q Plot')

axes[1, 0].hist(residuos_reducido, bins=30, edgecolor='black', alpha=0.7)
axes[1, 0].set_title('Histograma de Residuos')

residuos_sqrt = np.sqrt(np.abs(residuos_std))
axes[1, 1].scatter(y_pred_reducido, residuos_sqrt, alpha=0.6, edgecolors='k')
axes[1, 1].set_title('Scale-Location')

plt.tight_layout()
plt.show()


#%%
# ============================================================================
# DEFINIR VARIABLES MANUALMENTE, CORRER EL MODELO Y CALCULAR VIF
# ============================================================================

print("\n" + "="*80)
print("MODELO PERSONALIZADO Y ANÁLISIS DE MULTICOLINEALIDAD (VIF)")
print("="*80)

# 🔧 Definí manualmente las variables que querés incluir
# Ejemplo: variables_personalizadas = ['pib_per_capita', 'educacion_media', 'indice_desigualdad']
variables_personalizadas = ['inversion_educacion',
'libertad_prensa'
    # <-- escribí aquí las variables que querés incluir -->
]

# Validación
if not variables_personalizadas:
    print("⚠ No se definieron variables personalizadas. Por favor, agregá nombres de columnas válidas.")
else:
    print(f"\nVariables seleccionadas ({len(variables_personalizadas)}):")
    print(variables_personalizadas)

    # Construcción del modelo
    X_personalizado = X[variables_personalizadas]
    X_personalizado_sm = sm.add_constant(X_personalizado)
    mi_modelo = sm.OLS(y, X_personalizado_sm).fit()

    # Resultados
    print("\n" + "="*60)
    print("📈 RESUMEN DEL MODELO PERSONALIZADO (mi_modelo)")
    print("="*60)
    print(mi_modelo.summary())

    # Cálculo del VIF
    print("\n" + "="*60)
    print("🔍 CÁLCULO DEL FACTOR DE INFLACIÓN DE VARIANZA (VIF)")
    print("="*60)

    vif_personalizado = pd.DataFrame({
        "Variable": X_personalizado.columns,
        "VIF": [variance_inflation_factor(X_personalizado.values, i) for i in range(X_personalizado.shape[1])]
    }).sort_values('VIF', ascending=False)

    print(vif_personalizado.to_string(index=False))
    print("\nInterpretación: VIF < 5 (bajo), 5–10 (moderado), > 10 (alto)")

    # Métricas del modelo
    print("\n" + "="*60)
    print("📊 MÉTRICAS DEL MODELO PERSONALIZADO")
    print("="*60)
    print(f"R² = {mi_modelo.rsquared:.4f}")
    print(f"R² ajustado = {mi_modelo.rsquared_adj:.4f}")
    print(f"AIC = {mi_modelo.aic:.2f}")
    print(f"BIC = {mi_modelo.bic:.2f}")

#%%
# ============================================================================
# 10. PREDICCIÓN FINAL
# ============================================================================

print("\n" + "="*80)
print("EJEMPLO DE PREDICCIÓN (CORREGIDA)")
print("="*80)

# Tomamos un ejemplo (primera observación)
ejemplo = X_reducido.iloc[0:1].copy()
print("\nEjemplo de entrada:")
print(ejemplo.T)

# Importante: el modelo ya tiene la constante incluida, NO agregamos otra
prediccion = modelo_reducido.predict(exog=sm.add_constant(ejemplo, has_constant='add'))

print(f"\nPredicción de aprobación gubernamental: {prediccion.values[0]:.2f}%")
print(f"Valor real: {y.iloc[0]:.2f}%")
print(f"Error: {abs(prediccion.values[0] - y.iloc[0]):.2f}%")
# %%
