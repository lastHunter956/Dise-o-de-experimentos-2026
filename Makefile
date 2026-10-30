.PHONY: help install sync kernel execute execute-p1 execute-p2 execute-p3 execute-p4 execute-p5 execute-integrador execute-statgraphics execute-actividad6 execute-actividad7 execute-taguchi statreport audit test lab clean all

# Variables del entorno y proyecto
UV = uv
PYTHON = $(UV) run python
JUPYTER = $(UV) run jupyter
NOTEBOOK_P1 = Taller_Factorial_Parte_1_Resuelto.ipynb
NOTEBOOK_P2 = Taller_Factorial_Parte_2_Resuelto.ipynb
NOTEBOOK_P4 = Taller_Factorial_2^2.ipynb
NOTEBOOK_P5 = Taller_Factorial_2^5.ipynb
NOTEBOOK_INTEGRADOR = Experimento_2_5_Semiconductores_Integrador.ipynb
NOTEBOOK_STATGRAPHICS = Taller_Statgraphics_DOE_Integrador.ipynb
NOTEBOOK_ACTIVIDAD6 = Taller_Factorial_Fraccionado_2_7-4_Vibracion_Resuelto.ipynb
NOTEBOOK_ACTIVIDAD7 = Taller_Factorial_2_5_y_Fraccionados_Resuelto.ipynb
NOTEBOOK_TAGUCHI = Taller_Taguchi_L16_Lechadas_Cemento_Resuelto.ipynb
KERNEL_NAME = maestro-seferino
KERNEL_DISPLAY = Python (maestro-seferino - uv)

help: ## Muestra la lista de comandos disponibles y su descripcion
	@echo "=========================================================================="
	@echo " Makefile - Talleres Factoriales Parte 1 y 2 con uv, Jupyter y VS Code   "
	@echo "=========================================================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  make %-14s %s\n", $$1, $$2}'

install: sync ## Sincroniza e instala las dependencias del proyecto con uv

sync: ## Sincroniza el entorno virtual aislado (.venv) con uv.lock
	@echo "[INFO] Sincronizando entorno virtual con uv..."
	$(UV) sync

kernel: sync ## Crea y registra el kernel Jupyter para Visual Studio Code
	@echo "[INFO] Registrando kernelspec '$(KERNEL_NAME)'..."
	$(PYTHON) -m ipykernel install --user --name $(KERNEL_NAME) --display-name "$(KERNEL_DISPLAY)"
	@mkdir -p .vscode
	@printf '{\n  "python.defaultInterpreterPath": "$${workspaceFolder}/.venv/bin/python",\n  "jupyter.selectedKernel": "$(KERNEL_NAME)"\n}\n' > .vscode/settings.json
	@echo "[OK] Kernel registrado y configurado para VS Code."

execute-p1: ## Ejecuta el notebook de la Parte 1 de forma no interactiva
	@echo "[INFO] Ejecutando $(NOTEBOOK_P1)..."
	$(JUPYTER) nbconvert --to notebook --execute \
		--ExecutePreprocessor.timeout=300 \
		--output $(NOTEBOOK_P1) \
		$(NOTEBOOK_P1)
	@echo "[OK] Parte 1 ejecutada exitosamente."

execute-p2: ## Ejecuta el notebook de la Parte 2 de forma no interactiva
	@echo "[INFO] Ejecutando $(NOTEBOOK_P2)..."
	$(JUPYTER) nbconvert --to notebook --execute \
		--ExecutePreprocessor.timeout=300 \
		--output $(NOTEBOOK_P2) \
		$(NOTEBOOK_P2)
	@echo "[OK] Parte 2 ejecutada exitosamente."

execute-p3: execute-p4 ## Alias para ejecutar Taller_Factorial_2^2

execute-p4: ## Ejecuta el notebook de la Actividad 4 (2^2) de forma no interactiva
	@echo "[INFO] Ejecutando $(NOTEBOOK_P4)..."
	$(JUPYTER) nbconvert --to notebook --execute \
		--ExecutePreprocessor.timeout=300 \
		--output $(NOTEBOOK_P4) \
		$(NOTEBOOK_P4)
	@echo "[OK] Actividad 4 ejecutada exitosamente."

