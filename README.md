# Machine Learning — vinos

Proyecto académico para estudiar limpieza, normalización y comparación de modelos. Primera etapa: dataset de vinos. COVID queda pendiente.

Repositorio: [madahi-is/Machine-learning](https://github.com/madahi-is/Machine-learning).

**Archivo principal:** [`notebooks/01_vinos.ipynb`](notebooks/01_vinos.ipynb). Es la versión detallada con comentarios, basada en `preprocesamientoDeDatos.ipynb`. El notebook contiene todo el análisis y no ejecuta `src/vinos.py`.

## 1. Ubicación de los archivos

| Archivo o carpeta | Función |
| --- | --- |
| `notebooks/01_vinos.ipynb` | Notebook que editamos y ejecutamos en VS Code o Colab. |
| `data/raw/winequality-red.csv` | Dataset original; se conserva sin modificar. |
| `requirements.txt` | Versiones de NumPy, pandas y scikit-learn del proyecto. |
| `results/vinos_detallado/` | CSV, métricas y gráfico generados por el notebook. |
| `src/vinos.py` | Script de la primera versión; es una ejecución alternativa. |
| `.gitignore` | Evita subir el entorno virtual y resultados regenerables. |

El notebook renombrado debe estar **dentro de `notebooks/`**, no en la raíz. Guardar ese archivo no sube automáticamente los cambios a GitHub.

## 2. Abrir el proyecto en Visual Studio Code

Si ya tienes el repositorio en tu laptop, abre una terminal y ejecuta:

```bash
cd ~/Documentos/Machine-learning
code .
```

Si `code` no está disponible como comando, abre Visual Studio Code y selecciona **Archivo → Abrir carpeta**, luego `Documentos/Machine-learning`.

Para un compañero que aún no tiene una copia, descargar una sola vez:

```bash
cd ~/Documentos
git clone https://github.com/madahi-is/Machine-learning.git
cd Machine-learning
code .
```

El repositorio público se puede clonar por HTTPS sin credenciales. Para subir cambios se necesita autenticación y permiso de escritura. Madahi ya utiliza el remoto SSH `git@github.com:madahi-is/Machine-learning.git`; no es necesario cambiarlo.

## 3. Preparar Python para ejecutar en tu computadora

Estas instrucciones son para Linux Mint. No se necesitan Podman, Docker ni montar Google Drive.

### Crear el entorno virtual una sola vez

Abre **Terminal → Nueva terminal** dentro de VS Code y ejecuta:

```bash
cd ~/Documentos/Machine-learning
python3 --version
python3 -m venv .venv
source .venv/bin/activate
```

Utiliza Python 3.11 o 3.12 para este flujo; la ejecución de análisis se comprobó con Python 3.12. Si tu equipo muestra otra versión, revisa compatibilidad antes de cambiar el Python del sistema.

Si la creación falla porque falta `venv`, instala el componente y repite la creación:

```bash
sudo apt install python3-venv
```

`.venv` mantiene las librerías del proyecto separadas de las del sistema. No se sube a GitHub.

### Instalar las dependencias

Con el entorno activado:

```bash
python -m pip install -r requirements.txt
python -m pip install matplotlib==3.10.8 seaborn==0.13.2 ipykernel
```

`requirements.txt` contiene las tres dependencias del script inicial. El segundo comando añade las librerías gráficas que usa el notebook detallado y el motor de Python para ejecutarlo en VS Code. La primera celda del notebook también comprueba las versiones de las cinco librerías de análisis.

Cada vez que abras una terminal nueva, activa el entorno existente; no necesitas recrearlo ni reinstalar todo:

```bash
cd ~/Documentos/Machine-learning
source .venv/bin/activate
```

## 4. Editar y ejecutar `01_vinos.ipynb` en VS Code

1. Instala las extensiones **Python** y **Jupyter**, publicadas por Microsoft.
2. Abre `notebooks/01_vinos.ipynb` desde el explorador.
3. En **Seleccionar kernel**, elige el entorno Python de `.venv`. Si no aparece, usa **Python: Select Interpreter** desde la paleta de comandos y selecciona `.venv/bin/python`; después vuelve al selector del notebook.
4. Edita las celdas de código o texto y guarda con **Ctrl+S**.
5. Ejecuta la primera celda de configuración y luego las demás en orden con ▶️. También puedes usar **Ejecutar todo / Run All**.
6. Si cambias una etapa anterior, reinicia el kernel y ejecuta todo desde el principio para no conservar variables antiguas.

Si el archivo aparece como JSON, usa **Reabrir editor con → Jupyter Notebook**. La documentación oficial explica el editor, la selección del kernel y la ejecución de celdas: [notebooks en VS Code](https://code.visualstudio.com/docs/datascience/jupyter-notebooks).

### Si la primera celda pide reiniciar

El mensaje `SystemExit: Paquetes instalados. Reinicia la sesión...` es una pausa intencional, no un fallo del modelo. Reinicia el kernel y ejecuta nuevamente desde la primera celda. Esto evita mezclar librerías cargadas en memoria con versiones recién instaladas.

Si reaparece `ImportError` en NumPy, comprueba primero que elegiste `.venv` y reinicia el kernel. Si persiste, conserva el mensaje completo y la salida de instalación para revisarlos; no cambies versiones al azar.

### Comprobar el entorno seleccionado

Puedes ejecutar temporalmente esta celda:

```python
import sys
print(sys.executable)
```

En tu laptop debe apuntar al Python de `Machine-learning/.venv/bin/python`. Activar `.venv` en la terminal no garantiza por sí solo que el notebook tenga seleccionado ese mismo kernel.

## 5. Qué hace el notebook

1. Lee el CSV desde el proyecto y muestra dimensiones, tipos, primeras filas y estadísticas.
2. Detecta y muestra duplicados, los elimina y verifica el resultado.
3. Revisa faltantes, tipos y valores fuera de la escala esperada del objetivo.
4. Diagnostica atípicos con IQR sin modificar aún los datos.
5. Guarda y vuelve a leer el CSV de limpieza inicial, sin Drive.
6. Divide 80% para entrenamiento y 20% para prueba con semilla 42.
7. Genera la correlación sobre entrenamiento.
8. Aplica imputación, capping IQR y normalización MinMax mediante pipelines.
9. Entrena seis modelos, compara entrenamiento y validación cruzada de cinco folds y elige por MAE de validación.
10. Evalúa sobre prueba y guarda resultados.

El CSV suministrado contiene 1599 filas, 12 columnas, 240 duplicados exactos y ningún nulo; quedan 1359 filas al deduplicar. Sin identificador de muestra no puede demostrarse que toda coincidencia sea un error: la deduplicación es una decisión documentada del experimento.

`data` conserva el original; `data_limpia` contiene la limpieza inicial; `data_modelado` es la copia releída. Los parámetros de imputación, IQR y MinMax se aprenden solo en entrenamiento, también dentro de cada fold. No se recorta ni escala `quality`. El diagnóstico global de atípicos no se reutiliza para ajustar los modelos.

`APLICAR_CAPPING = True` mantiene el recorte solicitado como decisión experimental; un valor extremo no necesariamente es un error. No elegir entre variantes mirando test.

## 6. Modelos y métricas

Se predice la puntuación numérica `quality` a partir de once características. Tratamos una puntuación ordinal como regresión; esta aproximación tiene límites y puede generar predicciones decimales.

| Área | Modelo 1 | Modelo 2 |
| --- | --- | --- |
| Regresiones | Lineal múltiple | Ridge, variante lineal regularizada |
| Árboles | Árbol de decisión regresor | Random Forest regresor |
| SVM | SVR lineal | SVR con kernel RBF |

Se añade una referencia que predice la media. Los parámetros son una base inicial; no se ha realizado una búsqueda exhaustiva. Confirmar con la docente que Ridge y Random Forest cumplen las variantes solicitadas.

- **MAE:** error absoluto promedio en puntos de calidad; menor es mejor.
- **MSE:** error cuadrático promedio; penaliza errores grandes.
- **RMSE:** raíz del MSE, en puntos de calidad; menor es mejor.
- **R²:** medida de ajuste; puede ser negativo y no representa porcentaje de aciertos.

No usamos accuracy para estas predicciones numéricas. Una brecha amplia entre entrenamiento y validación puede señalar sobreajuste; no basta una cifra aislada para diagnosticarlo. La desviación entre folds no es un intervalo de confianza.

El test ya se exploró en versiones anteriores del trabajo: no debe describirse como una confirmación completamente nueva e independiente. La división aleatoria supone observaciones independientes; no hay identificadores de lote para verificar posibles agrupaciones.

## 7. Guardar resultados

Al ejecutar todas las celdas se crea `results/vinos_detallado/` con:

- `winequality-red-limpio.csv`: datos sin duplicados, antes del capping y normalización.
- `comparacion_cv.csv` y `comparacion_test.csv`: métricas.
- `predicciones_test.csv`: calidad real y predicciones de los modelos.
- `correlacion_train.csv` y `correlacion_train.png`: correlación.
- `X_train_normalizado.csv` y `X_test_normalizado.csv`: entradas preparadas por el modelo seleccionado.
- `particiones.csv` y `resumen.json`: partición, configuración y versiones.

Los resultados generados están ignorados por Git; se regeneran ejecutando el notebook. En Colab son temporales y debes descargarlos si quieres conservar esa ejecución. No uses las matrices ya normalizadas como entrada a una nueva validación cruzada: vuelve a partir de datos sin transformar.

## 8. Subir tus cambios a GitHub

Después de editar y guardar en VS Code, revisa el estado desde la terminal del proyecto:

```bash
git status
git diff --stat
```

Si modificaste el notebook y este README:

```bash
git add notebooks/01_vinos.ipynb README.md
git diff --cached --stat
git commit -m "docs: actualizar notebook y guia de ejecucion"
git push
```

Añade explícitamente otros archivos solo si los modificaste. `git add` prepara cambios, `git commit` los guarda en el historial local y `git push` los envía a GitHub.

Si `git status` indica que no hay cambios, no necesitas crear un commit. Si `git push` es rechazado porque el remoto avanzó, guarda tus cambios en un commit y ejecuta `git pull --rebase`; resuelve cualquier conflicto antes de continuar. No fuerces el push para sobrescribir el trabajo del equipo.

Puedes limpiar las salidas del notebook antes de guardar para reducir diferencias y tamaño. Si el equipo necesita resultados visibles para la entrega, acuerden conservar una ejecución completa y coherente.

## 9. Recibir cambios del equipo

Antes de empezar una nueva sesión, con tus cambios anteriores ya guardados en un commit y el árbol de trabajo limpio:

```bash
cd ~/Documentos/Machine-learning
git status
git pull --ff-only
```

Este comando actualiza la rama actual si puede avanzar sin crear una mezcla de historiales. Si indica que las ramas divergieron, no elimina nada: revisa el estado antes de integrar. Si cambiaron dependencias, vuelve a instalar las indicadas y reinicia el kernel.

Para colaborar, cada persona puede crear una rama después de actualizar `main`:

```bash
git switch main
git pull --ff-only
git switch -c feature/analisis-vinos
```

Después de editar y ejecutar:

```bash
git add notebooks/01_vinos.ipynb
git commit -m "docs: mejorar explicacion del analisis de vinos"
git push -u origin feature/analisis-vinos
```

Abre un Pull Request hacia `main`. Eviten editar simultáneamente el mismo notebook: su formato JSON hace que los conflictos sean difíciles de resolver. Si aparece un conflicto, revisen ambos cambios antes de elegir; no acepten todo un lado sin comprobarlo.

## 10. Editar en VS Code y ejecutar en Colab

También puedes editar localmente sin ejecutar en tu laptop:

1. Edita `notebooks/01_vinos.ipynb` y guarda con Ctrl+S.
2. Haz `git add`, `git commit` y `git push` como en la sección 8.
3. Abre [01_vinos.ipynb en Colab](https://colab.research.google.com/github/madahi-is/Machine-learning/blob/main/notebooks/01_vinos.ipynb).
4. Comprueba que aparece el título **“Preprocesamiento de datos de vinos y modelos — versión detallada para GitHub”**.
5. Ejecuta las celdas en orden. Si se instalan versiones nuevas, reinicia cuando lo indique y vuelve a ejecutar.

Una pestaña de Colab abierta antes del push puede conservar la versión anterior. Guarda primero cualquier edición que necesites conservar, cierra esa pestaña y abre el enlace otra vez. La primera celda reutiliza una carpeta clonada si ya existe: no actualiza ese clon automáticamente. Para empezar con el código recién publicado, utiliza un entorno de ejecución nuevo.

Editar en Colab tampoco actualiza GitHub automáticamente. Para publicar desde Colab usa **Archivo → Guardar una copia en GitHub**, selecciona este repositorio y la ruta `notebooks/01_vinos.ipynb`. Después descarga ese cambio en tu laptop con `git pull --ff-only` antes de seguir editando localmente.

## 11. Script alternativo de la primera versión

El flujo principal documentado es el notebook. Si quieres ejecutar el script anterior desde la raíz del proyecto y con el entorno activado:

```bash
python -m src.vinos
```

Su recorte está desactivado por defecto y escribe en `results/vinos/`; por eso puede producir métricas diferentes a las del notebook. Para activar IQR en ese script:

```bash
python -m src.vinos --cap-outliers
```

Esa variante guarda en `results/vinos_iqr/`. El archivo `results/ejecucion_verificada.txt` corresponde a una ejecución inicial del script, no al notebook detallado actual.

## Procedencia y referencias

El equipo aportó el archivo `winequality-red(1).csv`, renombrado en el repositorio. Completar en el informe su URL de origen, referencia bibliográfica y condiciones de redistribución; no se ha verificado la procedencia exacta de esta copia.

- [Notebooks en Visual Studio Code](https://code.visualstudio.com/docs/datascience/jupyter-notebooks).
- [Preprocesamiento y fuga de información en scikit-learn](https://scikit-learn.org/stable/common_pitfalls.html).
- [Métricas de evaluación en scikit-learn](https://scikit-learn.org/stable/modules/model_evaluation.html).
