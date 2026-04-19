# Guía de estudio — Notebook 1: Height (altura vs edad)

## Resumen del ejercicio

Se nos pide predecir la altura de un grupo de 21 alumnos a partir de su edad usando regresión lineal, pero **antes** debemos demostrar si la regresión lineal es una técnica adecuada para este problema haciendo un análisis descriptivo. Luego entrenamos el modelo, calculamos errores a mano y con sklearn, y sacamos conclusiones.

**Spoiler metodológico:** la regresión lineal **no funciona** aquí. La edad no explica la altura en adultos (el crecimiento ya ha terminado). El ejercicio está diseñado para que lo demostremos con datos.

---

## Celda 1 — Imports

```python
import pandas as pd                                  # manejo de DataFrames
import numpy as np                                   # cálculo numérico (errores manuales)
import matplotlib.pyplot as plt                      # gráficos base
import seaborn as sns                                # gráficos estadísticos más bonitos
from scipy import stats                              # test de correlación de Pearson con p-valor
sns.set_style('whitegrid')
```

**Qué hace cada import:**
- `pandas` (alias `pd`): para pasar la lista de tuplas a un DataFrame y poder trabajar con columnas con nombre.
- `numpy` (alias `np`): lo usaremos para calcular los errores a mano (medias, valores absolutos, raíz cuadrada).
- `matplotlib.pyplot` (alias `plt`): librería base de gráficos.
- `seaborn` (alias `sns`): encima de matplotlib, con gráficos estadísticos más bonitos por defecto.
- `scipy.stats`: la usamos para calcular la correlación de Pearson **con el p-valor**, cosa que pandas no nos da directamente.
- `sns.set_style('whitegrid')`: configura el estilo visual de todos los gráficos con fondo blanco y rejilla.

---

## Celda 2 — Los datos

```python
lista_alumnos = [("Leonardo S", 24, 1.82), ...]
```

Es una **lista de tuplas**. Cada tupla es `(nombre, edad, altura)`. 21 alumnos en total. No hay nada que ejecutar, solo que cargamos los datos en memoria.

---

## Celda 3 — Pasar los datos a DataFrame

```python
df = pd.DataFrame(lista_alumnos, columns=["nombre", "edad", "altura"])
df.head()
```

**Línea por línea:**
- `pd.DataFrame(...)`: constructor de DataFrame. Le pasamos dos cosas:
  - `lista_alumnos`: los datos (una lista de tuplas).
  - `columns=["nombre", "edad", "altura"]`: los nombres que queremos para las tres columnas. Sin esto, pandas nombraría las columnas 0, 1, 2.
- `df.head()`: muestra las **5 primeras filas**. Sirve para comprobar a ojo que la conversión ha ido bien.

**¿Por qué un DataFrame?** Porque sklearn acepta DataFrames directamente y porque manipular datos con nombre de columna es mucho más cómodo y legible que con índices numéricos.

---

## Celda 4 — Estadística descriptiva

```python
df.describe()
```

`describe()` es un método de pandas que, aplicado a un DataFrame, calcula automáticamente las estadísticas básicas de cada columna numérica:
- `count`: número de valores no nulos.
- `mean`: media aritmética.
- `std`: desviación típica (cuánto se separan los datos de la media en promedio).
- `min`, `max`: valores extremos.
- `25%`, `50%`, `75%`: primer cuartil, mediana y tercer cuartil.

**Lo que vemos aquí:**
- Edad: rango 23-45 años, media 32.
- Altura: rango 1,60-1,90 m, media 1,73 m, desviación típica 0,08 m (dispersión relativamente pequeña).

---

## Celda 5 — Correlación de Pearson

```python
r, p_valor = stats.pearsonr(df["edad"], df["altura"])
print(f"Coeficiente de Pearson (r): {r:.4f}")
print(f"P-valor: {p_valor:.4f}")
print(f"r² = {r**2:.4f}  →  la edad explica solo el {r**2*100:.2f}% de la variabilidad de la altura")
```

