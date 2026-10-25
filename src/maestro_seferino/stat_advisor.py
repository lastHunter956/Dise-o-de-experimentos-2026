"""
stat_advisor.py
---------------
Generador determinista del StatAdvisor (Asesor Estadístico) de Statgraphics Centurion.
Produce explicaciones narrativas y diagnósticos en lenguaje natural
para tablas ANOVA, diagramas de Pareto, gráficos de Cuthbert Daniel,
estructuras de alias en diseños fraccionados y optimización de respuestas.

100% local al proyecto maestro-seferino.
"""

from __future__ import annotations
import pandas as pd
import numpy as np

def advise_pareto(
    significant_terms: list[str],
    inactive_terms: list[str],
    alpha: float = 0.05,
    confidence: float = 95.0
) -> str:
    """Genera el texto interpretativo del StatAdvisor para el Diagrama de Pareto."""
    sig_str = ", ".join(significant_terms)
    inact_str = ", ".join(inactive_terms[:5]) + ("..." if len(inactive_terms) > 5 else "")
    
    advisor_text = (
        f"**El StatAdvisor:**\n"
        f"Este gráfico muestra cada uno de los efectos estandarizados ordenados por su magnitud "
        f"absoluta de mayor a menor. La línea vertical azul corresponde al umbral del estadístico "
        f"t de Student para un nivel de significancia $\\alpha = {alpha}$ (nivel de confianza del {confidence:.1f}%). "
        f"Cualquier barra que cruza esta línea divisoria se considera estadísticamente significativa.\n\n"
        f"- **Efectos Significativos detectados ({len(significant_terms)}):** {sig_str}. "
        f"Estos términos influyen de manera contundente sobre la variable Rendimiento.\n"
        f"- **Efectos No Significativos ({len(inactive_terms)}):** {inact_str}. "
        f"Estos términos caen por debajo del umbral crítico y su variación puede atribuirse al azar o ruido experimental."
    )
    return advisor_text

def advise_daniel(
    active_terms: list[str],
    positive_terms: list[str],
    negative_terms: list[str]
) -> str:
    """Genera el texto interpretativo del StatAdvisor para el Gráfico de Daniel."""
    pos_str = ", ".join(positive_terms) if positive_terms else "Ninguno"
    neg_str = ", ".join(negative_terms) if negative_terms else "Ninguno"
    
    advisor_text = (
        f"**El StatAdvisor:**\n"
        f"En el gráfico de probabilidad normal de efectos (Gráfico de Cuthbert Daniel, 1959), "
        f"los factores e interacciones que no tienen influencia real se alinean a lo largo de la "
        f"recta normal teórica central, demostrando que provienen de una distribución gaussiana "
        f"$\mathcal{{N}}(0, \\sigma^2)$ de error puro.\n\n"
        f"Por el contrario, los puntos que se apartan significativamente de la recta representan "
        f"efectos activos en el proceso industrial:\n"
        f"- **Efectos con impacto positivo ({len(positive_terms)}):** {pos_str} (al incrementar el factor de nivel bajo a alto, el rendimiento aumenta).\n"
        f"- **Efectos con impacto negativo ({len(negative_terms)}):** {neg_str}.\n"
        f"La clara separación entre la recta central de ruido y los términos activos confirma que "
        f"solo 4 efectos ({', '.join(active_terms)}) dominan el comportamiento del sistema litográfico."
    )
    return advisor_text

