# %% [markdown]
# # Estadística básica con encuestas (Argentina 2025)
# Cuaderno secuencial para explicar:
# 1) Medidas de tendencia central (media, mediana, moda, promedio ponderado)
# 2) Dispersión (desviación estándar, varianza, coeficiente de variación)
# 3) Distribuciones e **distribuciones acumuladas** (ECDF)
# 4) Distribución de frecuencias **condicionales** entre X e Y
#
# Todos los ejemplos se basan en encuestas de opinión pública en Argentina 2025.

# %%
import math
from statistics import mean, median, variance, stdev
from collections import Counter, defaultdict
import matplotlib.pyplot as plt
import random
import numpy as np
import pandas as pd

plt.rcParams["figure.figsize"] = (7,4)
plt.rcParams["axes.grid"] = True

# %% [markdown]
# # EJERCICIO 1 — Medidas de tendencia central con votos por mesa
# 120 mesas | votos para nuestro candidato por mesa (0–350).
# Se generan varias distribuciones, se calculan media–mediana–moda y se grafica cada una.
# Incluye: ejemplo secuencial (pocos valores) y un SANDBOX al final.

# %%

CAP_MESA = 350
N_MESAS  = 120

# %% [markdown]
# ## Ejemplo secuencial (pocos valores)
# Pequeño ejemplo con n impar para que la **mediana** sea entera.

# %%
ejemplo = [120, 140, 98, 132, 105, 150, 121]

suma = 0
for i, v in enumerate(ejemplo, start=1):
    antes = suma
    suma += v
    if i <= 5:
        print(f"Paso {i}: {antes} + {v} = {suma}")
    elif i == 6:
        print("... (pasos intermedios omitidos)")