**Línea por línea:**
- `stats.pearsonr(df["edad"], df["altura"])`: calcula la correlación de Pearson entre dos columnas. Devuelve dos valores:
  - `r`: el coeficiente, entre -1 y 1.
    - 1 = correlación positiva perfecta (cuando sube X, sube Y).
    - -1 = correlación negativa perfecta.
    - 0 = sin correlación lineal.
  - `p_valor`: probabilidad de obtener esa correlación por azar si en realidad no hubiera relación. Si es < 0,05 se considera estadísticamente significativa.
- `f"...{r:.4f}..."`: **f-string** de Python. Formatea el número con 4 decimales.
- `r**2`: r al cuadrado. Es el **coeficiente de determinación** cuando solo hay una variable predictora: indica qué fracción de la varianza de Y explica X.

**Resultados obtenidos:**
- r = -0,3293 → correlación negativa débil.
- p-valor = 0,1450 → **NO es estadísticamente significativa** (está por encima de 0,05).
- r² = 0,108 → la edad solo "explicaría" el 10,8% de la variabilidad de la altura.

---

## Celda 6 — Scatter plot

```python
sns.scatterplot(data=df, x="edad", y="altura")
plt.title("Dispersión edad vs altura")
plt.show()
```

**Línea por línea:**
- `sns.scatterplot(...)`: dibuja un gráfico de dispersión.
  - `data=df`: le pasamos el DataFrame.
  - `x="edad"`: nombre de la columna para el eje X.
  - `y="altura"`: nombre de la columna para el eje Y.
- `plt.title(...)`: añade un título.
- `plt.show()`: renderiza el gráfico.

**Lo que debemos ver:** una nube de puntos dispersa, sin ninguna tendencia clara. Esto confirma visualmente la conclusión de la correlación.

---

## Conclusión del análisis descriptivo

Tres argumentos convergen:
1. **Correlación muy débil** (r = -0,33) y **no significativa** (p = 0,145).
2. **r² = 0,11** → la edad explicaría solo el 11% de la variabilidad.
3. **Nube de puntos sin tendencia** visible.

Además, biológicamente tiene sentido: la altura adulta no depende de la edad entre los 23 y los 45 años. **La regresión lineal NO es una buena técnica para este problema.** Aun así, entrenamos el modelo porque el enunciado lo pide y porque es didáctico ver qué pinta tiene un mal modelo.

---

## Celda 7 — Imports de sklearn

```python
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
```

- `LinearRegression`: la clase del modelo de regresión lineal de sklearn.
- `train_test_split`: función que divide datos en train y test de forma aleatoria.

---

## Celda 8 — Preparar X, y y split

```python
X = df[["edad"]]
y = df["altura"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"Train: {X_train.shape[0]} registros    Test: {X_test.shape[0]} registros")
```

**Punto CRÍTICO sobre corchetes:**
- `df[["edad"]]` con **doble corchete** → devuelve un **DataFrame (2D)**. Esto es lo que sklearn espera como X.
- `df["edad"]` con **un solo corchete** → devuelve una **Serie (1D)**. Esto es lo que sklearn espera como y.
- Si te confundes y pasas `df["edad"]` como X, sklearn te dará un error. Recuérdalo siempre.

**Sobre train_test_split:**
- `test_size=0.2` → el 20% de los datos van a test, el 80% a train. Con 21 filas: ~17 train, ~4 test (sklearn redondea, en nuestro caso salen 16 y 5).
- `random_state=42` → la división es aleatoria, pero fijamos la semilla para que siempre salga la misma. El número 42 es convencional (referencia a la Guía del Autoestopista Galáctico), pero vale cualquiera.

**Devuelve 4 cosas en ese orden:** X_train, X_test, y_train, y_test. El orden es importante, no lo confundas.

**Advertencia metodológica:** con solo 21 datos y test_size=0,2, nos quedamos con 5 puntos en test. Es extremadamente poco. Cualquier métrica que calculemos sobre ese test va a tener una varianza enorme. En un caso real, con tan pocos datos, sería mejor usar validación cruzada, pero aquí seguimos lo que pide el enunciado.

---

## Celda 9 — Entrenar el modelo

