# Guía de estudio — Notebook 2: Diabetes

## Resumen del ejercicio

El dataset `load_diabetes` de sklearn contiene 442 pacientes con 10 mediciones fisiológicas (edad, sexo, BMI, presión arterial y 6 mediciones de suero sanguíneo) y una variable objetivo: la **progresión de la diabetes un año después**. El ejercicio pide:

1. Cargar y describir el dataset.
2. Responder preguntas sobre su estructura.
3. Entrenar un modelo de regresión lineal (¡ojo al split!).
4. Predecir, comparar con lo real y medir errores.
5. Iterar el modelo intentando mejorarlo (con StandardScaler o reduciendo features).

**Aviso metodológico clave del enunciado:** pide usar **los últimos 20 registros como test**. Esto es un **split por posición, NO un split aleatorio**. NO usamos `train_test_split`, usamos slicing (`[:-20]`, `[-20:]`).

---

## Celda 1 — Imports de visualización

```python
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_style('whitegrid')
```

Solo las librerías de gráficos. El estilo `whitegrid` pone fondo blanco y rejilla gris suave.

---

## Celda 2 — Cargar el dataset

```python
import pandas as pd
import numpy as np
from sklearn.datasets import load_diabetes
diabetes = load_diabetes()
```

- `load_diabetes()`: función de sklearn que devuelve un objeto **Bunch** (parecido a un diccionario) con los datos ya preparados. Los datasets de sklearn vienen limpios y listos para usar, sin necesidad de descargar CSVs.
- No devuelve un DataFrame, devuelve un diccionario con varias claves (las vemos en la siguiente celda).

---

## Celda 3 — Inspeccionar el objeto completo

```python
diabetes
```

Simplemente mostramos el objeto. Veremos un montón de claves y arrays de numpy. Útil para saber con qué estamos tratando pero poco legible.

---

## Celda 4 — Ver las claves

```python
diabetes.keys()
```

Nos muestra qué atributos tiene el Bunch:
- `data` → los valores de las 10 features (array 2D).
- `target` → la variable objetivo (array 1D).
- `DESCR` → descripción textual del dataset.
- `feature_names` → lista con los nombres de las 10 features.
- `frame`, `data_filename`, `target_filename`, `data_module` → metadatos menos relevantes para nosotros.

---

## Celda 5 — Imprimir la descripción

```python
print(diabetes['DESCR'])
```

- **Uso crítico de `print()`:** si haces simplemente `diabetes['DESCR']` te saldrá el texto con `\n` literales visibles en vez de saltos de línea. El `print()` interpreta los `\n` como saltos de línea reales. Esto está literalmente en la pista del enunciado.
- Leer esto es imprescindible para entender qué representa cada columna.

---

## Respuestas a las preguntas del enunciado

1. **¿Cuántos atributos hay? ¿Qué significan?** 10 features fisiológicas:
   - `age`: edad
   - `sex`: sexo
   - `bmi`: índice de masa corporal
   - `bp`: presión arterial media
   - `s1`: colesterol total (tc)
   - `s2`: lipoproteínas de baja densidad (ldl, "colesterol malo")
   - `s3`: lipoproteínas de alta densidad (hdl, "colesterol bueno")
   - `s4`: ratio colesterol total / HDL
   - `s5`: log de triglicéridos
   - `s6`: nivel de azúcar en sangre
   
   Todas ya vienen **escaladas**: centradas en media 0 y con la suma de cuadrados de cada columna igual a 1.

2. **Relación entre `data` y `target`:** `data` contiene las 10 variables predictoras (X) y `target` la variable a predecir (y, progresión de la diabetes al cabo de un año).

3. **¿Cuántos registros?** 442.

---

## Celda 6 — Verificar con código

```python
print(f"Número de features: {diabetes.data.shape[1]}")
print(f"Número de registros: {diabetes.data.shape[0]}")
print(f"Nombres de las features: {diabetes.feature_names}")
```

- `diabetes.data.shape` devuelve una tupla `(filas, columnas)`.
- `shape[0]` = número de filas (registros).
- `shape[1]` = número de columnas (features).

---

## Celda 7 — Shape de data y target

```python
print(f"Shape de data:   {diabetes.data.shape}")
print(f"Shape de target: {diabetes.target.shape}")
print("\nPrimeras 3 filas de data:")
print(diabetes.data[:3])
print(f"\nPrimeros 5 valores de target: {diabetes.target[:5]}")
print(f"Rango de target: min={diabetes.target.min()}, max={diabetes.target.max()}, mean={diabetes.target.mean():.2f}")
```

