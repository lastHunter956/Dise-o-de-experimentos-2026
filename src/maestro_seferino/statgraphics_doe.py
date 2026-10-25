"""
statgraphics_doe.py
-------------------
Motor de simulación de Statgraphics Centurion para Diseño de Experimentos (DOE).
Soporta factoriales completos 2^k y factoriales fraccionados 2^(k-p),
cálculo de estructuras de alias (resolución), descomposición ANOVA,
exclusión de términos (calculadora de análisis), colapsación de diseños
y generación de coordenadas para gráficos estilo Statgraphics.

100% local al proyecto maestro-seferino.
"""

from __future__ import annotations
import math
import itertools
from typing import Any
import numpy as np
import pandas as pd
from scipy import stats

# ------------------------------------------------------------------------------
# 1. BASES DE DATOS OFICIALES DEL TEXTO (GUTIÉRREZ & DE LA VARA)
# ------------------------------------------------------------------------------

# Tabla 6.14: Experimento 2^5 Completo (32 corridas)
DATOS_2_5_COMPLETO = [
    # Bloque E = -1, D = -1
    (1,  -1, -1, -1, -1, -1, '(1)', 7.0),
    (2,   1, -1, -1, -1, -1, 'a',   9.0),
    (3,  -1,  1, -1, -1, -1, 'b',   34.0),
    (4,   1,  1, -1, -1, -1, 'ab',  55.0),
    (5,  -1, -1,  1, -1, -1, 'c',   16.0),
    (6,   1, -1,  1, -1, -1, 'ac',  20.0),
    (7,  -1,  1,  1, -1, -1, 'bc',  41.0),
    (8,   1,  1,  1, -1, -1, 'abc', 60.0),
    # Bloque E = -1, D = +1
    (9,  -1, -1, -1,  1, -1, 'd',    8.0),
    (10,  1, -1, -1,  1, -1, 'ad',   10.0),
    (11, -1,  1, -1,  1, -1, 'bd',   32.0),
    (12,  1,  1, -1,  1, -1, 'abd',  50.0),
    (13, -1, -1,  1,  1, -1, 'cd',   18.0),
    (14,  1, -1,  1,  1, -1, 'acd',  21.0),
    (15, -1,  1,  1,  1, -1, 'bcd',  44.0),
    (16,  1,  1,  1,  1, -1, 'abcd', 61.0),
    # Bloque E = +1, D = -1
    (17, -1, -1, -1, -1,  1, 'e',    8.0),
    (18,  1, -1, -1, -1,  1, 'ae',   12.0),
    (19, -1,  1, -1, -1,  1, 'be',   35.0),
    (20,  1,  1, -1, -1,  1, 'abe',  52.0),
    (21, -1, -1,  1, -1,  1, 'ce',   15.0),
    (22,  1, -1,  1, -1,  1, 'ace',  22.0),
    (23, -1,  1,  1, -1,  1, 'bce',  45.0),
    (24,  1,  1,  1, -1,  1, 'abce', 65.0),
    # Bloque E = +1, D = +1
    (25, -1, -1, -1,  1,  1, 'de',    6.0),
    (26,  1, -1, -1,  1,  1, 'ade',   10.0),
    (27, -1,  1, -1,  1,  1, 'bde',   30.0),
    (28,  1,  1, -1,  1,  1, 'abde',  53.0),
    (29, -1, -1,  1,  1,  1, 'cde',   15.0),
    (30,  1, -1,  1,  1,  1, 'acde',  20.0),
    (31, -1,  1,  1,  1,  1, 'bcde',  41.0),
    (32,  1,  1,  1,  1,  1, 'abcde', 63.0)
]

# Tabla 8.4: Fracción Principal 2^(5-1) (I = +ABCDE, 16 corridas)
DATOS_2_5_1_PRINCIPAL = [
    (1,  -1, -1, -1, -1,  1, 'e',     8.0),
    (2,   1, -1, -1, -1, -1, 'a',     9.0),
    (3,  -1,  1, -1, -1, -1, 'b',    34.0),
    (4,   1,  1, -1, -1,  1, 'abe',  52.0),
    (5,  -1, -1,  1, -1, -1, 'c',    16.0),
    (6,   1, -1,  1, -1,  1, 'ace',  22.0),
    (7,  -1,  1,  1, -1,  1, 'bce',  45.0),
    (8,   1,  1,  1, -1, -1, 'abc',  60.0),
    (9,  -1, -1, -1,  1, -1, 'd',     8.0),
    (10,  1, -1, -1,  1,  1, 'ade',  10.0),
    (11, -1,  1, -1,  1,  1, 'bde',  30.0),
    (12,  1,  1, -1,  1, -1, 'abd',  50.0),
    (13, -1, -1,  1,  1,  1, 'cde',  15.0),
    (14,  1, -1,  1,  1, -1, 'acd',  21.0),
    (15, -1,  1,  1,  1, -1, 'bcd',  44.0),
    (16,  1,  1,  1,  1,  1, 'abcde', 63.0)
]