execute-p5: ## Ejecuta el notebook de la Actividad 5 (2^5) de forma no interactiva
	@echo "[INFO] Ejecutando $(NOTEBOOK_P5)..."
	$(JUPYTER) nbconvert --to notebook --execute \
		--ExecutePreprocessor.timeout=300 \
		--output $(NOTEBOOK_P5) \
		$(NOTEBOOK_P5)
	@echo "[OK] Actividad 5 ejecutada exitosamente."

execute-integrador: ## Ejecuta el nuevo notebook integrador del Experimento 2^5
	@echo "[INFO] Ejecutando $(NOTEBOOK_INTEGRADOR)..."
	$(JUPYTER) nbconvert --to notebook --execute \
		--ExecutePreprocessor.timeout=300 \
		--output $(NOTEBOOK_INTEGRADOR) \
		$(NOTEBOOK_INTEGRADOR)
	@echo "[OK] Notebook Integrador 2^5 ejecutado exitosamente."

execute-statgraphics: ## Ejecuta el notebook de Statgraphics DOE (3 partes / 8 pasos)
	@echo "[INFO] Ejecutando $(NOTEBOOK_STATGRAPHICS)..."
	$(JUPYTER) nbconvert --to notebook --execute \
		--ExecutePreprocessor.timeout=300 \
		--output $(NOTEBOOK_STATGRAPHICS) \
		$(NOTEBOOK_STATGRAPHICS)
	@echo "[OK] Notebook Statgraphics DOE ejecutado exitosamente."

execute-actividad6: ## Ejecuta el notebook de la Actividad 6 (2^(7-4) Fraccionado Saturado)
	@echo "[INFO] Ejecutando $(NOTEBOOK_ACTIVIDAD6)..."
	UV_CACHE_DIR=/tmp/uv_cache $(JUPYTER) nbconvert --to notebook --execute \
		--ExecutePreprocessor.timeout=300 \
		--output $(NOTEBOOK_ACTIVIDAD6) \
		$(NOTEBOOK_ACTIVIDAD6)
	@echo "[OK] Actividad 6 ejecutada exitosamente."

execute-actividad7: ## Ejecuta el notebook de la Actividad 7 (2^5 y Fraccionados)
	@echo "[INFO] Ejecutando $(NOTEBOOK_ACTIVIDAD7)..."
	$(JUPYTER) nbconvert --to notebook --execute \
		--ExecutePreprocessor.timeout=300 \
		--output $(NOTEBOOK_ACTIVIDAD7) \
		$(NOTEBOOK_ACTIVIDAD7)
	@echo "[OK] Actividad 7 ejecutada exitosamente."

execute-taguchi: ## Ejecuta el notebook de Diseño Robusto Taguchi L16 (Lechadas de Cemento)
	@echo "[INFO] Ejecutando $(NOTEBOOK_TAGUCHI)..."
	$(JUPYTER) nbconvert --to notebook --execute \
		--ExecutePreprocessor.timeout=300 \
		--output $(NOTEBOOK_TAGUCHI) \
		$(NOTEBOOK_TAGUCHI)
	@echo "[OK] Taller Taguchi L16 ejecutado exitosamente."

statreport: ## Compila el documento StatReport oficial de Statgraphics en HTML
	@echo "[INFO] Compilando StatReport_Actividad_DOE_Semiconductores.html..."
	UV_CACHE_DIR=/tmp/uv_cache $(UV) run python -m maestro_seferino.stat_reporter
	@echo "[OK] StatReport generado exitosamente."

audit: ## Ejecuta la auditoria determinista de respuestas contra ground truth
	@echo "[INFO] Ejecutando auditoría determinista de respuestas..."
	python3 .agents/scripts/audit_2k_results.py
	python3 .agents/scripts/audit_actividad6.py
	python3 .agents/scripts/audit_actividad7.py
	python3 .agents/scripts/audit_taguchi_l16.py

execute: execute-p1 execute-p2 execute-p4 execute-p5 execute-integrador execute-statgraphics audit ## Ejecuta todos los notebooks y valida la auditoria

test: execute ## Alias para validar la ejecucion completa de los notebooks

lab: ## Inicia el servidor interactivo de Jupyter Lab con uv
	@echo "[INFO] Iniciando Jupyter Lab..."
	$(JUPYTER) lab

clean: ## Limpia archivos temporales y caches de ejecucion
	@echo "[INFO] Limpiando archivos temporales..."
	@rm -rf __pycache__ .ipynb_checkpoints .pytest_cache
	@echo "[OK] Limpieza terminada."

all: sync kernel execute ## Instala dependencias, registra el kernel y valida los notebooks
