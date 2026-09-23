# Actualización: redes neuronales y gráficas

Esta entrega conserva los notebooks detallados de vinos y COVID, su limpieza, particiones y seis modelos anteriores. Añade un séptimo candidato: RNA_MLP. El material de clase (páginas 13–14) sirve como base conceptual para el perceptrón multicapa y la retropropagación.

## Cambios

- Vinos: 11 entradas, capas ocultas de 32 y 16 neuronas, salida continua de calidad.
- COVID: 10 entradas de historial/calendario, capas ocultas de 16 y 8 neuronas, salida continua de casos reportados mañana. No es una LSTM.
- Ambas: ReLU, Adam, regularización L2, semilla 42, objetivo estandarizado dentro del ajuste. Cada fold aprende de nuevo escaladores y pesos.
- Se conservan KFold para vinos y TimeSeriesSplit con gap para COVID. No hay validación interna aleatoria en la red.
- Gráficos individuales para los siete modelos y sus referencias: real frente a predicho, residuos; curvas temporales para COVID; pérdida por época de la red; comparación MAE train/validación y prueba.
- Recta condicional del modelo lineal: se varía una entrada y las demás quedan en la mediana de entrenamiento. No confundirla con la diagonal ideal y=x de los diagramas de predicción.
- Comentarios de código, explicación de hiperparámetros, métricas e interpretación en celdas separadas.

## Actualizar el proyecto en Visual Studio Code

1. Descomprime el ZIP. Copia `notebooks/01_vinos.ipynb` y `notebooks/02_covid.ipynb` a la carpeta `notebooks` de tu proyecto. Revisa tus modificaciones locales antes de reemplazarlos.
2. Copia `docs/REDES_Y_GRAFICAS.md` a `docs`. Si tu requirements.txt tiene otras dependencias, conserva esas líneas y agrega las versiones de esta entrega.
3. Los CSV incluidos son las copias usadas para verificar. Los notebooks esperan ambos en `data/raw/`. No requieren Drive.
4. Abre el notebook actualizado en VS Code, selecciona tu entorno Python y ejecuta las celdas de arriba abajo. Si la primera celda instala paquetes y pide reinicio, reinicia el kernel y vuelve a ejecutar.
5. Las figuras aparecen al ejecutar y se guardan como PNG en `results/vinos_detallado/graficas` y `results/covid_bolivia/graficas`. También se incluyen los PNG y CSV de nuestra comprobación, para poder verlos sin volver a entrenar.
6. Revisa los archivos antes de publicarlos:

```bash
git diff --stat
git status
git add notebooks/01_vinos.ipynb notebooks/02_covid.ipynb docs/REDES_Y_GRAFICAS.md requirements.txt
git commit -m "feat: agregar redes neuronales y graficas de evaluacion"
git push origin main
```

Si los CSV de datos aún no están en GitHub, añádelos también antes del commit. Los resultados pueden estar excluidos por .gitignore; no es necesario subirlos para ejecutar los notebooks.

## Ejecutar desde GitHub en Colab

Después de subir los cambios, abre cada notebook actualizado:

- https://colab.research.google.com/github/madahi-is/Machine-learning/blob/main/notebooks/01_vinos.ipynb
- https://colab.research.google.com/github/madahi-is/Machine-learning/blob/main/notebooks/02_covid.ipynb

Usa una sesión nueva si tu sesión anterior conserva una copia vieja del repositorio. Ejecuta todo en orden. No necesitas TensorFlow ni GPU.

## Qué se comprobó y límites

Se ejecutaron las celdas de análisis, preprocesamiento, entrenamiento, CV, predicción, métricas y gráficos con Python 3.12 y las versiones indicadas. Se verificaron conteos de modelos, separación de índices train/test y predicciones finitas. Las rectas condicionales añadidas se comprobaron por separado usando los mismos ajustes lineales. Se inspeccionaron figuras renderizadas. La instalación/clonación de la celda inicial y la interfaz de Colab/VS Code no se ejecutaron aquí. Los notebooks se entregan sin salidas incrustadas: sus resultados verificados están en results/ y en los registros de ejecución.

COVID emitió ConvergenceWarning: el límite de épocas se alcanzó en el ajuste final y en algunos folds. La advertencia se conserva; esta red es un candidato inicial, no una solución óptima. No se cambiaron hiperparámetros para perseguir mejores resultados de prueba.

El conjunto de prueba ya se observó en versiones anteriores: esta ampliación es exploratoria. Una evaluación independiente futura requiere nuevos datos no usados. R² no es accuracy; no se promete alcanzar 75% de aciertos en estas tareas de regresión.

Documentación de la implementación: https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPRegressor.html
