# %% [markdown]
# # EJERCICIO 4 — Probabilidades condicionales paso a paso (con tablas y totales)
# **Ballotage 2023** · Voto a **Milei** vs **Massa**

# Se usan **tablas de contingencia con totales** (pandas) y fórmulas explícitas.


plt.rcParams["figure.figsize"] = (8, 4.8)
plt.rcParams["axes.grid"] = True

# ---------------- Escenario fijo (mismos datos en todos los pasos) ----------------
spec = {
    ("Urbana","Hombre"): {"n":  90, "p_milei": 0.49},
    ("Urbana","Mujer") : {"n": 810, "p_milei": 0.46},
    ("Rural", "Hombre"): {"n":  40, "p_milei": 0.80},
    ("Rural", "Mujer") : {"n":  60, "p_milei": 0.40},
}
ZONAS   = ["Urbana","Rural"]
GENEROS = ["Hombre","Mujer"]
VOTOS   = ["Milei","Massa"]

# Expandimos a un DataFrame de registros (n ≈ 1000)
rows = []
for (zona, genero), pars in spec.items():
    n = int(pars["n"])
    m = int(round(n*pars["p_milei"]))  # Milei
    a = n - m                          # Massa
    rows += [{"Zona": zona, "Género": genero, "Voto": "Milei"}]*m
    rows += [{"Zona": zona, "Género": genero, "Voto": "Massa"}]*a
df = pd.DataFrame(rows)
n_total = len(df)

# %% [markdown]
# ## Paso 1 — **Solo ZONA** → `P(Voto \| Zona)`
# Fórmula por zona \(z\):  
# \[
# P(\text{Milei}\mid z)=\frac{\text{cuentas de Milei en }z}{\text{total de casos en }z}
# \]

# %%
# Conteos por Zona x Voto (con totales)
ct_z = pd.crosstab(df["Zona"], df["Voto"], margins=True, margins_name="Total")
ct_z

# %%
# Probabilidades condicionales por fila: P(Voto | Zona) (con totales)
p_z = pd.crosstab(df["Zona"], df["Voto"], normalize="index", margins=True, margins_name="Total")
p_z.style.format("{:.2%}")

# %%
# Agregado ponderado por tamaño de zona (pesos = participación de cada zona en la muestra)
w_z = df["Zona"].value_counts(normalize=True).rename("Peso zona")
p_milei_z = p_z["Milei"].drop("Total")
p_agg_z = float((p_milei_z * w_z).sum())

tabla_z = pd.DataFrame({
    "P(Milei | Zona)": p_milei_z.map("{:.2%}".format),
    "Peso zona": w_z.map("{:.2%}".format),
})
tabla_z["Aporte"] = (p_milei_z * w_z).map("{:.2%}".format)

fila_agregado = pd.DataFrame([{
    "P(Milei | Zona)": "—",
    "Peso zona": "—",
    "Aporte": f"{p_agg_z:.2%}"
}], index=["Agregado"])

pd.concat([tabla_z, fila_agregado])

print(f"Agregado por zona: P(Milei) = {p_agg_z:.2%}  → {'Gana Milei' if p_agg_z>0.5 else 'Gana Massa'}")

# %%
# Gráfico P(Voto|Zona)
x = np.arange(len(ZONAS))
pM = [p_milei_z[z] for z in ZONAS]
pA = [1-p for p in pM]
plt.bar(x, pM, label="Milei", color="#4e79a7")
plt.bar(x, pA, bottom=pM, label="Massa", color="#f28e2b")
plt.xticks(x, ZONAS)
plt.yticks(np.linspace(0,1,6), [f"{int(t*100)}%" for t in np.linspace(0,1,6)])
plt.ylim(0,1.02)
plt.title("P(Voto | Zona)")
plt.legend(); plt.show()

# %% [markdown]
# **Lectura:** mirando solo **Zona**, el gran peso de **Urbana** (con menor \(P(\text{Milei}|z)\)) inclina el agregado hacia **Massa**.

# %% [markdown]
# ## Paso 2 — Agregamos **GÉNERO** y calculamos `P(Voto \| Género)` y `P(Voto \| Zona, Género)`
# Fórmulas:  
# \[
# P(\text{Milei}\mid g)=\frac{\sum_z \text{Milei}_{z,g}}{\sum_z n_{z,g}},\qquad
# P(\text{Milei}\mid z,g)=\frac{\text{Milei}_{z,g}}{n_{z,g}}
# \]

# %%
# Conteos por Género x Voto (con totales)
ct_g = pd.crosstab(df["Género"], df["Voto"], margins=True, margins_name="Total")
ct_g

# %%
# Probabilidades condicionales P(Voto | Género)
p_g = pd.crosstab(df["Género"], df["Voto"], normalize="index", margins=True, margins_name="Total")
p_g.style.format("{:.2%}")

# %%
# Conteos por (Zona,Género) x Voto (con totales)
ct_zg = pd.crosstab([df["Zona"], df["Género"]], df["Voto"], margins=True, margins_name="Total")
ct_zg

# %%
# Probabilidades P(Voto | Zona, Género)
p_zg = pd.crosstab([df["Zona"], df["Género"]], df["Voto"], normalize="index", margins=True, margins_name="Total")
p_zg.style.format("{:.2%}")

# %% [markdown]
# **Lectura intermedia:** al **condicionar por Género**, se ve que `P(Milei | Rural, Hombre)` es muy alta y
# `P(Milei | Urbana, Mujer)` es baja (además son la mayoría de la muestra), explicando el sesgo del promedio por zona.

# %% [markdown]
# ## Paso 3 — **Reponderar por Género 50/50** con la misma evidencia condicional
# Con \(P(\text{Milei}\mid \text{Género})\) calculamos el agregado para un electorado balanceado: \(w_H=w_M=0.5\).  
# \[
# P(\text{Milei})=\sum_g P(\text{Milei}\mid g)\cdot w_g
# \]

# %%
w_g_5050 = pd.Series({"Hombre": 0.5, "Mujer": 0.5}, name="Peso género (50/50)")
p_milei_g = p_g["Milei"].drop("Total")
p_agg_g_5050 = float((p_milei_g * w_g_5050).sum())

tabla_g = pd.DataFrame({
    "P(Milei | Género)": p_milei_g.map("{:.2%}".format),
    "Peso género (50/50)": w_g_5050.map("{:.2%}".format),
})
tabla_g["Aporte"] = (p_milei_g * w_g_5050).map("{:.2%}".format)

fila_agregado_g = pd.DataFrame([{
    "P(Milei | Género)": "—",
    "Peso género (50/50)": "—",
    "Aporte": f"{p_agg_g_5050:.2%}"
}], index=["Agregado"])

pd.concat([tabla_g, fila_agregado_g])

# %%
print(f"Agregado por **género balanceado**: P(Milei) = {p_agg_g_5050:.2%}  → "
      f"{'Gana Milei' if p_agg_g_5050>0.5 else 'Gana Massa'}")

# %% [markdown]
# **Lectura final**  
# - Con `P(Voto|Zona)` y los **pesos de zona** de la muestra, el agregado favorecía a **Massa**.  
# - Al incorporar `P(Voto|Género)` y **reponderar** el electorado a 50/50, el agregado se mueve y puede favorecer a **Milei**.  
# - La conclusión depende de **qué variables condicionamos** y de los **pesos** usados al recombinar (zonas, géneros).
# %%
