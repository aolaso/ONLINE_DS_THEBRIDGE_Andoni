# GUIÓN DE PRESENTACIÓN - 16 de abril 2026
## ¿Cuánto vale tu trabajo?
### Estructura: 5 slides (5 min) + web en directo (10 min) + 5 slides (5 min)

---

## ANTES DE EMPEZAR (checklist)

- [ ] Web abierta en otra pestaña (cuantovaletutrabajo.lovable.app)
- [ ] Comprobar que la web carga bien con internet del aula
- [ ] Presentación PPTX en modo pantalla completa
- [ ] Notebook abierto por si preguntan algo técnico
- [ ] Leer este guión una vez más en voz alta

---

## FASE 1: SLIDES (5 minutos)

### SLIDE 1: Título (30 seg)
> "¿Cuánto vale tu trabajo? Esa es la pregunta que he intentado responder. No con opiniones ni titulares, sino con los datos oficiales de Eurostat, que es la oficina de estadística de la Unión Europea. Los mismos datos que usan los gobiernos para tomar decisiones."

(No leas nada de la pantalla. Deja que la tipografía hable sola y pasa.)

---

### SLIDE 2: ¿De qué va? (1 min)
> "He analizado datos de 38 países europeos. No solo la UE, sino también vecinos como Noruega, Turquía o Reino Unido. ¿Por qué? Porque si solo miro los 27 de la UE, no puedo saber si el proyecto europeo protege mejor a los trabajadores que los países de fuera.

> Son 8 bases de datos diferentes de Eurostat: salarios, vivienda, inflación, pobreza, brecha de género. En total, más de mil filas de datos que van desde 1999 hasta 2026. Cinco de esos datasets los descargué a mano desde la web de Eurostat, y tres los obtuve por API, que es cuando le pides los datos directamente al servidor de Eurostat desde Python.

> Y todo esto tiene un foco muy concreto: el debate sobre los 1.500 euros de salario mínimo en el País Vasco y en España. ¿Es mucho? ¿Es poco? Solo tiene sentido responder a eso si lo comparas con lo que pasa en el resto de Europa."

---

### SLIDE 3: Las 5 preguntas (1 min)
> "He planteado 5 preguntas concretas, 5 hipótesis, que son afirmaciones que puedo comprobar mirando los datos.

> La primera: ¿1.000 euros compran lo mismo en Dublín que en Bucarest? Spoiler: no, ni de lejos. Y eso tiene consecuencias enormes cuando comparamos salarios entre países.

> La segunda: si un gobierno sube el salario mínimo, ¿se reduce la brecha salarial entre hombres y mujeres? Las mujeres están sobrerrepresentadas en los empleos peor pagados, así que en teoría debería ayudar.

> La tercera es la que más duele: ¿la vivienda sube más rápido que el sueldo? Porque de nada sirve cobrar más si el alquiler se come la subida.

> La cuarta: ¿tener trabajo garantiza no ser pobre? Casi 1 de cada 10 trabajadores europeos dice que no.

> Y la quinta: ¿la generación Z vive peor que sus padres? Los datos aquí me sorprendieron, como veréis."

---

### SLIDE 4: ¿Cómo lo he hecho? (1.5 min)
> "Antes de ver los resultados, un minuto sobre el método. Lo he dividido en tres fases.

> Primero, recoger los datos. Todo viene de Eurostat, fuentes públicas y oficiales.

> Segundo, limpiar. Esta es la parte que no se ve pero que lleva el 80% del tiempo. Los datos de Eurostat no vienen listos: hay columnas pegadas que hay que separar, hay códigos raros que significan 'dato no disponible', hay datasets que tienen 9 filas donde debería haber 1. Si la limpieza está mal, el análisis está mal.

> Y tercero, analizar. Para cada pregunta hago un gráfico para VER el patrón y un test estadístico para MEDIR si ese patrón es real o casualidad. El test que uso se llama Pearson. Me da un número entre -1 y +1 que dice cómo de fuerte es la relación entre dos variables. Y un p-value: si es menor que 0.05, el resultado es fiable."

---

### SLIDE 5: Vamos a la web (30 seg)
> "Ahora vamos a explorar los datos en directo. He construido una web donde podéis ver los gráficos, los datos y los resultados de cada hipótesis."

(Abre la pestaña con la web.)

---

## FASE 2: WEB EN DIRECTO (10 minutos)

### Orden: Mapa → H1 → H3 → H4 → H5 → País Vasco

---

### MAPA (1 min)
> "Esto es el mapa de Europa coloreado por salario mínimo en PPS, que es la moneda que mide el poder adquisitivo real. Cuanto más oscuro el verde, más puedes comprar con tu salario mínimo.

> Fijaos en algo: Alemania es más oscuro que Irlanda. Pero Irlanda cobra más en euros. ¿Cómo es posible? Porque Irlanda es carísima. Cuando ajustas por lo que cuesta la vida allí, el salario mínimo irlandés rinde menos que el alemán."

---