```python
modelo = LinearRegression()
modelo.fit(X_train, y_train)
print(f"Intercepto (a): {modelo.intercept_:.4f}")
print(f"Pendiente (b): {modelo.coef_[0]:.6f}")
print(f"Ecuación: altura = {modelo.intercept_:.4f} + ({modelo.coef_[0]:.6f}) * edad")
```

**Línea por línea:**
- `LinearRegression()`: crea una instancia del modelo vacía, todavía sin entrenar.
- `modelo.fit(X_train, y_train)`: entrena el modelo. Internamente, sklearn busca los valores de `a` (intercepto) y `b` (pendiente) que minimizan la suma de cuadrados de los errores. La fórmula que aprende es: `altura = a + b * edad`.
- `modelo.intercept_`: atributo que guarda el intercepto tras entrenar. El guión bajo al final es la convención de sklearn para atributos aprendidos.
- `modelo.coef_`: array con los coeficientes (pendientes) de cada feature. Como solo tenemos una feature (`edad`), accedemos al primero con `[0]`.

**Resultado obtenido:**
```
altura = 1.8581 + (-0.004357) * edad
```
La pendiente es **negativa**, lo que implicaría que cuanto mayor, más bajo. Biológicamente absurdo: es ruido estadístico producto de tener muy pocos datos.

---

## Celda 10 — Dibujar la recta

```python
sns.scatterplot(data=df, x="edad", y="altura", label="Datos reales")
edades_plot = pd.DataFrame({"edad": np.linspace(df["edad"].min(), df["edad"].max(), 100)})
alturas_plot = modelo.predict(edades_plot)
plt.plot(edades_plot, alturas_plot, color="red", label="Recta de regresión")
plt.title("Regresión lineal: altura vs edad")
plt.legend()
plt.show()
```

**Línea por línea:**
- Primero pintamos la nube de puntos como antes, pero añadimos `label="Datos reales"` para la leyenda.
- `np.linspace(min, max, 100)`: genera 100 puntos equiespaciados entre la edad mínima y la máxima. Necesitamos esto para dibujar la recta.
- Lo metemos en un DataFrame con el nombre de columna `"edad"` para que sklearn no nos suelte un warning.
- `modelo.predict(edades_plot)`: aplicamos el modelo sobre esos 100 puntos para obtener las alturas predichas.
- `plt.plot(..., color="red")`: dibujamos la recta en rojo encima del scatter.
- `plt.legend()`: muestra la leyenda con las etiquetas `label` que hemos definido.

---

## Celda 11 — Predicciones en test

```python
y_pred = modelo.predict(X_test)
comparacion = pd.DataFrame({"real": y_test.values, "predicho": y_pred})
comparacion["error"] = comparacion["real"] - comparacion["predicho"]
comparacion
```

- `modelo.predict(X_test)`: aplica el modelo al test y devuelve las alturas predichas.
- Construimos un DataFrame con columnas `real` (valores verdaderos) y `predicho` (lo que predice el modelo).
- `.values` convierte la Serie `y_test` a array de numpy; lo usamos para que pandas no intente alinear por índice (que en test está desordenado por el split aleatorio).
- Añadimos la columna `error = real - predicho`. Este es el **residuo** de cada punto: si es positivo, el modelo está subestimando; si es negativo, sobrestimando.

---

## Celda 12 — Errores manuales con numpy

```python
errores = y_test.values - y_pred
mae_manual = np.mean(np.abs(errores))
mse_manual = np.mean(errores ** 2)
rmse_manual = np.sqrt(mse_manual)
mape_manual = np.mean(np.abs(errores / y_test.values)) * 100
```

**Esto es el corazón del ejercicio: entender qué es cada métrica.**

- **MAE (Mean Absolute Error — Error Absoluto Medio):**
  ```
  MAE = media( |real - predicho| )
  ```
  - `np.abs(errores)`: pone todos los errores en positivo (si no lo hiciéramos, errores positivos y negativos se compensarían y la media saldría casi 0).
  - `np.mean(...)`: hace la media.
  - **Interpretación:** en promedio, nuestro modelo se equivoca en MAE unidades (metros en este caso). Fácil de entender.