- `data` es 2D: (442, 10) → 442 registros × 10 features. Esto es lo que sklearn espera.
- `target` es 1D: (442,) → un valor de target por paciente.
- `diabetes.data[:3]` → slicing numpy, las 3 primeras filas.
- `target.min()`, `.max()`, `.mean()` → métodos de numpy para estadísticas rápidas.
- El target va de 25 a 346, con media ~152.

---

## Celda 8 — Importar linear_model

```python
from sklearn import linear_model
```

Importamos el **módulo** completo. Luego llamaremos a `linear_model.LinearRegression()`. (Alternativa equivalente: `from sklearn.linear_model import LinearRegression`.)

---

## Celda 9 — Crear la instancia del modelo

```python
diabetes_model = linear_model.LinearRegression()
```

Creamos una instancia vacía, sin entrenar todavía. Fíjate que usamos exactamente el nombre de variable que pide el enunciado: `diabetes_model`. Respetar los nombres del enunciado es importante para que el ejercicio pase cualquier corrección automática.

---

## Celda 10 — Split por POSICIÓN (⚠ importante)

```python
diabetes_data_train   = diabetes.data[:-20]
diabetes_target_train = diabetes.target[:-20]
diabetes_data_test    = diabetes.data[-20:]
diabetes_target_test  = diabetes.target[-20:]
```

**Esta celda es la trampa del ejercicio.** El enunciado dice "Use the last 20 records for the test data". Eso es un split **por posición**, NO un split aleatorio. Por tanto NO usamos `train_test_split`, usamos **slicing de numpy**:

- `data[:-20]` → "desde el principio hasta 20 antes del final" → 422 registros de train.
- `data[-20:]` → "desde 20 antes del final hasta el final" → 20 registros de test.

Esto es equivalente en Python estándar a `data[0:-20]` y `data[-20:len(data)]`.

**Advertencia metodológica:** un split por posición sólo tiene sentido si los datos están ordenados temporalmente (por ejemplo, un time series donde quieres predecir el futuro a partir del pasado) o si sabes que no hay orden en las filas. Con datos médicos aleatorios, **un split aleatorio sería más correcto estadísticamente**, pero el enunciado pide este split por posición y hay que respetarlo.

---

## Celda 11 — Descriptivo con DataFrame

```python
df = pd.DataFrame(diabetes.data, columns=diabetes.feature_names)
df['target'] = diabetes.target
df.describe()
```

- Convertimos `data` a DataFrame para poder usar `.describe()` y `.corr()` con comodidad.
- Le damos nombres de columnas con `columns=diabetes.feature_names`.
- Añadimos `target` como una columna más. Esto nos permite luego calcular la correlación de cada feature con el target.

---

## Celda 12 — Histograma del target

```python
sns.histplot(df['target'], kde=True)
plt.title("Distribución del target (progresión de diabetes a 1 año)")
plt.show()
```

- `sns.histplot(...)`: dibuja un histograma.
  - `kde=True` añade la curva de densidad por encima (una versión "suavizada" del histograma).
- Queremos ver si el target tiene una distribución razonable. Una de las asunciones de la regresión lineal es que los residuos sean aproximadamente normales; conviene ver primero si el target ya lo es. Si el target estuviera muy sesgado, podríamos transformarlo (log).

---

## Celda 13 — Heatmap de correlaciones

```python
plt.figure(figsize=(10, 8))
sns.heatmap(df.corr(), annot=True, cmap='coolwarm', fmt='.2f')
plt.title("Correlaciones entre features y target")
plt.show()
```

**Línea por línea:**
- `plt.figure(figsize=(10, 8))`: fijamos el tamaño del gráfico en pulgadas (ancho, alto).
- `df.corr()`: calcula la matriz de correlaciones de Pearson entre todas las columnas numéricas.
- `sns.heatmap(...)`: dibuja un mapa de calor:
  - `annot=True`: escribe los valores numéricos dentro de cada celda.
  - `cmap='coolwarm'`: paleta de colores del azul (negativo) al rojo (positivo) pasando por el blanco (cero).
  - `fmt='.2f'`: formato numérico con 2 decimales.

**Lo que vemos:**
- **Mejores predictores de target:** `bmi` (0,59), `s5` (0,57), `bp` (0,44).
- **Multicolinealidad fuerte:** `s1` y `s2` correlan 0,90 entre sí, `s3` y `s4` correlan -0,74. Esto significa que llevan información redundante.

