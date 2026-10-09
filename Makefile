.PHONY: help install sync kernel execute execute-p1 execute-p2 test lab clean all

# Variables del entorno y proyecto
UV = uv
PYTHON = $(UV) run python
JUPYTER = $(UV) run jupyter
NOTEBOOK_P1 = Taller_Factorial_Parte_1_Resuelto.ipynb
NOTEBOOK_P2 = Taller_Factorial_Parte_2_Resuelto.ipynb
NOTEBOOK_P4 = Taller_Factorial_2^2.ipynb
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


execute: execute-p1 execute-p2 execute-p4 ## Ejecuta los notebooks (Parte 1, Parte 2 y Actividad 4)

test: execute ## Alias para validar la ejecucion completa de los notebooks

lab: ## Inicia el servidor interactivo de Jupyter Lab con uv
	@echo "[INFO] Iniciando Jupyter Lab..."
	$(JUPYTER) lab

clean: ## Limpia archivos temporales y caches de ejecucion
	@echo "[INFO] Limpiando archivos temporales..."
	@rm -rf __pycache__ .ipynb_checkpoints .pytest_cache
	@echo "[OK] Limpieza terminada."

all: sync kernel execute ## Instala dependencias, registra el kernel y valida los notebooks
