# COVID: pendiente

No hay archivo ni modelos COVID incluidos todavía. Al recibirlo debemos definir:

1. Qué representa una fila: paciente, país/día, hospital u otra unidad.
2. Qué variable queremos predecir y en qué momento se conoce cada predictor.
3. Si es regresión (cantidad) o clasificación (categoría).
4. Cómo interpretar nulos, códigos especiales, fechas, duplicados y acumulados.
5. Si dividir por tiempo, paciente o región para evitar fuga de información.

No aplicar automáticamente la limpieza de vinos a COVID. En datos temporales no se debe usar una división aleatoria para pronosticar el futuro. No utilizar variables posteriores al resultado que se quiere predecir. Para clasificación podrían compararse logística y logística regularizada, árbol y Random Forest, SVC lineal y RBF, con métricas adecuadas al desbalance. Si se exige dos familias distintas dentro de regresiones, consultar el alcance con la docente.

Antes de compartir datos de pacientes, revisar identificadores y permisos. El proyecto es académico, no una herramienta clínica.
