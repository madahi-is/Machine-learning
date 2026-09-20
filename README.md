# Machine Learning: vinos y COVID

Proyecto académico reproducible, sin Google Drive. Estado: vinos implementado; COVID pendiente de recibir y revisar.

## Objetivo y modelos
En vinos se predice la puntuación `quality` usando las 11 variables fisicoquímicas. Es una primera formulación de regresión de una puntuación ordinal, no una clasificación. No se redondean las predicciones para medirlas.

| Área | Modelo 1 | Modelo 2 |
| --- | --- | --- |
| Regresiones | Regresión lineal múltiple | Ridge (regresión lineal regularizada) |
| Árboles | Árbol de decisión regresor | Random Forest regresor |
| SVM | SVR con kernel lineal | SVR con kernel RBF |

Se incluye DummyRegressor (media) como referencia. Ridge es una variante lineal y Random Forest un ensamble de árboles. Confirmar que la docente acepta estas variantes. La regresión logística, pese a su nombre, es un modelo de clasificación; no se mezcla directamente con regresión lineal para comparar la misma tarea.

## Ejecución en Colab (sin instalar Python en tu laptop)
1. Publica este proyecto siguiendo `docs/GITHUB.md`.
2. Abre https://colab.research.google.com/ y elige Archivo → Abrir notebook → GitHub.
3. Pega la URL del repositorio y abre `notebooks/01_vinos.ipynb`.
4. En la primera celda de código coloca la URL real del repositorio.
5. Ejecuta las celdas en orden. No se solicita acceso a Drive.

El CSV se descarga junto con el repositorio. Para el flujo simple se requiere un repositorio público; el acceso de Colab a repositorios privados requiere autenticación adicional. No pongas tokens en el notebook.

## Ejecución local (Python 3.11 o 3.12)
Desde la carpeta del proyecto en Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m src.vinos
```

Si falta el módulo venv en Linux Mint, instalar `python3-venv` con el gestor del sistema. El notebook local puede abrirse en Jupyter/VS Code; Jupyter no es necesario para ejecutar el script. En Windows, activar con `.venv\Scripts\activate`.

## Flujo metodológico
1. Conservar el CSV original y validar tipos, columnas, nulos y objetivo.
2. Quitar duplicados exactos: 1599 → 1359 filas, 240 duplicados, 0 nulos en el archivo entregado. Es una decisión del experimento: sin identificador no puede demostrarse que toda coincidencia sea un error. Evita colocar copias idénticas en train y test.
3. Separar 80% entrenamiento y 20% prueba con semilla 42. El objetivo no entra a la normalización.
4. Diagnosticar atípicos con IQR sobre entrenamiento. Por defecto se conservan; para experimentar con recorte usar `python -m src.vinos --cap-outliers`. No ejecutar ambas variantes para escoger según test.
5. Imputar mediana si aparecen nulos y normalizar con MinMaxScaler. Los parámetros se aprenden dentro de cada fold de entrenamiento mediante Pipeline. Los árboles no necesitan escalado, pero se incluye para mantener el flujo común.
6. Comparar los seis modelos con validación cruzada de 5 folds dentro del 80%. Elegir por menor MAE medio. Se reporta dispersión entre folds, no un intervalo de confianza.
7. Entrenar con todo el 80% y evaluar una sola vez sobre el 20% reservado. Se reporta test de todos los modelos para el trabajo, pero la elección ya se hizo con CV.

MinMax usa mínimos/máximos del entrenamiento. Un dato nuevo puede quedar fuera de [0,1]; no se debe reajustar el escalador con test. Los CSV normalizados exportados son del ajuste final; no usarlos como entrada a CV, porque introduciría información entre folds. Volver a ejecutar siempre desde el original.

## Métricas
- MAE: error absoluto promedio, en puntos de calidad; menor es mejor.
- RMSE: error que penaliza más los errores grandes; menor es mejor.
- R²: ajuste respecto a la variación del objetivo; mayor es mejor y puede ser negativo. No es porcentaje de aciertos.

Los hiperparámetros son una base inicial, no una búsqueda exhaustiva. Para una etapa posterior, usar GridSearchCV solo en entrenamiento y mantener test reservado. La partición aleatoria supone observaciones independientes; no hay identificadores de lote para comprobar agrupaciones.

## Archivos
- `data/raw/winequality-red.csv`: copia sin modificar del archivo suministrado.
- `src/vinos.py`: limpieza, normalización, modelos y evaluación compartidos.
- `notebooks/01_vinos.ipynb`: guía ejecutable en Colab o local.
- `results/vinos/`: salidas regenerables (ignoradas por Git).
- `docs/GITHUB.md`: publicación y colaboración.
- `docs/COVID.md`: decisiones pendientes.

Las salidas incluyen limpieza.json, diagnóstico IQR, particiones, datos sin duplicados, tablas CV/test, predicciones y matrices normalizadas. `results/ejecucion_verificada.txt` contiene la ejecución inicial comprobada con el CSV adjunto.

## Procedencia
Archivo aportado por el equipo: `winequality-red(1).csv`, renombrado para facilitar rutas. Antes de publicar, completar la referencia bibliográfica, URL de origen y condiciones de redistribución; no se ha verificado la procedencia exacta de esta copia. No se incluye una licencia para datos de terceros.

Referencias técnicas para estudiar: https://scikit-learn.org/stable/common_pitfalls.html y https://scikit-learn.org/stable/modules/model_evaluation.html .