# Tabla 8.4: Fracción Complementaria 2^(5-1) (I = -ABCDE, 16 corridas)
DATOS_2_5_1_COMPLEMENTARIA = [
    (1,  -1, -1, -1, -1, -1, '(1)',   7.0),
    (2,   1, -1, -1, -1,  1, 'ae',   12.0),
    (3,  -1,  1, -1, -1,  1, 'be',   35.0),
    (4,   1,  1, -1, -1, -1, 'ab',   55.0),
    (5,  -1, -1,  1, -1,  1, 'ce',   15.0),
    (6,   1, -1,  1, -1, -1, 'ac',   20.0),
    (7,  -1,  1,  1, -1, -1, 'bc',   40.0),
    (8,   1,  1,  1, -1,  1, 'abce', 65.0),
    (9,  -1, -1, -1,  1,  1, 'de',    6.0),
    (10,  1, -1, -1,  1, -1, 'ad',   10.0),
    (11, -1,  1, -1,  1, -1, 'bd',   32.0),
    (12,  1,  1, -1,  1,  1, 'abde', 53.0),
    (13, -1, -1,  1,  1, -1, 'cd',   18.0),
    (14,  1, -1,  1,  1,  1, 'acde', 20.0),
    (15, -1,  1,  1,  1,  1, 'bcde', 41.0),
    (16,  1,  1,  1,  1, -1, 'abcd', 61.0)
]

COLS = ['Corrida', 'A', 'B', 'C', 'D', 'E', 'Tratamiento', 'Rendimiento']

def get_dataset(part: str = "completo") -> pd.DataFrame:
    """Retorna el DataFrame oficial según la parte solicitada."""
    if part == "completo":
        return pd.DataFrame(DATOS_2_5_COMPLETO, columns=COLS)
    elif part in ["principal", "fraccion_principal"]:
        return pd.DataFrame(DATOS_2_5_1_PRINCIPAL, columns=COLS)
    elif part in ["complementaria", "fraccion_complementaria"]:
        return pd.DataFrame(DATOS_2_5_1_COMPLEMENTARIA, columns=COLS)
    else:
        raise ValueError(f"Parte desconocida: {part}")

# ------------------------------------------------------------------------------
# 2. CÁLCULO DE ESTRUCTURA DE ALIAS (RESOLUCIÓN V)
# ------------------------------------------------------------------------------

def compute_alias_structure_2_5_1(sign_generator: int = +1) -> dict[str, str]:
    """
    Retorna la estructura de confusión de efectos para el diseño 2^(5-1)
    con generador I = sign_generator * ABCDE.
    Resolución V: Ningún efecto principal está confundido con interacciones dobles.
    Interacciones dobles están confundidas con interacciones triples.
    """
    sgn = "+" if sign_generator > 0 else "-"
    opp_sgn = "-" if sign_generator > 0 else "+"

    # Los 15 contrastes independientes estimables
    aliases = {
        "A": f"A {sgn} BCDE",
        "B": f"B {sgn} ACDE",
        "C": f"C {sgn} ABDE",
        "D": f"D {sgn} ABCE",
        "E": f"E {sgn} ABCD",
        "AB": f"AB {sgn} CDE",
        "AC": f"AC {sgn} BDE",
        "AD": f"AD {sgn} BCE",
        "AE": f"AE {sgn} BCD",
        "BC": f"BC {sgn} ADE",
        "BD": f"BD {sgn} ACE",
        "BE": f"BE {sgn} ACD",
        "CD": f"CD {sgn} ABE",
        "CE": f"CE {sgn} ABD",
        "DE": f"DE {sgn} ABC"
    }
    return aliases

# ------------------------------------------------------------------------------
# 3. MOTOR DE ESTIMACIÓN DE EFECTOS PARA STATGRAPHICS
# ------------------------------------------------------------------------------

