"""Experimento reproducible: ejecutar con python -m src.vinos desde la raíz."""
from pathlib import Path
import json
import platform
import numpy as np
import pandas as pd
import sklearn
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.dummy import DummyRegressor
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split, KFold, cross_validate
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

ROOT = Path(__file__).resolve().parents[1]
SEED = 42


class IQRClipper(TransformerMixin, BaseEstimator):
    """Recorte experimental: aprende límites SOLO en el conjunto de entrenamiento."""
    def fit(self, X, y=None):
        q1, q3 = np.nanpercentile(np.asarray(X), [25, 75], axis=0)
        self.lower_ = q1 - 1.5 * (q3 - q1)
        self.upper_ = q3 + 1.5 * (q3 - q1)
        return self

    def transform(self, X):
        return np.clip(np.asarray(X), self.lower_, self.upper_)


def load_clean():
    # El original se conserva intacto. No requiere Drive ni rutas personales.
    raw = pd.read_csv(ROOT / 'data/raw/winequality-red.csv', sep=None, engine='python')
    raw.columns = raw.columns.str.strip()
    if 'quality' not in raw or raw.shape[1] != 12:
        raise ValueError('Revisar encabezados y separador del archivo de vinos.')
    numeric = raw.apply(pd.to_numeric, errors='coerce').replace([np.inf, -np.inf], np.nan)
    invalid = raw.notna() & numeric.isna()
    if invalid.any().any():
        raise ValueError('Hay valores no numéricos o infinitos; revisar antes de continuar.')
    clean = numeric.drop_duplicates().dropna(subset=['quality'])
    if not clean.quality.between(0, 10).all():
        raise ValueError('quality fuera de la escala esperada 0–10.')
    report = {
        'filas_originales': len(raw), 'columnas': len(raw.columns),
        'duplicados_exactos': int(numeric.duplicated().sum()),
        'nulos_por_columna': numeric.isna().sum().to_dict(),
        'filas_sin_objetivo_tras_deduplicar': int(numeric.drop_duplicates().quality.isna().sum()),
        'filas_limpias': len(clean),
    }
    return clean, report


def build_models(cap_outliers=False):
    estimators = {
        'Referencia_media': ('Referencia', DummyRegressor()),
        'Lineal': ('Regresiones', LinearRegression()),
        'Ridge': ('Regresiones', Ridge(alpha=1.0)),
        'Arbol': ('Árboles', DecisionTreeRegressor(max_depth=5, min_samples_leaf=5, random_state=SEED)),
        'RandomForest': ('Árboles', RandomForestRegressor(n_estimators=200, min_samples_leaf=2, random_state=SEED, n_jobs=1)),
        'SVR_lineal': ('SVM', SVR(kernel='linear', C=1.0)),
        'SVR_RBF': ('SVM', SVR(kernel='rbf', C=10.0, gamma='scale')),
    }
    result = {}
    for name, (area, estimator) in estimators.items():
        steps = [('imputar', SimpleImputer(strategy='median'))]
        if cap_outliers:
            steps.append(('recortar', IQRClipper()))
        steps.extend([('normalizar', MinMaxScaler()), ('modelo', estimator)])
        result[name] = (area, Pipeline(steps))
    return result


def run(cap_outliers=False):
    clean, report = load_clean()
    X, y = clean.drop(columns='quality'), clean['quality']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=SEED)
    if X_train.isna().all().any():
        raise ValueError('Una variable está completamente vacía en entrenamiento.')
    out = ROOT / 'results' / ('vinos_iqr' if cap_outliers else 'vinos')
    out.mkdir(parents=True, exist_ok=True)
    clean.to_csv(out / 'datos_sin_duplicados.csv', index=False)
    report.update(entrenamiento=len(X_train), prueba=len(X_test), semilla=SEED,
                  recorte_iqr=cap_outliers, python=platform.python_version(),
                  pandas=pd.__version__, numpy=np.__version__, sklearn=sklearn.__version__)
    (out / 'limpieza.json').write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding='utf-8')
    # Diagnóstico IQR de entrenamiento: detectar no significa que sea un error.
    q1, q3 = X_train.quantile(.25), X_train.quantile(.75)
    low, high = q1 - 1.5*(q3-q1), q3 + 1.5*(q3-q1)
    pd.DataFrame({'limite_inferior': low, 'limite_superior': high,
                  'valores_atipicos_train': ((X_train < low) | (X_train > high)).sum()}).to_csv(out / 'outliers_train.csv')
    pd.DataFrame({'fila_original': clean.index, 'particion': [
        'train' if i in X_train.index else 'test' for i in clean.index
    ]}).to_csv(out / 'particiones.csv', index=False)
    cv = KFold(n_splits=5, shuffle=True, random_state=SEED)
    rows, fitted = [], {}
    for name, (area, pipeline) in build_models(cap_outliers).items():
        scores = cross_validate(pipeline, X_train, y_train, cv=cv,
            scoring={'mae': 'neg_mean_absolute_error', 'rmse': 'neg_root_mean_squared_error', 'r2': 'r2'})
        pipeline.fit(X_train, y_train)
        fitted[name] = pipeline
        rows.append({'modelo': name, 'area': area,
                     'MAE_CV': -scores['test_mae'].mean(), 'MAE_CV_std': scores['test_mae'].std(),
                     'RMSE_CV': -scores['test_rmse'].mean(), 'R2_CV': scores['test_r2'].mean()})
    comparison = pd.DataFrame(rows).sort_values('MAE_CV')
    # Elegir antes de consultar test. La referencia no compite como modelo del trabajo.
    selected = comparison.loc[comparison.area != 'Referencia', 'modelo'].iloc[0]
    comparison.to_csv(out / 'comparacion_cv.csv', index=False)
    test_rows, predictions = [], pd.DataFrame({'quality_real': y_test})
    for name, pipeline in fitted.items():
        pred = pipeline.predict(X_test)
        predictions[name] = pred
        test_rows.append({'modelo': name, 'MAE_test': mean_absolute_error(y_test, pred),
                          'RMSE_test': float(np.sqrt(mean_squared_error(y_test, pred))),
                          'R2_test': r2_score(y_test, pred), 'seleccionado_por_cv': name == selected})
    test = pd.DataFrame(test_rows)
    test.to_csv(out / 'comparacion_test.csv', index=False)
    predictions.to_csv(out / 'predicciones_test.csv', index_label='fila_original')
    pre = fitted[selected][:-1]
    for label, frame in [('train', X_train), ('test', X_test)]:
        pd.DataFrame(pre.transform(frame), index=frame.index, columns=X.columns).to_csv(
            out / f'X_{label}_normalizado.csv', index_label='fila_original')
    print('Modelo elegido por MAE de validación cruzada:', selected)
    print(comparison.round(4).to_string(index=False))
    print('\nEvaluación final (no usar para reajustar):\n', test.round(4).to_string(index=False))
    return comparison, test, report


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--cap-outliers', action='store_true', help='Experimento opcional de recorte IQR')
    run(parser.parse_args().cap_outliers)
