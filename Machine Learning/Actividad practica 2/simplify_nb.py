import json

with open("jimenez_arias_actividad2.ipynb", "r", encoding="utf-8") as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'markdown':
        source = "".join(cell['source'])
        
        # Ex 1A
        if "El diagrama de dispersión expone de manera visual la distribución conjunta" in source:
            cell['source'] = ["## A. Analizar el conjunto de datos proporcionados usando los métodos y gráficos pertinentes.\n\n",
                              "**Análisis de los datos:**\n",
                              "Al observar el diagrama de dispersión, podemos ver de manera clara cómo se relacionan ambas variables. Hay una **tendencia positiva**: es decir, por lo general, los padres más altos tienden a tener hijos proporcionalmente más altos. Como es natural al medir personas, los puntos están algo dispersos porque la estatura de un hijo no depende solo del padre, sino de otras cosas como la genética de la madre o la alimentación, pero la relación principal es bastante evidente."]
        
        # Ex 1B
        elif "La regresión lineal simple busca ajustar una recta" in source:
            cell['source'] = ["## B. Crear un modelo de regresión lineal para así obtener los parámetros de dicho modelo.\n\n",
                              "**Análisis de los resultados del modelo:**\n",
                              "El modelo de regresión crea una línea recta matemática para tratar de pasar lo más cerca posible del centro de todos los datos.\n\n",
                              "- **La pendiente (Beta 1):** Nos indica cuánto esperamos que crezca la estatura del hijo por cada unidad extra en la estatura del padre.\n",
                              "- **El intercepto (Beta 0):** Nos indica dónde empieza la línea numéricamente. Aunque biológicamente un padre no podría medir 0, es un valor matemático necesario para fijar el punto de partida en nuestra gráfica."]
        
        # Ex 1C
        elif "Al superponer el vector de regresión sobre la nube de puntos se aprecia que la recta actúa" in source:
            cell['source'] = ["## C. Representar en un diagrama la recta de regresión junto a los datos.\n\n",
                              "**Análisis de la recta:**\n",
                              "Al colocar la línea de predicciones roja sobre nuestros puntos reales, podemos confirmar visualmente el buen comportamiento del modelo. Esta línea funciona como una especie de 'promedio global' en diagonal. Algunos datos reales quedan por encima o por debajo, pero la línea traza el camino que mejor envuelve y representa el comportamiento de la mayoría."]
        
        # Ex 1D
        elif "El promedio convencional (media) es sumamente sensible a atípicos" in source:
            cell['source'] = ["## D. Realizar una predicción para la trimedia y la centrimedia de la variable independiente.\n\n",
                              "**Análisis de predicciones robustas:**\n",
                              "El promedio normal muchas veces puede engañarnos si consideramos a personas extraordinariamente altas o de estatura muy baja. Por eso preferimos calcular la **trimedia** y la **centrimedia**, que son medidas 'robustas' ya que logran omitir o restarle importancia a esos extremos poco comunes.\n\n",
                              "Al poner estos valores calculados dentro de nuestro modelo de regresión, logramos predecir la estatura más verídica que tendría un hijo de un 'padre de estatura convencional', evitando con esto que las rarezas inflen nuestra respuesta final."]
        
        # Ex 1E
        elif "Expresa matemáticamente qué porcentaje de la varianza total" in source:
            cell['source'] = ["## E. Obtener y analizar el coeficiente R^2, el error cuadrático medio y la estimación de varianza por máxima verosimilitud.\n\n",
                              "**Análisis de las métricas de error y precisión:**\n",
                              "- **El Coeficiente $R^2$:** Este valor es muy útil porque nos indica qué tanta porción de la estatura del hijo es explicada exclusivamente pos la del padre. Al no ser un $R^2$ cercano al 100%, comprobamos lo que dijimos al inicio: hay variables ambientales fuera del algoritmo que también rigen esta métrica.\n",
                              "- **El Error Cuadrático Medio y la Varianza (MLE):** Son indicadores que miden cuánto llega a equivocarse nuestra recta alejándose de los registros reales. Conocer este límite de falla  nos da mayor perspectiva de la realidad."]
        
        # Ex 1F
        elif "Validar supuestos es lo que dota de validez inferencial al RLS" in source:
            cell['source'] = ["## F. Determinar si se cumple la homocedasticidad y normalidad de los residuos.\n\n",
                              "**Evaluación de los residuos del algoritmo:**\n",
                              "Para estar seguros de que nuestras conclusiones son firmes, realizamos estos test de rigor:\n",
                              "1. **Normalidad (Shapiro-Wilk):** Compara los fallos buscando si gozan de una distribución 'normal' clásica de campana.\n",
                              "2. **Homocedasticidad (Breusch-Pagan):** Evalúa un requisito clave: que la variabilidad de los errores se mantenga más o menos constante, sin formar un 'embudo' visual. \n\n",
                              "Al observar los gráficos y procesar los tests, nos alegra ver cumplido el principio de homocedasticidad en los residuos, validando nuestra práctica algorítmica."]
        
        # Ex 1G
        elif "Todo vector tiene cierto peso predictivo, pero necesitamos saber si es matemáticamente nulo" in source:
            cell['source'] = ["## G. Comprobar si la variable independiente es significativa o no significativa en el modelo creado.\n\n",
                              "**Significancia de la variable:**\n",
                              "Para este apartado utilizamos el Intervalo de Confianza, de tal forma que no dejemos los hallazgos a la simple 'casualidad'. Si nuestro intervalo de valores cayera alguna vez en el número cero (0), implicaría que probablemente la estatura del papá a veces no aporta en nada.\n\n",
                              "Dado que los cálculos devueltos caen muy lejos del cero y no lo incluyen, comprobamos de forma rigurosa y matemática que esta variable **sí es indudablemente significativa** para predecir al hijo."]
        
        # Ex 1H
        elif "El modelo construido posee fuerte significancia estadística en los parámetros" in source:
            cell['source'] = ["## H. Tomando en cuenta todo lo anterior, ¿Este modelo es útil para realizar predicciones y cómo se podría realizar una mejora del mismo?\n\n",
                              "**¿Considero útil este modelo?**\n",
                              "Sí, es indudablemente útil, ya que confirmamos con las pruebas estadísticas que la altura paterna efectivamente influye de manera significativa. Las comprobaciones fundamentales como la Homocedasticidad salieron estables, sirviendo como un excelente marco de diagnóstico rápido en aproximaciones médicas iniciales.\n\n",
                              "**¿Cómo lo podemos mejorar basándonos en nuestra teoría?**\n",
                              "1. Transicionar de una vía simple a una múltiple: recolectar y subir las mediciones genéticas de la madre al conjunto de datos.\n",
                              "2. Aprovechar recursos detectados como la Centrimedia para proceder con la limpieza y exclusión de los sujetos que tengan registros atípicos (muy grandes o muy pequeños) que generan ruido alterando la precisión final."]
        
        # Ex 2A
        elif "Inicialmente, los modelos de aprendizaje maquinal son incapaces de interpretar el lenguaje" in source:
            cell['source'] = ["## A. Analizar el conjunto de datos proporcionados usando los métodos y los gráficos pertinentes.\n\n",
                              "**Análisis exploratorio:**\n",
                              "Para poder alimentar un modelo lineal con la meta de Calorías ('Low Efficiency', 'High Efficiency'), se requiere transformar esas palabras a números equivalentes (0, 1, 2) pues la regresión demanda números reales.\n\n",
                              "A modo exploratorio generamos tanto una Tabla Descriptiva para revisar los promedios universales como una Matriz de Correlación que nos ilumina el panorama sobre cuáles variables de estilo de vida parecen ir más atadas de la mano al resultado ideal corporal. Finalmente, se anexan histogramas en cuadrícula de nuestra población para vislumbrar su estado general."]
        
        # Ex 2B
        elif "Aunque el modelo es múltiple, el supuesto pide destilar empíricamente una regresión" in source:
            cell['source'] = ["## B. En caso de seleccionar una única variable independiente para predecir Y, ¿cuál sería y por qué?\n\n",
                              "**Elección de impacto directo:**\n",
                              "Si sólo tuviéramos permitido meter una única de las variables al modelo para predecir la eficiencia (haciendo en vez de múltiple, algo simple), la decisión se guía matemáticamente. Debemos escoger aquella donde su 'correlación absoluta' sea la más elevada contra la meta (eficiencia de calorías). Entre más cerca del 1 se encuentre (o del -1), indicará la fuerza biológica de relación estrecha que ambos poseen en el día a día."]
        
        # Ex 2C (Keep text, just check for formatting)
        # Ex 2D
        elif "La regresión múltiple ya no crea una \"recta bidimensional\", sino un **hiperplano multidimensional**" in source:
            cell['source'] = ["## D. Crear un modelo de regresión lineal múltiple para obtener y analizar sus parámetros.\n\n",
                              "**Análisis de nuestra estructura:**\n",
                              "Al armar nuestra regresión, el formato se vuelve múltiple porque cada variable aporta lo suyo en la ecuación, por ende cada una tiene su propio parámetro de influencia. Aquellas variables (como la masa corporal o la actividad) que posean coeficientes más distanciados dictarán al final qué es lo que más influye la máquina natural de la persona."]
        
        # Ex 2E
        elif "La herramienta OLS provee el valor universal más valioso: los $P>|t|$" in source:
            cell['source'] = ["## E. Determinar las variables significativas y analizar formalmente el $R^2$.\n\n",
                              "**Interpretación de la regresión y el $R^2$:**\n",
                              "Al imprimir el reporte formal (OLS), observamos en especial la columna de $P$-valores. La docencia establece que variables con P menor o igual a 0.05 sí se ganan la corona de 'significativas', logrando un impacto real.\n\n",
                              "Por el lado del ajuste predictivo, se observa un altísimo $R^2$ sobre el dataset de testing para esta problemática deportiva. Un nivel que nos asegura rotundamente que, si introducimos de golpe nuestra vida personal, la predicción arrojada mantendría un estándar altísimo."]
        
        # Ex 2F
        elif "No todas las mediciones físicas contribuyeron un efecto verídico real sobre" in source:
            cell['source'] = ["## F. Eliminar variables que NO son significativas y comparar el $R^2$.\n\n",
                              "**Filtrado analítico:**\n",
                              "Es una de las mejores y más aplicables sugerencias en Machine Learning: si limpiamos la fórmula y botamos todos los predictores biológicos que superaron el umbral de significancia del 0.05, depuramos por completo el ruido del sistema iterativo. Lo más increíble es observar que, al testear este nuevo modelo emparejado más pequeño, el $R^2$ apenas experimenta cambios perjudiciales, confirmando que deshacerse del lastre no daña predicciones."]
        
        # Ex 2G
        elif "Un pecado en estadística múltiple es la colinealidad" in source:
            cell['source'] = ["## G. Analizar la colinealidad usando Factor de Inflación de Varianza (VIF).\n\n",
                              "**Vulnerabilidades de Colinealidad (VIF):**\n",
                              "La prueba 'VIF' detecta si un par de variables caen en redundancia extrema y compiten para dar el mismo valor de información. Si el número del VIF sobrepasa un estado de salud entre 5 a 10, es una alta advertencia de colinealidad. Si estas mediciones tienen mucha asociación entre ellas mismas, los coeficientes fallan e inferir de forma unitaria se vuelve engañoso."]
        
        # Ex 2H
        elif "Todo análisis descansa en poder confirmar de la forma lo más visual posible si la discrepancia" in source:
            cell['source'] = ["## H. Comparar métricas residuales, predichos contra validados empíricamente.\n\n",
                              "**Graficando la Efectividad (Validados vs Predichos):**\n",
                              "Se cruza la predicción en un eje y la exactitud del testeo en otro. Si lo pronosticado es bueno, estos puntos se pegan formando por sí mismos la diagonal perfecta del plano sin mayores desviaciones. Ver esta alineación es una de las mayores insignias de que el error cuadrado se ha disipado grandemente."]
        
        # Ex 2I
        elif "Exprimir y obtener el arreglo de medianas correspondientes a todo el dataset" in source:
            cell['source'] = ["## I. Realizar la predicción condicional sustentada en la tendencia central mediana poblacional general.\n\n",
                              "**El Perfil del Usuario Convencional:**\n",
                              "Calcular las medianas de absolutamente cada rutina (sueño, vasos de agua, pesos) y dárselas de comer a la red predictora arroja un panorama inigualable. El resultado que imprime es exactamente en qué estatus de eficiencia calórica quedaría estancado un ser humano en la sociedad moderna estricta y rígidamente promedio."]
        
        # Ex 2J
        elif "Definitivamente, el modelo de regresión algorítmica múltiple goza de una aplastante fiabilidad" in source:
            cell['source'] = ["## J. Consideraciones Analíticas, Supuestos Universales y Reflexión Estructural\n\n",
                              "**¿Es de utilidad nuestro modelo final?**\n",
                              "Claro que sí, es sumamente provechoso. Al juntar varias variables diarias simultáneamente como el agua o el tiempo activo, la certeza calórica explota a niveles altísimos con el $R^2$. Es una herramienta predecible y muy fiel para una aproximación general clínica.\n\n",
                              "**Limitaciones a tomar en serio:**\n",
                              "A pesar de los halagos empíricos, la gran falla se evidenció en la comprobación VIF: **demasiada colinealidad**. Cosas obvias como tus minutos activos están fuertemente engranadas a tus pasos diarios, lo cual genera un pleito algorítmico interno, inflando la varianza al tratar de atribuir el peso individual.\n\n",
                              "**Recomendación pura:**\n",
                              "Tomando en cuenta la colinealidad que hallamos en las pruebas o que la meta era en sí clasificar datos de etiquetas ('Alta' y 'Normal'), la clave de evolución más orgánica sin tocar la regresión recae en reevaluar las métricas y castigar en exclusión aquellas sumamente idénticas con VIF > 10, y continuar el análisis de predicción libre de ruidos."]

    # Code cell modifications
    if cell['cell_type'] == 'code':
        source = "".join(cell['source'])
        # Fix the % bug that caused the crash in test
        if 'print("El IC al 95%' in source:
            cell['source'] = [line.replace('print("El IC al 95%', 'print("El IC al 95 por ciento') for line in cell['source']]
        
        # In Ex 1 A: change plot from red stars to scatter for aesthetic perfection
        if "plt.plot(X1, y1, 'b*'" in source:
            cell['source'] = [line.replace("plt.plot(X1, y1, 'b*', alpha=0.6)", "plt.scatter(X1, y1, color='navy', alpha=0.6, edgecolors='white', s=70)") for line in cell['source']]

with open("jimenez_arias_actividad2.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Notebook simplified successfully")
