# Talleres de Diseno de Experimentos (DOE): Factoriales (Parte 1, Parte 2 y Actividad 4)

---

## 1. Archivos Entregables

- **`Taller_Factorial_Parte_1_Resuelto.ipynb`**: Notebook Jupyter de la Parte 1 (29 celdas, 13 figuras pre-renderizadas en `dark_background`).
- **`Taller_Factorial_Parte_2_Resuelto.ipynb`**: Notebook Jupyter de la Parte 2 (22 celdas, 9 figuras pre-renderizadas en `dark_background`).
- **`Taller_Factorial_2^2.ipynb`**: Mega Notebook Integrador del Capítulo 6 (Incluye 5 casos prácticos: $2^2$, $2^3$, $2^5$, Puntos Centrales y Bloques).
- **`Makefile`**: Automatizacion determinista con `uv` para instalacion, registro de kernel y pruebas.

---

## 2. Automatizacion Rapida con `make` y `uv`

El proyecto esta completamente gestionado con `uv`. Se proveen comandos directos en el `Makefile`:

```bash
make help        # Muestra la lista de comandos disponibles
make install     # Sincroniza e instala las dependencias en .venv
make kernel      # Registra el kernel de Jupyter para VS Code
make execute-p1  # Valida y ejecuta el notebook de la Parte 1
make execute-p2  # Valida y ejecuta el notebook de la Parte 2
make execute-p3  # Valida y ejecuta el notebook integrador del Taller_Factorial_2^2
make execute     # Ejecuta los notebooks secuencialmente
make test        # Alias para ejecucion y validacion de pruebas
make lab         # Abre Jupyter Lab con el entorno uv
make all         # Ejecuta install + kernel + execute en un solo paso
```

---

## 3. Ejecucion en Visual Studio Code (VS Code)

El kernel Jupyter `Python (maestro-seferino - uv)` (id: `maestro-seferino`) esta registrado globalmente y vinculado al entorno `.venv`:

1. Abra esta carpeta en VS Code (`code .`).
2. Abra cualquiera de los dos notebooks:
   - `Taller_Factorial_Parte_1_Resuelto.ipynb`
   - `Taller_Factorial_Parte_2_Resuelto.ipynb`
3. En la esquina superior derecha, verifique que el kernel activo sea:
   **`Python (maestro-seferino - uv)`**
4. Ejecute cualquier celda individualmente con `Shift + Enter` o todo el notebook con **Run All**.

---

## 4. Apertura y Ejecucion en Google Colab

Ambos notebooks son 100% compatibles con Google Colab y utilizan exclusivamente librerias estandar (`numpy`, `pandas`, `scipy`, `statsmodels`, `matplotlib`, `seaborn`):

1. Ingrese a [Google Colab](https://colab.research.google.com).
2. Seleccione **Subir** (Upload) y arrastre el notebook deseado (`Parte 1` o `Parte 2`).
3. Vaya a **Entorno de ejecucion** -> **Ejecutar todas**.