---

## Celda 14 — Entrenar y ver coeficientes

```python
diabetes_model.fit(diabetes_data_train, diabetes_target_train)
print(f"Intercepto: {diabetes_model.intercept_:.4f}")
print(f"\nCoeficientes ({len(diabetes_model.coef_)} valores):")
for name, coef in zip(diabetes.feature_names, diabetes_model.coef_):
    print(f"  {name}: {coef:+.4f}")
```

- `.fit(X, y)`: entrena el modelo buscando la ecuación `target = intercepto + c₁·age + c₂·sex + ... + c₁₀·s6` que minimiza la suma de cuadrados de los errores.
- `.intercept_`: el término independiente.
- `.coef_`: array con los 10 coeficientes (uno por cada feature).
- `zip(names, coefs)`: empareja cada nombre con su coeficiente en un bucle. `zip` para cuando se agota la lista más corta.
- `:+.4f`: formato con signo (+ o -) y 4 decimales.

**Interpretación cuidadosa:** como las features ya vienen escaladas de origen, los coeficientes **más grandes en valor absoluto señalan las features más importantes**. Si no estuvieran escaladas, comparar coeficientes directamente sería incorrecto (por eso en el Notebook 1 de housing se usa StandardScaler antes de interpretar).

---

## Celda 15 — Predicciones

```python
predictions = diabetes_model.predict(diabetes_data_test)
predictions
```

Aplicamos el modelo entrenado a los 20 registros de test. Nos devuelve un array con 20 valores predichos.

---

## Celda 16 — Comparación real vs predicho

```python
comparacion = pd.DataFrame({
    "real":     diabetes_target_test,
    "predicho": predictions,
    "error":    diabetes_target_test - predictions
})
comparacion
```

Construimos un DataFrame con tres columnas. La resta `real - predicho` funciona elemento a elemento porque ambos son arrays de numpy del mismo tamaño.

---

## Celda 17 — Scatter real vs predicho

```python
plt.figure(figsize=(7, 7))
plt.scatter(diabetes_target_test, predictions)
min_val = min(diabetes_target_test.min(), predictions.min())
max_val = max(diabetes_target_test.max(), predictions.max())
plt.plot([min_val, max_val], [min_val, max_val], 'r--', label="Predicción perfecta")
plt.xlabel("Valor real")
plt.ylabel("Valor predicho")
plt.title("Real vs Predicho en test")
plt.legend()
plt.show()
```

- `plt.scatter(real, predicho)`: dibuja cada par (real, predicho) como un punto.
- Dibujamos además la **diagonal y=x** en rojo discontinuo. Esta diagonal representa la predicción perfecta: si un punto cae exactamente encima, el modelo acertó.
- Cuanto más dispersos estén los puntos respecto a la diagonal, peor predice el modelo.
- `'r--'`: atajo de matplotlib para "red, dashed" (rojo, discontinuo).

---

## Celda 18 — Métricas de error

```python
from sklearn.metrics import (mean_absolute_error, mean_absolute_percentage_error,
                             mean_squared_error, r2_score)

mae  = mean_absolute_error(diabetes_target_test, predictions)
mse  = mean_squared_error(diabetes_target_test, predictions)
rmse = np.sqrt(mse)
mape = mean_absolute_percentage_error(diabetes_target_test, predictions) * 100
r2   = r2_score(diabetes_target_test, predictions)
```

Las mismas métricas que en el Notebook 1 de Height:
- **MAE:** en promedio nos equivocamos en MAE unidades de target.
- **MSE:** error cuadrático medio (unidades al cuadrado).
- **RMSE:** raíz del MSE, de vuelta a las unidades originales del target.
- **MAPE:** error relativo en porcentaje.
- **R²:** fracción de la varianza explicada.

**Resultados obtenidos:**
- MAE = 36,6 → el modelo se equivoca en promedio en 36,6 unidades de target (sobre valores que rondan 150).
- RMSE = 44,8 → más alto que MAE porque hay algunos errores grandes.
- MAPE = 39,3% → en promedio nos equivocamos en un ~40% del valor real. **Es mucho.**
- R² = 0,585 → el modelo explica el 58,5% de la variabilidad del target en test. Bastante mejor que el del Height (R² negativo), pero lejos de ser un buen modelo clínico.

