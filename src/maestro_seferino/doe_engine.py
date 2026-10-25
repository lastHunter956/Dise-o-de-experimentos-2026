"""
doe_engine.py
-------------
Motor analítico determinista para Diseño y Análisis de Experimentos (DOE).
Especializado en Diseños Factoriales 2^k (replicados y no replicados),
cálculo de contrastes y efectos de Yates, descomposición ANOVA,
construcción de gráficos de Cuthbert Daniel, selección por parsimonia (Mejor ANOVA)
y diagnóstico riguroso de supuestos residuales.

100% autónomo y localizado en el proyecto maestro-seferino.
"""

from __future__ import annotations
import itertools
from typing import Any
import numpy as np
import pandas as pd
from scipy import stats

def get_yates_label(bits: list[int], factor_names: list[str]) -> str:
    """Retorna la etiqueta de Yates para una combinación dada (-1 o 1)."""
    active = [factor_names[i].lower() for i, b in enumerate(bits) if b == 1]
    return "".join(active) if active else "(1)"

def build_2k_design(factors: list[str], response_values: list[float] | None = None) -> pd.DataFrame:
    """
    Construye la matriz en orden estándar de Yates para k factores.
    A varía cada 1 corrida, B cada 2, C cada 4, etc.
    """
    k = len(factors)
    n_runs = 2 ** k
    rows = []
    for i in range(n_runs):
        row = {}
        bits = []
        for j, factor in enumerate(factors):
            # Alterna cada 2^j
            bit_val = 1 if ((i >> j) & 1) else -1
            row[factor] = bit_val
            bits.append(bit_val)
        row["Tratamiento"] = get_yates_label(bits, factors)
        row["Orden_Estandar"] = i + 1
        if response_values is not None:
            row["Y"] = response_values[i]
        rows.append(row)
    return pd.DataFrame(rows)

def compute_factorial_effects(
    df: pd.DataFrame,
    factors: list[str],
    response_col: str = "Y",
    n_reps: int = 1
) -> dict[str, Any]:
    """
    Calcula los 2^k - 1 contrastes, efectos, coeficientes beta y sumas de cuadrados.
    """
    k = len(factors)
    y = df[response_col].values
    N = len(y)
    runs_per_rep = 2 ** k
    grand_mean = float(np.mean(y))
    sct = float(np.sum(y ** 2) - (np.sum(y) ** 2) / N)

    effects_list = []
    for order in range(1, k + 1):
        for combo in itertools.combinations(factors, order):
            term_name = "".join(combo)
            sign_vector = np.ones(N)
            for f in combo:
                sign_vector *= df[f].values

            contrast = float(np.sum(sign_vector * y))
            # Efecto = Contraste / (n * 2^(k-1))
            effect = contrast / (n_reps * (2 ** (k - 1)))
            # Suma de Cuadrados = Contraste^2 / (n * 2^k)
            ss = (contrast ** 2) / (n_reps * (2 ** k))
            beta = effect / 2.0

            effects_list.append({
                "Termino": term_name,
                "Orden": order,
                "Contraste": contrast,
                "Efecto": effect,
                "AbsEfecto": abs(effect),
                "Coeficiente": beta,
                "SC": ss,
                "GL": 1
            })

    effects_df = pd.DataFrame(effects_list)

    # Coordenadas para el Gráfico de Daniel (Papel de Probabilidad Normal)
    daniel_df = effects_df.sort_values(by="Efecto").reset_index(drop=True).copy()
    P = len(daniel_df)
    daniel_df["Rank"] = np.arange(1, P + 1)
    daniel_df["Prob_Empirica"] = (daniel_df["Rank"] - 0.5) / P
    daniel_df["Z_Normal"] = stats.norm.ppf(daniel_df["Prob_Empirica"])

    # Diagrama de Pareto (orden descendente de magnitud absoluta)
    pareto_df = effects_df.sort_values(by="AbsEfecto", ascending=False).reset_index(drop=True).copy()

    return {
        "k": k,
        "n_reps": n_reps,
        "N": N,
        "grand_mean": grand_mean,
        "sct": sct,
        "effects_df": effects_df,
        "daniel_df": daniel_df,
        "pareto_df": pareto_df
    }

