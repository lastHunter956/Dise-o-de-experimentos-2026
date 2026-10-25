"""
maestro_seferino
----------------
Paquete de computación estadística para Diseño y Análisis de Experimentos (DOE).
Alineado con las metodologías de Maestro Seferino, Gutiérrez & De la Vara,
y emulador completo de Statgraphics (DOE, StatAdvisor y StatReporter).
"""

from .doe_engine import (
    build_2k_design,
    compute_factorial_effects,
    build_preliminary_anova,
    build_best_anova,
    fit_coded_model
)

from .statgraphics_doe import (
    get_dataset,
    compute_alias_structure_2_5_1,
    analyze_statgraphics_design,
    build_statgraphics_anova
)

from .stat_advisor import (
    advise_pareto,
    advise_daniel,
    advise_anova,
    advise_alias_structure,
    advise_optimization
)

from .stat_reporter import (
    build_full_statreport
)

__all__ = [
    "build_2k_design",
    "compute_factorial_effects",
    "build_preliminary_anova",
    "build_best_anova",
    "fit_coded_model",
    "get_dataset",
    "compute_alias_structure_2_5_1",
    "analyze_statgraphics_design",
    "build_statgraphics_anova",
    "advise_pareto",
    "advise_daniel",
    "advise_anova",
    "advise_alias_structure",
    "advise_optimization",
    "build_full_statreport"
]