**Conclusión honesta:** el modelo captura algo de señal (R² = 0,58, no es despreciable), pero la precisión es baja. No sería usable para tomar decisiones clínicas. Esto está bien: es un ejercicio educativo sobre un dataset limitado a 10 variables fisiológicas básicas.

---

## Celdas 19, 20, 21 — Iteraciones del modelo

### Iteración A — StandardScaler

```python
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaler.fit(diabetes_data_train)
X_train_scaled = scaler.transform(diabetes_data_train)
X_test_scaled  = scaler.transform(diabetes_data_test)

model_scaled = linear_model.LinearRegression()
model_scaled.fit(X_train_scaled, diabetes_target_train)
predictions_scaled = model_scaled.predict(X_test_scaled)
```

**Punto metodológico esencial:**
- `scaler.fit(train)`: el scaler aprende la media y la desviación típica **solo con train**. Nunca le muestres el test al scaler en el `fit`, porque estarías "filtrando" información del test al train (data leakage).
- `scaler.transform(train)` y `scaler.transform(test)`: aplicamos la misma transformación aprendida a ambos.

**Resultado: mismo MAE, RMSE y R² que el modelo original.** Esto es teóricamente esperable: en una regresión lineal sin regularización, escalar las features no cambia las predicciones, solo cambia la **escala de los coeficientes**. El único valor añadido real es que los coeficientes del modelo escalado son ahora comparables entre sí (en unidades de desviación típica), lo que permite ver qué features son más importantes.

### Iteración B — Quitar s1 (multicolinealidad)

```python
idx_sin_s1 = [i for i, name in enumerate(diabetes.feature_names) if name != 's1']
X_train_B = diabetes_data_train[:, idx_sin_s1]
X_test_B  = diabetes_data_test[:,  idx_sin_s1]
```

- `enumerate(lista)`: devuelve pares `(índice, valor)`.
- **Comprensión de lista** `[i for i, name in ... if ...]`: recorre todos los pares y nos quedamos con los índices donde el nombre NO es 's1'.
- `data[:, idx_sin_s1]`: slicing de numpy. Los dos puntos `:` significan "todas las filas", `idx_sin_s1` selecciona esas columnas.

**Justificación:** s1 y s2 correlan 0,90, son casi la misma información. Quitar una reduce la multicolinealidad sin perder prácticamente señal.

**Resultado: R² sube de 0,585 a 0,589.** Mejora mínima, casi ruido, pero obtenida a cambio de un modelo más simple y estable.

### Iteración C — Solo 3 features

```python
idx_top3 = [diabetes.feature_names.index(name) for name in ['bmi', 'bp', 's5']]
X_train_C = diabetes_data_train[:, idx_top3]
X_test_C  = diabetes_data_test[:,  idx_top3]
```

- `lista.index(nombre)`: devuelve la posición del elemento en la lista.
- Seleccionamos solo las 3 features con mayor correlación con el target.

**Resultado: R² = 0,573.** Ligeramente inferior al original, pero con un modelo **radicalmente más simple** (3 features vs 10). En la práctica esto es muchas veces preferible (principio de parsimonia, menor riesgo de overfitting, más fácil de explicar a un médico).

---

## Tabla comparativa y conclusiones

| Modelo                  | MAE   | RMSE  | R²    |
|-------------------------|-------|-------|-------|
| Original (10 features)  | 36,61 | 44,77 | 0,585 |
| StandardScaler          | 36,61 | 44,77 | 0,585 |
| Sin s1 (9 features)     | 36,70 | 44,56 | 0,589 |
| Solo bmi + bp + s5      | 38,37 | 45,44 | 0,573 |

**Conclusiones metodológicas:**

1. **StandardScaler no mejora una regresión lineal simple.** Solo cambia la escala de los coeficientes para hacerlos comparables. Serviría con regularización (Ridge, Lasso).
2. **Quitar features correlacionadas** mejora marginalmente el modelo y aumenta su estabilidad. Es una buena práctica.
3. **Modelo parsimonioso** (3 features) sacrifica un poco de R² a cambio de simplicidad radical. En un entorno real hay que balancear precisión e interpretabilidad.
4. **⚠ Advertencia importante:** las diferencias entre modelos son muy pequeñas y el test es minúsculo (20 muestras). Con tan poco test, la varianza es enorme: no podemos concluir con seguridad que un modelo sea realmente mejor. Para una comparación rigurosa habría que usar **validación cruzada** (`cross_val_score`) sobre el conjunto completo, lo cual queda fuera del enunciado pero es lo que se haría en un proyecto real.