def build_preliminary_anova(
    effects_df: pd.DataFrame,
    sct: float,
    max_order_included: int = 2
) -> pd.DataFrame:
    """
    Construye el ANOVA preliminar enviando las interacciones de orden superior
    (> max_order_included) al error experimental (Pooling).
    """
    included = effects_df[effects_df["Orden"] <= max_order_included].copy()
    excluded = effects_df[effects_df["Orden"] > max_order_included].copy()

    sc_error = float(excluded["SC"].sum())
    gl_error = int(excluded["GL"].sum())
    cm_error = sc_error / gl_error if gl_error > 0 else np.nan

    included["CM"] = included["SC"] / included["GL"]
    included["F_0"] = included["CM"] / cm_error
    included["p_value"] = stats.f.sf(included["F_0"], included["GL"], gl_error)

    # Filas de error y total
    error_row = pd.DataFrame([{
        "Termino": "Error experimental (Pool)",
        "Orden": 0,
        "Contraste": np.nan,
        "Efecto": np.nan,
        "AbsEfecto": np.nan,
        "Coeficiente": np.nan,
        "SC": sc_error,
        "GL": gl_error,
        "CM": cm_error,
        "F_0": np.nan,
        "p_value": np.nan
    }])

    total_gl = int(effects_df["GL"].sum())
    total_row = pd.DataFrame([{
        "Termino": "Total",
        "Orden": 0,
        "Contraste": np.nan,
        "Efecto": np.nan,
        "AbsEfecto": np.nan,
        "Coeficiente": np.nan,
        "SC": sct,
        "GL": total_gl,
        "CM": np.nan,
        "F_0": np.nan,
        "p_value": np.nan
    }])

    return pd.concat([included, error_row, total_row], ignore_index=True)

def build_best_anova(
    effects_df: pd.DataFrame,
    sct: float,
    selected_terms: list[str]
) -> tuple[pd.DataFrame, dict[str, float]]:
    """
    Construye el Mejor ANOVA conservando únicamente los términos activos seleccionados
    y transfiriendo el resto a la Suma de Cuadrados del Error.
    """
    active = effects_df[effects_df["Termino"].isin(selected_terms)].copy()
    pooled = effects_df[~effects_df["Termino"].isin(selected_terms)].copy()

    sc_model = float(active["SC"].sum())
    gl_model = int(active["GL"].sum())

    sc_error = float(pooled["SC"].sum())
    gl_error = int(pooled["GL"].sum())
    cm_error = sc_error / gl_error if gl_error > 0 else np.nan

    active["CM"] = active["SC"] / active["GL"]
    active["F_0"] = active["CM"] / cm_error
    active["p_value"] = stats.f.sf(active["F_0"], active["GL"], gl_error)

    error_row = pd.DataFrame([{
        "Termino": "Error",
        "Orden": 0,
        "Contraste": np.nan,
        "Efecto": np.nan,
        "AbsEfecto": np.nan,
        "Coeficiente": np.nan,
        "SC": sc_error,
        "GL": gl_error,
        "CM": cm_error,
        "F_0": np.nan,
        "p_value": np.nan
    }])

    total_gl = gl_model + gl_error
    total_row = pd.DataFrame([{
        "Termino": "Total",
        "Orden": 0,
        "Contraste": np.nan,
        "Efecto": np.nan,
        "AbsEfecto": np.nan,
        "Coeficiente": np.nan,
        "SC": sct,
        "GL": total_gl,
        "CM": np.nan,
        "F_0": np.nan,
        "p_value": np.nan
    }])

    anova_table = pd.concat([active, error_row, total_row], ignore_index=True)

    # Métricas de bondad de ajuste
    r2 = sc_model / sct
    r2_adj = 1.0 - (sc_error / gl_error) / (sct / total_gl)

    metrics = {
        "SC_Modelo": sc_model,
        "GL_Modelo": gl_model,
        "SC_Error": sc_error,
        "GL_Error": gl_error,
        "CM_Error": cm_error,
        "R2": r2,
        "R2_Adj": r2_adj,
        "Desv_Error": float(np.sqrt(cm_error))
    }

    return anova_table, metrics

def fit_coded_model(
    df: pd.DataFrame,
    factors: list[str],
    selected_terms: list[str],
    response_col: str = "Y"
) -> dict[str, Any]:
    """
    Ajusta la ecuación de regresión en variables codificadas:
    Y_hat = beta_0 + sum(beta_i * x_i) + sum(beta_ij * x_i * x_j)
    donde beta_0 = media_global y beta_k = Efecto_k / 2.
    """
    y = df[response_col].values
    grand_mean = float(np.mean(y))
    N = len(y)

    coefficients = {"Intercepto": grand_mean}
    pred = np.full(N, grand_mean)

    for term in selected_terms:
        # Extraer factores involucrados en el término
        # Por ejemplo: 'A' -> ['A'], 'AB' -> ['A', 'B']
        term_factors = [f for f in factors if f in term]
        sign_vector = np.ones(N)
        for f in term_factors:
            sign_vector *= df[f].values

        contrast = float(np.sum(sign_vector * y))
        effect = contrast / (2 ** (len(factors) - 1))
        beta = effect / 2.0
        coefficients[term] = beta
        pred += beta * sign_vector

    residuals = y - pred

    # Pruebas de supuestos
    # 1. Normalidad
    shapiro_stat, shapiro_p = stats.shapiro(residuals)

    # 2. Resumen
    return {
        "coefficients": coefficients,
        "fitted": pred,
        "residuals": residuals,
        "shapiro_stat": float(shapiro_stat),
        "shapiro_p": float(shapiro_p)
    }