- **MSE (Mean Squared Error — Error Cuadrático Medio):**
  ```
  MSE = media( (real - predicho)² )
  ```
  - `errores ** 2`: eleva al cuadrado cada error. Esto hace dos cosas: (1) convierte todo a positivo, (2) castiga los errores grandes más que los pequeños (un error de 2 pesa 4, uno de 4 pesa 16).
  - **Interpretación:** no tiene unidades interpretables directamente (metros al cuadrado en nuestro caso). Sirve sobre todo para comparar modelos.

- **RMSE (Root Mean Squared Error — Raíz del Error Cuadrático Medio):**
  ```
  RMSE = √MSE
  ```
  - `np.sqrt(mse_manual)`: raíz cuadrada.
  - **Interpretación:** es el MSE devuelto a las unidades originales (metros). Parecido al MAE pero penaliza más los errores grandes.

- **MAPE (Mean Absolute Percentage Error — Error Porcentual Absoluto Medio):**
  ```
  MAPE = media( |error / real| ) * 100
  ```
  - Divide cada error entre su valor real para tener el error en forma relativa.
  - Lo multiplicamos por 100 para expresarlo en porcentaje.
  - **Interpretación:** en promedio, nuestro modelo se equivoca en un MAPE% del valor real. Útil cuando los valores reales varían mucho en escala.
  - **Cuidado:** si algún valor real es 0 o muy pequeño, el MAPE se dispara o rompe.

---

## Celda 13 — Errores con sklearn

```python
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, mean_squared_error

mae_sklearn  = mean_absolute_error(y_test, y_pred)
mse_sklearn  = mean_squared_error(y_test, y_pred)
rmse_sklearn = np.sqrt(mse_sklearn)
mape_sklearn = mean_absolute_percentage_error(y_test, y_pred) * 100
```

Cada función de sklearn toma **dos argumentos: `(y_real, y_predicho)` en ese orden**. Si los inviertes, el MAE y el MSE salen iguales (por los valores absolutos y los cuadrados), pero el MAPE sale distinto porque divide por el primero.

Las cuatro métricas nos dan exactamente los mismos valores que los cálculos manuales. Esto es una comprobación de que hemos entendido bien cómo se calculan.

---

## Celda 14 — R² en test

```python
r2_test = modelo.score(X_test, y_test)
print(f"R² en test: {r2_test:.4f}")
```

- `modelo.score(X_test, y_test)`: devuelve el **coeficiente de determinación R²** del modelo sobre los datos que le pasemos.
- R² mide qué fracción de la varianza de y explica el modelo. Valores posibles:
  - **R² = 1** → modelo perfecto.
  - **R² = 0** → el modelo predice igual que si siempre respondiéramos "la media".
  - **R² < 0** → el modelo predice **peor** que la media. Es posible y significa que el modelo no sirve para nada.

**Resultado: R² = -1,04.** El modelo predice sustancialmente peor que si ignoráramos la edad y siempre respondiéramos la altura media. Confirmación empírica de que la regresión lineal no funciona aquí.

---

## Conclusión final del ejercicio

1. El análisis descriptivo ya indicaba que no había relación lineal: correlación débil, p-valor > 0,05, r² = 0,11.
2. Aun así entrenamos el modelo. Obtuvimos una recta con pendiente negativa (biológicamente absurda).
3. Las métricas de error en test (MAE ≈ 5,3 cm, MAPE ≈ 3%) pueden parecer razonables, pero engañan: el **R² negativo** revela que el modelo es **peor que predecir siempre la media**.
4. **Conclusión:** la regresión lineal no sirve para este problema. Para resolverlo mejor habría que incluir otras variables (sexo, genética, etnia...) o admitir que la altura no es predecible a partir de la sola edad en adultos.

Este ejercicio enseña dos lecciones importantes:
- **Antes de entrenar un modelo, haz análisis descriptivo para ver si tiene sentido.**
- **R² es la métrica reveladora**: MAE o RMSE bajos no garantizan que el modelo sea útil; R² sí te dice si es mejor que no hacer nada.