def advise_anova(
    anova_df: pd.DataFrame,
    r2: float,
    r2_adj: float,
    rmse: float,
    confidence: float = 95.0
) -> str:
    """Genera el texto interpretativo del StatAdvisor para la tabla ANOVA."""
    # Filtrar términos significativos
    sig_rows = anova_df[anova_df["Valor_p"] < 0.05]
    sig_names = [row["Termino"] for _, row in sig_rows.iterrows() if row["Termino"] not in ["Error residual", "Total (corregido)"]]
    
    advisor_text = (
        f"**El StatAdvisor:**\n"
        f"La tabla de Análisis de Varianza (ANOVA) descompone la variabilidad total observada en el "
        f"Rendimiento en contribuciones independientes asignadas a cada factor principal e interacción. "
        f"Dado que {len(sig_names)} efectos ({', '.join(sig_names)}) presentan valores-P inferiores a 0.05, "
        f"se concluye que tienen un efecto estadísticamente significativo sobre el Rendimiento con un nivel "
        f"de confianza del {confidence:.1f}%.\n\n"
        f"**Estadísticas de Bondad de Ajuste:**\n"
        f"- **R-Cuadrada ($R^2$):** Explica el **{r2 * 100:.2f}%** de la variabilidad observada en el experimento.\n"
        f"- **R-Cuadrada Ajustada ($R^2_{{\\text{{adj}}}}$):** Corrige por el número de coeficientes incluidos, situándose en **{r2_adj * 100:.2f}%**. "
        f"Este valor extraordinariamente alto indica que el modelo es parsimonioso y altamente predictivo.\n"
        f"- **Error Estándar del Estimado (RMSE):** {rmse:.4f}%, que representa la dispersión típica de los residuos experimentales."
    )
    return advisor_text

def advise_alias_structure(
    aliases: dict[str, str],
    resolution: str = "V"
) -> str:
    """Genera el texto interpretativo del StatAdvisor para la estructura de alias."""
    advisor_text = (
        f"**El StatAdvisor:**\n"
        f"El diseño factorial fraccionado implementado es de **Resolución {resolution}** ($2^{{5-1}}_{{\\text{{V}}}}$). "
        f"En este diseño:\n"
        f"1. **Ningún efecto principal está confundido (*aliased*) con interacciones de dos factores.** "
        f"Los efectos principales ($A, B, C, D, E$) únicamente se confunden con interacciones cuádruples ($BCDE, ACDE, \\dots$), "
        f"las cuales son físicamente insignificantes por el principio de escasez de efectos.\n"
        f"2. **Las interacciones de dos factores se confunden únicamente con interacciones de tres factores** "
        f"(por ejemplo, $AB \\pm CDE$).\n\n"
        f"Por lo tanto, la estimación de los efectos principales y de la interacción clave $AB$ es "
        f"completamente limpia y confiable, permitiendo obtener exactamente las mismas conclusiones que "
        f"con el diseño factorial completo de 32 corridas, pero utilizando únicamente la mitad de las corridas (16)."
    )
    return advisor_text

def advise_optimization(
    opt_levels: dict[str, str],
    pred_yield: float,
    current_mean: float
) -> str:
    """Genera el texto interpretativo del StatAdvisor para la optimización y predicción."""
    settings_str = ", ".join([f"{k} = {v}" for k, v in opt_levels.items()])
    diff = pred_yield - current_mean
    
    advisor_text = (
        f"**El StatAdvisor:**\n"
        f"El objetivo de este análisis es **Maximizar la variable Rendimiento (%)**. "
        f"El modelo ajustado predice que la condición óptima del proceso corresponde a:\n"
        f"**[{settings_str}]**.\n\n"
        f"- **Rendimiento Predicho en el Óptimo:** **{pred_yield:.2f}%**.\n"
        f"- **Ganancia Industrial Estimada:** Un incremento de **+{diff:.2f}%** respecto a la media "
        f"global base del proceso ({current_mean:.2f}%).\n\n"
        f"**Criterio Económico:** Los factores $D$ (Dimensión de máscara) y $E$ (Tiempo de grabado) "
        f"no mostraron influencia estadística detectable, por lo que se ajustan en su nivel Bajo ($-1.0$) "
        f"para reducir los costos de consumibles litográficos y minimizar el tiempo de ciclo en los reactores de plasma."
    )
    return advisor_text