### H1: El salario nominal engaña (2 min)
> "Cada punto del scatter es un país. Eje horizontal: lo que cobras en euros. Eje vertical: lo que realmente puedes comprar. Si fueran iguales, todos estarían en la diagonal.

> Mirad: Rumanía está por encima. Cobra 703 euros, pero equivale a 1.105 en poder de compra. Irlanda cobra 2.146 euros pero equivale a solo 1.554. El coste de vida se come 600 euros.

> (Lollipop chart) Cada línea muestra la distancia entre lo que cobras y lo que puedes comprar. Rumanía gana un 61%. Irlanda pierde un 28%. España está casi en el centro, +10%.

> 21 de 27 países cambian de posición en el ranking cuando pasamos de euros a poder adquisitivo. Comparar salarios en euros es engañoso."

---

### H3: Vivienda (2.5 min)
> "Aquí hay un truco interesante. El test de Pearson NO sale significativo: r = 0,044. Pero la hipótesis SÍ se valida.

> Pearson me respondía a una pregunta que yo no hacía. Pearson mide si los países con más salario tienen vivienda más cara. Pero mi pregunta es: ¿cuál CRECE más rápido? Y para eso comparo velocidades.

> (Barras) Verde: cuánto ha subido el salario. Rojo: cuánto ha subido la vivienda. Portugal: salario +61%, vivienda +124%. En 8 de 10 países, la vivienda gana la carrera. Solo España y Rumanía son excepciones.

> La herramienta correcta depende de la pregunta. No todo se mide con correlación."

---

### H4: Working poor (2 min)
> "Casi 1 de cada 10 trabajadores europeos es pobre a pesar de tener empleo. El 8,6%.

> Dato sorprendente: Luxemburgo. Salario mínimo más alto de Europa, pero pobreza laboral del 13,5%. El coste de vida se come el salario.

> Y otro hallazgo: desempleo y pobreza laboral NO son el mismo problema. La correlación entre ellos es solo 0,287. Crear empleo no resuelve la pobreza automáticamente. Importa QUÉ trabajo."

---

### H5: Gen Z (1.5 min)
> "Los datos me corrigieron. En 27 de 28 países el salario real ha subido. La Gen Z cobra más que sus padres a su edad.

> Pero Europa Occidental apenas se ha movido. Bélgica: 3,8% en 16 años.

> Y aquí viene la conexión más importante. Si combino esto con H3, la foto cambia: la Gen Z puede comprar más comida, pero tiene mucho más difícil alquilar un piso.

> La hipótesis es falsa en los números, pero cierta en la experiencia vivida. La precariedad no se mide en euros. Se mide en metros cuadrados."

---

### PAÍS VASCO (1 min)
> "1.500 euros en el País Vasco equivalen a 1.651 de poder adquisitivo. Supera a Francia, se acerca a Bélgica. Es una convergencia con la media alta europea.

> Pero como hemos visto, la cifra sola no basta. Sin vivienda asequible, 1.500 euros se quedarán cortos."

(Vuelve a la presentación, slide 6.)

---

## FASE 3: SLIDES DE CIERRE (5 minutos)

### SLIDE 6: Resultados (1 min)
> "Tres validadas, una parcial, una refutada. La refutada demuestra rigor: si no sale, se dice."

### SLIDE 7: El hallazgo principal (1.5 min)
> "La Gen Z gana más, pero puede permitirse menos. H5 y H3 juntas cuentan la historia que no se ve por separado. La precariedad ya no se mide en euros. Se mide en metros cuadrados."

### SLIDE 8: País Vasco (1 min)
> "1.651 PPS. Convergencia real con los estándares europeos. Pero necesita vivienda, igualdad y empleo digno."

### SLIDE 9: Lo que he aprendido (1 min)
> "Cuatro cosas. Los datos te corrigen. No todo se mide igual. Limpiar es el 80%. Y las hipótesis se conectan."

### SLIDE 10: Cierre (30 seg)
> "¿Cuánto vale tu trabajo? Depende de dónde vivas. Gracias."

---

## RESPUESTAS PREPARADAS

**"¿Por qué Pearson?"** "Es el test estándar para medir correlación lineal. Para un EDA es la herramienta base."

**"¿Por qué outer join?"** "Cada dataset cubre años diferentes. Con outer conservo todo y gestiono los huecos hipótesis por hipótesis."

**"¿Cómo elegiste los filtros?"** "Desde la web de Eurostat. Cada dataset tiene un explorador con filtros donde están todas las opciones descritas."

**"¿Los datos del País Vasco son de Eurostat?"** "No. Eurostat no tiene datos por CCAA. Apliqué el ratio PPS/EUR de España a la propuesta de 1.500 euros."

**"¿H5 no se valida pero dices que la Gen Z vive peor?"** "H5 pregunta si la inflación se come el salario. No. Pero H3 muestra que la vivienda sube más rápido. Juntas: cobran más pero acceden a menos."

**"¿Qué mejorarías?"** "Datos de alquiler real para H3, variables de control para H2 y H4, y análisis por CCAA."