def analyze_statgraphics_design(
    df: pd.DataFrame,
    factors: list[str] = ['A', 'B', 'C', 'D', 'E'],
    response_col: str = 'Rendimiento',
    max_order: int = 2
) -> dict[str, Any]:
    """
    Simula el comando 'DOE -> Analizar Diseño' de Statgraphics.
    Calcula efectos, sumas de cuadrados, errores estándar, estadísticos t y coordenadas de Daniel.
    """
    N = len(df)
    y = df[response_col].values
    grand_mean = float(np.mean(y))
    sct = float(np.sum((y - grand_mean) ** 2))

    # Identificar si es factorial completo (N=32) o fraccionado (N=16)
    k = len(factors)
    divisor_efecto = N / 2.0  # Para N=32 es 16; para N=16 es 8

    effects = []
    # Evaluar hasta max_order (o todos si se especifica)
    eval_orders = list(range(1, max_order + 1))
    for order in eval_orders:
        for combo in itertools.combinations(factors, order):
            name = "".join(combo)
            sign = np.ones(N)
            for f in combo:
                sign *= df[f].values
            contrast = float(np.sum(sign * y))
            eff = contrast / divisor_efecto
            ss = (contrast ** 2) / float(N)
            beta = eff / 2.0
            effects.append({
                "Termino": name,
                "Orden": order,
                "Contraste": contrast,
                "Efecto": eff,
                "AbsEfecto": abs(eff),
                "Coeficiente": beta,
                "SC": ss,
                "GL": 1
            })

    eff_df = pd.DataFrame(effects)

    # Coordenadas de Daniel (Papel Normal)
    daniel_df = eff_df.sort_values(by="Efecto").reset_index(drop=True).copy()
    P = len(daniel_df)
    daniel_df["Rank"] = np.arange(1, P + 1)
    daniel_df["Prob_Empirica"] = (daniel_df["Rank"] - 0.5) / P
    daniel_df["Z_Normal"] = stats.norm.ppf(daniel_df["Prob_Empirica"])

    # Gráfico Half-Normal (Semi-Normal) de Daniel
    half_df = eff_df.sort_values(by="AbsEfecto").reset_index(drop=True).copy()
    half_df["Rank"] = np.arange(1, P + 1)
    # Probabilidad semi-normal: p = 0.5 + 0.5*(i - 0.5)/P
    half_df["Prob_Half"] = 0.5 + 0.5 * (half_df["Rank"] - 0.5) / P
    half_df["Z_Half"] = stats.norm.ppf(half_df["Prob_Half"])

    # Diagrama de Pareto
    pareto_df = eff_df.sort_values(by="AbsEfecto", ascending=False).reset_index(drop=True).copy()

    return {
        "N": N,
        "grand_mean": grand_mean,
        "sct": sct,
        "effects_df": eff_df,
        "daniel_df": daniel_df,
        "half_df": half_df,
        "pareto_df": pareto_df
    }

# ------------------------------------------------------------------------------
# 4. TABLA ANOVA AL ESTILO STATGRAPHICS (CON POOLING Y EXCLUSIÓN)
# ------------------------------------------------------------------------------

def build_statgraphics_anova(
    effects_df: pd.DataFrame,
    sct: float,
    included_terms: list[str]
) -> tuple[pd.DataFrame, dict[str, float]]:
    """
    Construye la tabla ANOVA formateada exactamente como Statgraphics:
    Fuente | Suma de Cuadrados | Gl | Cuadrado Medio | Razón-F | Valor-P
    """
    active = effects_df[effects_df["Termino"].isin(included_terms)].copy()
    # Los términos no incluidos van al error (Pooling)
    excluded = effects_df[~effects_df["Termino"].isin(included_terms)].copy()

    sc_model = float(active["SC"].sum())
    gl_model = int(active["GL"].sum())

    # La suma de cuadrados del error es la diferencia con el total
    sc_error = sct - sc_model
    total_gl = len(effects_df)  # O N-1
    gl_error = (len(effects_df) if total_gl > 31 else 31) - gl_model

    cm_error = sc_error / gl_error if gl_error > 0 else np.nan

    active["CM"] = active["SC"] / active["GL"]
    active["Razon_F"] = active["CM"] / cm_error if cm_error > 0 else np.nan
    active["Valor_p"] = stats.f.sf(active["Razon_F"], active["GL"], gl_error) if gl_error > 0 else np.nan

    error_row = pd.DataFrame([{
        "Termino": "Error residual",
        "Orden": 0,
        "Contraste": np.nan,
        "Efecto": np.nan,
        "AbsEfecto": np.nan,
        "Coeficiente": np.nan,
        "SC": sc_error,
        "GL": gl_error,
        "CM": cm_error,
        "Razon_F": np.nan,
        "Valor_p": np.nan
    }])

    total_row = pd.DataFrame([{
        "Termino": "Total (corregido)",
        "Orden": 0,
        "Contraste": np.nan,
        "Efecto": np.nan,
        "AbsEfecto": np.nan,
        "Coeficiente": np.nan,
        "SC": sct,
        "GL": gl_model + gl_error,
        "CM": np.nan,
        "Razon_F": np.nan,
        "Valor_p": np.nan
    }])

    table = pd.concat([active, error_row, total_row], ignore_index=True)

    r2 = sc_model / sct
    r2_adj = 1.0 - (sc_error / gl_error) / (sct / (gl_model + gl_error)) if gl_error > 0 else np.nan

    metrics = {
        "R2": r2,
        "R2_Adj": r2_adj,
        "CME": cm_error,
        "RMSE": float(np.sqrt(cm_error)) if cm_error > 0 else np.nan,
        "GL_Error": gl_error,
        "SC_Error": sc_error
    }

    return table, metrics
