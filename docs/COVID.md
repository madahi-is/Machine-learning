# COVID — primera comparación reproducible

Notebook principal: `notebooks/02_covid.ipynb`. Se mantiene separado de `01_vinos.ipynb`.

## Elección del archivo y objetivo

Se inspeccionaron los seis CSV entregados. `covid_19_data.csv` reúne reportes por fecha/región de confirmados, muertes y recuperados; las series globales separan esas medidas y colocan fechas en columnas. Los archivos `_US` contienen detalle territorial de Estados Unidos. No son seis piezas que debamos unir obligatoriamente.

Se eligió `time_series_covid_19_confirmed.csv` para una primera tarea concreta: predecir los casos nuevos reportados mañana en Bolivia con los reportes disponibles hasta hoy. Bolivia es un alcance inicial de este trabajo, no una selección por rendimiento. Se conserva el CSV global completo y se selecciona su fila nacional en el notebook.

El archivo contiene 276 filas y 498 columnas, con 494 fechas entre 22/01/2020 y 29/05/2021. Para Bolivia hay una sola fila y no se encontraron conteos faltantes o descensos del acumulado. Province/State vacío no significa un caso faltante; las coordenadas no son necesarias para esta tarea.

## Preparación y evaluación

- Convertir fechas a filas y calcular diferencias de acumulados.
- Conservar ceros observados y picos; sin evidencia no se pueden reemplazar por la media o recortar como errores.
- Empezar desde el primer reporte positivo, 11/03/2020.
- Crear rezagos 0, 1, 2, 6, 7 y 13, medias retrospectivas de 7/14 días y calendario conocido de mañana.
- Quedan 431 observaciones supervisadas: 343 para entrenamiento, una de separación y 87 para prueba.
- Normalizar X con MinMax y estandarizar y dentro de cada entrenamiento; las predicciones se devuelven a unidades de casos mediante TransformedTargetRegressor.
- Validación temporal de cinco folds, gap=1. No se mezclan fechas aleatoriamente.
- Predicción de un día adelante: en test las entradas se actualizan con reportes observados hasta cada origen; el modelo no se reentrena. No es una predicción de los 87 días desde el primer día.

Se comparan Lineal/Ridge, Árbol/Random Forest y SVR lineal/RBF, además de persistencia y referencia semanal. Las configuraciones son iniciales, no optimizadas exhaustivamente. El notebook presenta código y comentarios para cada modelo, entrenamiento, validación y métricas finales.

## Resultados comprobados en esta ejecución

Prueba: fechas objetivo 04/03/2021–29/05/2021. Métricas calculadas sin redondear ni recortar las predicciones.

| Modelo | MAE validación temporal | MAE prueba | R² prueba |
| --- | ---: | ---: | ---: |
| Persistencia (mañana igual a hoy) | 204.32 | 747.77 | -0.5542 |
| Ridge | 216.22 | 568.05 | 0.1407 |
| SVR lineal | 217.94 | 609.52 | 0.0331 |
| Referencia semanal | 243.96 | 611.63 | -0.0540 |
| Lineal | 262.66 | 602.38 | 0.0192 |
| Random Forest | 340.20 | 607.97 | 0.0484 |
| Árbol | 358.29 | 663.04 | -0.2035 |
| SVR RBF | 398.36 | 663.41 | 0.0730 |

Ridge es el mejor algoritmo de los seis por MAE de validación. La mejor solución al incluir reglas sencillas es persistencia por ese mismo criterio. Ridge también tiene menor MAE en prueba, pero la elección previa no se cambia retrospectivamente mirando test.

El desempeño de prueba es débil. No corresponde declarar que el proyecto ya alcanzó un rendimiento aceptable o que Ridge sea el mejor modelo para cualquier dataset COVID. El gráfico muestra reportes cero intercalados con picos; pueden influir retrasos y cambios de reporte, pero este archivo no permite atribuirles una causa con certeza.

Se registran segundos de fit/predict. Son una medición orientativa en un equipo, no un benchmark repetido. La eficiencia computacional es distinta a la calidad predictiva.

## El requisito de 75%

Antes de declarar cumplimiento, consultar si se refiere a accuracy, precision, R² u otra definición. Accuracy y precision son métricas distintas de clasificación. R²=0.75 no es 75% de predicciones correctas y 1−MAPE no debe etiquetarse como accuracy.

Si el requisito fuera R² ≥ 0.75 en prueba, ninguno de estos seis modelos lo cumple. Si fuera accuracy, habría que definir una tarea de clasificación distinta y justificada. No cambiar el objetivo o los umbrales solo para alcanzar una cifra.

## Límites y siguiente mejora posible

La serie contiene reportes históricos y puede incorporar revisiones posteriores a cada fecha. No contamos con las versiones originales de cada día. Los datos son limitados y hay cambios de dinámica; las brechas train/validación pueden reflejar tanto sobreajuste como cambios temporales.

Una siguiente etapa razonable es examinar la calidad de los reportes y evaluar un objetivo semanal si corresponde al propósito académico. Otra es ajustar hiperparámetros mediante validación temporal dentro de entrenamiento. Como test ya se inspeccionó, no debe usarse repetidamente para elegir mejoras y luego presentarlo como confirmación independiente. Para eso harían falta nuevos datos reservados o un protocolo temporal externo.

## Añadir a tu repositorio

Extraer el ZIP en Descargas. Debe quedar `~/Descargas/covid-entrega/`. Desde la terminal:

```bash
cd ~/Documentos/Machine-learning
cp -a ~/Descargas/covid-entrega/notebooks/. notebooks/
cp -a ~/Descargas/covid-entrega/data/. data/
cp -a ~/Descargas/covid-entrega/docs/. docs/
git status
git add notebooks/02_covid.ipynb data/raw/time_series_covid_19_confirmed.csv docs/COVID.md
git commit -m "feat: agregar analisis temporal y modelos de covid"
git push
```

No se reemplaza ningún archivo de vinos. `docs/COVID.md` reemplaza la nota anterior que marcaba COVID como pendiente. No se incluye un README raíz para evitar sobrescribir tus cambios locales; puedes añadir en él un enlace a este documento.

El ZIP también contiene `results/covid_bolivia/` con esta ejecución de referencia; puedes consultarla directamente. El notebook regenera esas salidas al ejecutar y el .gitignore existente las excluye de Git.

Abrir `notebooks/02_covid.ipynb` en VS Code con el entorno ya usado para vinos, o [abrir en Colab después del push](https://colab.research.google.com/github/madahi-is/Machine-learning/blob/main/notebooks/02_covid.ipynb). Ejecutar en orden. Si la primera celda instala librerías, reiniciar cuando lo indique y volver a ejecutar. La verificación realizada aquí cubre todas las celdas de análisis y modelos; el acceso a GitHub y la instalación inicial requieren tu sesión.

## Procedencia

CSV suministrado por el equipo, conservado sin alterar. Completar el enlace de origen del comprimido y las condiciones de uso. Su formato es compatible con las series de Johns Hopkins; eso no verifica la procedencia exacta de esta copia.

Referencias: [TimeSeriesSplit](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html), [R²](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.r2_score.html), [documentación JHU](https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/README.md).