media_ej = suma / len(ejemplo)
ordenados = sorted(ejemplo)
mediana_ej = ordenados[len(ordenados)//2]      # n impar → entero
moda_ej = Counter(ejemplo).most_common(1)[0][0]

print("\nResultados (ejemplo):")
print(f"  Media = {media_ej:.2f} | Mediana = {mediana_ej} | Moda = {moda_ej}")

# %% [markdown]
# ## Presets de distribuciones (votos por mesa)
# - **Movilización alta/baja (Binomial)**: p alta/baja → más/ménos votos esperados. Centro ≈ n·p.
# - **Competida (Normal recortada)**: campana alrededor de μ, con σ moderada.
# - **Sesgo alto/bajo (Beta)**: empuja la masa a valores altos o bajos.
# - **Polarizada (Beta < 1)**: picos en los extremos (bimodal en los bordes).
# Cada preset imprime **propiedades breves** y muestra **media, mediana y moda** en el gráfico.

# %%
PRESETS = {
    "movilizacion_alta": {
        "name": "Movilización alta (Binomial p=0.50)",
        "mode": "binomial", "N": N_MESAS, "SEED": 2025, "p": 0.50,
        "props": "p alta → centro ~ n·p (=175), var máx. en p=0.5."
    },
    "base_binomial": {
        "name": "Base (Binomial p=0.35)",
        "mode": "binomial", "N": N_MESAS, "SEED": 2025, "p": 0.35,
        "props": "apoyo moderado → centro ~ n·p (=122.5)."
    },
    "movilizacion_baja": {
        "name": "Movilización baja (Binomial p=0.20)",
        "mode": "binomial", "N": N_MESAS, "SEED": 2025, "p": 0.20,
        "props": "p baja → más masa en valores chicos (centro ~70)."
    },
    "competida_gauss": {
        "name": "Competida (Normal μ=120, σ=30)",
        "mode": "gauss", "N": N_MESAS, "SEED": 2025, "MU": 120, "SIGMA": 30,
        "props": "campana alrededor de μ; recortada a [0,350]."
    },
    "sesgo_alto_beta": {
        "name": "Sesgo a valores altos (Beta 5,2)",
        "mode": "beta", "N": N_MESAS, "SEED": 2025, "ALPHA": 5, "BETA": 2,
        "props": "empuja hacia valores altos (cola en bajos)."
    },
    "sesgo_bajo_beta": {
        "name": "Sesgo a valores bajos (Beta 2,5)",
        "mode": "beta", "N": N_MESAS, "SEED": 2025, "ALPHA": 2, "BETA": 5,
        "props": "empuja hacia valores bajos (cola en altos)."
    },
    "polarizada_beta": {
        "name": "Polarizada (Beta 0.6, 0.6)",
        "mode": "beta", "N": N_MESAS, "SEED": 2025, "ALPHA": 0.6, "BETA": 0.6,
        "props": "picos en 0 y 350; valle central (bimodal)."
    },
}
BAR_COLORS = {
    "movilizacion_alta": "#c7e9c0",
    "base_binomial":     "#9ecae1",
    "movilizacion_baja": "#fdae6b",
    "competida_gauss":   "#bcbddc",
    "sesgo_alto_beta":   "#fdd0a2",
    "sesgo_bajo_beta":   "#a1d99b",
    "polarizada_beta":   "#fb6a4a",
}

# %% [markdown]
# ## Funciones

# %%
def _clip(x, lo=0, hi=CAP_MESA):
    return lo if x < lo else hi if x > hi else x

def generar_votos(pkg: dict):
    """Lista de enteros 0–350 (120 mesas) según paquete."""
    random.seed(pkg.get("SEED", None))
    N = int(pkg["N"])
    mode = pkg["mode"]
    out = []
    if mode == "binomial":
        p = float(pkg["p"])
        for _ in range(N):
            # simulación simple de Binomial(n=350, p)
            ex = sum(1 for _t in range(CAP_MESA) if random.random() < p)
            out.append(ex)
    elif mode == "gauss":
        mu, sig = float(pkg["MU"]), float(pkg["SIGMA"])
        for _ in range(N):
            out.append(_clip(round(random.gauss(mu, sig))))
    elif mode == "beta":
        a, b = float(pkg["ALPHA"]), float(pkg["BETA"])
        for _ in range(N):
            u = random.betavariate(a, b)
            out.append(_clip(round(u * CAP_MESA)))
    else:
        raise ValueError("mode inválido")
    return out

def mediana_discreta(xs):
    xs = sorted(xs); n = len(xs)
    # para n par tomamos el menor de los dos centrales (medida discreta)
    return xs[n//2 - 1] if n % 2 == 0 else xs[n//2]

def _bins(step=20):
    edges = list(range(0, CAP_MESA + step, step))
    if edges[-1] < CAP_MESA: edges.append(CAP_MESA)
    return edges

def top_modos(xs, bins, k=2):
    """Centros de los k bins más altos (modas tipo histograma)."""
    counts, edges = np.histogram(xs, bins=bins)
    idx = np.argsort(counts)[::-1]  # de mayor a menor
    modos = []
    maxc = counts[idx[0]]
    for j in idx:
        if counts[j] < maxc: break  # solo los máximos (empates)
        centro = (edges[j] + edges[j+1]) / 2
        modos.append(centro)
        if len(modos) == k: break
    return modos

def mostrar_distribucion(key: str):
    """Imprime propiedades + medidas y grafica 1 distribución por llamada."""
    pkg = PRESETS[key]
    vals = generar_votos(pkg)
    m = mean(vals)
    med = mediana_discreta(vals)
    bins = _bins(step=20)
    modos = top_modos(vals, bins, k=2)    # puede devolver 1 o 2 picos

    print(pkg["name"])
    print("Propiedades:", pkg["props"])
    print(f"Medidas → n={len(vals)} | Media={m:.2f} | Mediana={med} | Moda(s)~ {[int(round(x)) for x in modos]}\n")

    plt.hist(vals, bins=bins, align="mid", rwidth=0.9,
             color=BAR_COLORS[key], edgecolor="black", zorder=1)

    plt.axvline(m,   color="#FF00FF", linewidth=2.8, linestyle="--", label=f"Media {m:.2f}", zorder=3)
    plt.axvline(med, color="#00CFFF", linewidth=2.8, linestyle="-.", label=f"Mediana {med}", zorder=3)
    for j, mc in enumerate(modos, start=1):
        lab = f"Moda ~{int(round(mc))}" if j == 1 else f"Moda 2 ~{int(round(mc))}"
        plt.axvline(mc, color="#FF7F0E", linewidth=2.8, linestyle="-", label=lab, zorder=3)

    plt.title(pkg["name"])
    plt.xlabel("Votos para el candidato por mesa")
    plt.ylabel("Frecuencia (mesas)")
    plt.xlim(0, CAP_MESA)
    plt.legend()
    plt.show()

# %% [markdown]
# ## Plots (llamar uno por vez)
# Ejecuta una celda por distribución. Cada llamada imprime sus propiedades y medidas y dibuja el histograma.

# %%
# movilización alta (p grande)
mostrar_distribucion("movilizacion_alta")

# %%
# base binomial (apoyo moderado)
mostrar_distribucion("base_binomial")

# %%
# movilización baja (p chica)
mostrar_distribucion("movilizacion_baja")

# %%
# competida (normal recortada)
mostrar_distribucion("competida_gauss")

# %%
# sesgo a valores altos
mostrar_distribucion("sesgo_alto_beta")

# %%
# sesgo a valores bajos
mostrar_distribucion("sesgo_bajo_beta")

# %%
# polarizada (picos en extremos; pueden verse dos líneas naranjas si hay empate de picos)
mostrar_distribucion("polarizada_beta")

# %% [markdown]
# ## SANDBOX — tu propia distribución
# Edita el paquete y llama `mostrar_distribucion_sbx(SANDBOX)`.

# %%
SANDBOX = {
    "name": "Mi binomial competitiva (p=0.42)",
    "mode": "binomial", "N": N_MESAS, "SEED": 2025, "p": 0.42,
    "props": "p intermedia → centro ~ n·p (=147)."
    # Ejemplos:
    # {"name":"Mi normal (μ=180,σ=35)","mode":"gauss","N":N_MESAS,"SEED":2025,"MU":180,"SIGMA":35,"props":"campana centrada alta."}
    # {"name":"Mi beta (4.5,2.0)","mode":"beta","N":N_MESAS,"SEED":2025,"ALPHA":4.5,"BETA":2.0,"props":"sesgo alto."}
}

# %%
def mostrar_distribucion_sbx(pkg: dict, color="#6baed6"):
    vals = generar_votos(pkg)
    m = mean(vals)
    med = mediana_discreta(vals)
    bins = _bins(step=20)
    modos = top_modos(vals, bins, k=2)

    print(pkg["name"])
    if "props" in pkg: print("Propiedades:", pkg["props"])
    print(f"Medidas → n={len(vals)} | Media={m:.2f} | Mediana={med} | Moda(s)~ {[int(round(x)) for x in modos]}\n")

    plt.hist(vals, bins=bins, align="mid", rwidth=0.9,
             color=color, edgecolor="black", zorder=1)
    plt.axvline(m,   color="#FF00FF", linewidth=2.8, linestyle="--", label=f"Media {m:.2f}", zorder=3)
    plt.axvline(med, color="#00CFFF", linewidth=2.8, linestyle="-.", label=f"Mediana {med}", zorder=3)
    for j, mc in enumerate(modos, start=1):
        lab = f"Moda ~{int(round(mc))}" if j == 1 else f"Moda 2 ~{int(round(mc))}"
        plt.axvline(mc, color="#FF7F0E", linewidth=2.8, linestyle="-", label=lab, zorder=3)
    plt.title(pkg["name"])
    plt.xlabel("Votos para el candidato por mesa")
    plt.ylabel("Frecuencia (mesas)")
    plt.xlim(0, CAP_MESA)
    plt.legend()
    plt.show()

# %%
mostrar_distribucion_sbx(SANDBOX)
######################################################################################
# %% [markdown]
# # EJERCICIO 2 — Dispersión de **satisfacción** por municipio (PBA, 2025)
# Variable: satisfacción (escala entera 1–10). Se definen municipios con medias y dispersiones distintas.
# Cada plot se genera llamando a una función y muestra **media**, **desvío**, **varianza** y **coef. de variación (CV)**.
# Al final hay un **SANDBOX** con parámetros simples: `media`, `sigma`, `n`.


# %% [markdown]
# ## Presets (municipios con medias y dispersiones distintas)

# %%
MUNICIPIOS = {
    "La_Plata":      {"name": "La Plata",        "mu": 6.2, "sigma": 0.9, "n": 200, "seed": 2025,
                      "props": "media alta, baja dispersión"},
    "Mar_del_Plata": {"name": "Mar del Plata",   "mu": 5.8, "sigma": 1.3, "n": 200, "seed": 2025,
                      "props": "media media, dispersión moderada"},
    "Bahia_Blanca":  {"name": "Bahía Blanca",    "mu": 6.5, "sigma": 1.8, "n": 200, "seed": 2025,
                      "props": "media alta, dispersión alta"},
    "Quilmes":       {"name": "Quilmes",         "mu": 5.2, "sigma": 1.5, "n": 200, "seed": 2025,
                      "props": "media baja-media, dispersión media"},
    "Moreno":        {"name": "Moreno",          "mu": 4.8, "sigma": 1.7, "n": 200, "seed": 2025,
                      "props": "media baja, dispersión alta"},
    "San_Isidro":    {"name": "San Isidro",      "mu": 7.0, "sigma": 0.8, "n": 200, "seed": 2025,
                      "props": "media muy alta, baja dispersión"},
}
COLORS = {
    "La_Plata": "#6baed6",
    "Mar_del_Plata": "#74c476",
    "Bahia_Blanca": "#fd8d3c",
    "Quilmes": "#9e9ac8",
    "Moreno": "#fb6a4a",
    "San_Isidro": "#31a354",
}

# %% [markdown]
# ## Utilidades

# %%
def _clip_1_10(x):  # recorta al rango 1..10
    return 1 if x < 1 else 10 if x > 10 else x

def simular_satisfaccion(mu: float, sigma: float, n: int, seed: int = 2025):
    random.seed(seed)
    datos = []
    for _ in range(n):
        x = round(random.gauss(mu, sigma))   # entero
        datos.append(_clip_1_10(x))
    return datos

def cv_porcentaje(xs):
    m = mean(xs)
    return float('nan') if m == 0 else (stdev(xs) / m) * 100

def plot_dispersion(xs, titulo, color):
    m  = mean(xs)
    sd = stdev(xs)
    var = variance(xs)
    cv = cv_porcentaje(xs)

    # Histograma (barras enteras 1..10)
    plt.hist(xs, bins=range(1,12), align="left", rwidth=0.85,
             color=color, edgecolor="black", zorder=1)
    # Líneas de media y ±1σ
    plt.axvline(m,      color="#FF00FF", linewidth=2.6, linestyle="--", label=f"Media {m:.2f}", zorder=3)
    plt.axvline(m - sd, color="#00CFFF", linewidth=2.0, linestyle="-.", label=f"−1σ {max(m-sd,1):.2f}", zorder=3)
    plt.axvline(m + sd, color="#00CFFF", linewidth=2.0, linestyle="-.", label=f"+1σ {min(m+sd,10):.2f}", zorder=3)

    plt.title(titulo)
    plt.xlabel("Satisfacción (1–10)")
    plt.ylabel("Frecuencia")
    plt.xticks(range(1,11))
    plt.legend()
    # Anotación CV
    plt.text(0.02, 0.95, f"Var={var:.2f} | σ={sd:.2f} | CV={cv:.1f}%",
             transform=plt.gca().transAxes, va="top", ha="left",
             bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.9))
    plt.show()

def mostrar_municipio(key: str):
    cfg = MUNICIPIOS[key]
    xs  = simular_satisfaccion(cfg["mu"], cfg["sigma"], cfg["n"], cfg["seed"])
    print(f"{cfg['name']} — {cfg['props']}")
    print(f"n={len(xs)} | media={mean(xs):.2f} | σ={stdev(xs):.2f} | var={variance(xs):.2f} | CV={cv_porcentaje(xs):.1f}%\n")
    plot_dispersion(xs, f"Satisfacción — {cfg['name']}", COLORS[key])

# %% [markdown]
# ## Plots 1 a 1 (ejecuta la(s) llamada(s) que desees)

# %%
mostrar_municipio("La_Plata")

# %%
mostrar_municipio("Mar_del_Plata")

# %%
mostrar_municipio("Bahia_Blanca")

# %%
mostrar_municipio("Quilmes")

# %%
mostrar_municipio("Moreno")

# %%
mostrar_municipio("San_Isidro")

# %% [markdown]
# ## SANDBOX — parámetros simples
# Cambia `media`, `sigma`, `n` (y opcional `seed`). Ejecuta estas dos celdas.

# %%
SANDBOX = {
    "name":  "Mi municipio (μ=6.3, σ=1.2, n=250)",
    "media": 5,
    "sigma": 4,
    "n":     250,
    "seed":  202,
    "color": "#1f77b4"
}

# %%
xs = simular_satisfaccion(SANDBOX["media"], SANDBOX["sigma"], SANDBOX["n"], SANDBOX["seed"])
print(f"{SANDBOX['name']}")
print(f"n={len(xs)} | media={mean(xs):.2f} | σ={stdev(xs):.2f} | var={variance(xs):.2f} | CV={cv_porcentaje(xs):.1f}%\n")
plot_dispersion(xs, SANDBOX["name"], SANDBOX["color"])

# %% [markdown]
# # EJERCICIO 3 — Frecuencia acumulada (ECDF) y **promedio ponderado por población**
# Caso: **La Matanza (LM)** vs **San Isidro (SI)**, 2025.
# Meta: mostrar que **M** puede tener **mayor media no ponderada**, pero al ponderar por población
# (LM >> SI) el agregado favorece a **P**.

# -------------------- Población usada para ponderar (tabla) --------------------
POB = {
    "La Matanza": 1_800_000,
    "San Isidro":   300_000,
}

print("Poblaciones para ponderación")
print("Municipio     | Población")
for k, v in POB.items():
    print(f"{k:12s} | {v:,}")
print()

# %% [markdown]
# ## 1) Simulación (reproducible)
# Diseñamos medias para forzar el efecto:
# - LM: **P** alto (≈7.2), **M** bajo (≈5.2)
# - SI: **M** alto (≈7.4), **P** bajo (≈4.6)

# %%
def _clip_1_10(x): 
    return 1 if x < 1 else 10 if x > 10 else x

def simular(mu, sigma, n, seed):
    random.seed(seed)
    return [_clip_1_10(round(random.gauss(mu, sigma))) for _ in range(n)]

N_LM = 500
N_SI = 500

# La Matanza
LM_P = simular(mu=7.2, sigma=0.8, n=N_LM, seed=123)
LM_M = simular(mu=5.2, sigma=0.9, n=N_LM, seed=124)

# San Isidro
SI_P = simular(mu=4.6, sigma=0.8, n=N_SI, seed=223)
SI_M = simular(mu=7.4, sigma=0.8, n=N_SI, seed=224)

# %% [markdown]
# ## 2) Tablas de **frecuencia relativa** y **acumulada** (por municipio y candidato)

def tablas(xs):
    vals = list(range(1, 11))
    c = Counter(xs)
    f_abs = [c.get(v, 0) for v in vals]
    tot = sum(f_abs)
    f_rel = [f/tot for f in f_abs]
    ac_rel = list(np.cumsum(f_rel))
    return vals, f_rel, ac_rel, tot

def imprimir_tabla(titulo, xs):
    vals, f_rel, ac_rel, tot = tablas(xs)
    print(f"{titulo}  | n={tot}")
    print("Valor |  f_rel% |  acum%")
    for v, fr, ar in zip(vals, f_rel, ac_rel):
        print(f"{v:>5} | {fr*100:7.2f} | {ar*100:7.2f}")
    print()

imprimir_tabla("La Matanza — P", LM_P)
imprimir_tabla("La Matanza — M", LM_M)
imprimir_tabla("San Isidro — P", SI_P)
imprimir_tabla("San Isidro — M", SI_M)

# %% [markdown]
# ## 3) ECDF (una por municipio)

def plot_ecdf(d1, d2, lab1, lab2, titulo, color1, color2):
    x1 = sorted(d1); y1 = np.arange(1, len(x1)+1)/len(x1)
    x2 = sorted(d2); y2 = np.arange(1, len(x2)+1)/len(x2)
    plt.step(x1, y1, where="post", linewidth=2.3, label=lab1, color=color1)
    plt.step(x2, y2, where="post", linewidth=2.3, label=lab2, color=color2)
    plt.axvline(6, color="#888", linestyle="--", linewidth=1.6, label="Umbral 6")
    plt.title(titulo)
    plt.xlabel("Satisfacción (1–10)")
    plt.ylabel("Proporción acumulada")
    plt.xlim(1, 10); plt.ylim(0, 1.02); plt.legend(); plt.show()

plot_ecdf(LM_P, LM_M, "P en La Matanza", "M en La Matanza",
          "ECDF — La Matanza (P domina)", "#1f77b4", "#ff7f0e")

plot_ecdf(SI_P, SI_M, "P en San Isidro", "M en San Isidro",
          "ECDF — San Isidro (M domina)", "#1f77b4", "#ff7f0e")

# %% [markdown]
# ## 4) Medias locales y comparación **no ponderada** vs **ponderada**
# - **No ponderada**: promedio simple de las medias municipales (M gana).
# - **Ponderada por población**: LM pesa mucho más → el agregado favorece a **P**.

# %%
# Medias locales
LM_P_mean, LM_M_mean = mean(LM_P), mean(LM_M)
SI_P_mean, SI_M_mean = mean(SI_P), mean(SI_M)

print("Medias locales")
print(f"  La Matanza:  P={LM_P_mean:.2f} | M={LM_M_mean:.2f}")
print(f"  San Isidro:  P={SI_P_mean:.2f} | M={SI_M_mean:.2f}\n")

# No ponderada (promedio simple de medias municipales)
P_unw = (LM_P_mean + SI_P_mean)/2
M_unw = (LM_M_mean + SI_M_mean)/2

# Ponderada por población
TOT_POP = POB["La Matanza"] + POB["San Isidro"]
P_w = (LM_P_mean*POB["La Matanza"] + SI_P_mean*POB["San Isidro"]) / TOT_POP
M_w = (LM_M_mean*POB["La Matanza"] + SI_M_mean*POB["San Isidro"]) / TOT_POP

print("Promedio de satisfacción — **antes** de ponderar (media simple de municipios)")
print(f"  P={P_unw:.2f}   |   M={M_unw:.2f}   →", "Gana M" if M_unw>P_unw else "Gana P")
print("\nPromedio de satisfacción — **ponderado por población**")
print(f"  P={P_w:.2f}   |   M={M_w:.2f}     →", "Gana M" if M_w>P_w else "Gana P")

# Lectura breve
print("\nLectura:")
print("• En SI, M tiene valores más altos; en LM, P es claramente superior (ver ECDFs).")
print("• Con la media **no ponderada** (promedio simple de municipios), M queda arriba.")
print("• Al **ponderar por población**, el peso demográfico de La Matanza invierte el resultado y favorece a P.")


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
