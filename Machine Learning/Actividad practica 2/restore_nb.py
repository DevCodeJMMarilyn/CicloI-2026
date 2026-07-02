import json

cells = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# Actividad Práctica 2: Regresión Lineal Simple\n",
            "**Nombre:** Jimenez Arias\n",
            "**Código:** u20231085"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## A. Analizar el conjunto de datos proporcionados usando los métodos y gráficos pertinentes.",
            "\n\n**Análisis de los resultados:** El diagrama de dispersión expone de manera visual la distribución de las variables conjuntas de la muestra. Se puede observar una tendencia positiva: valores más altos en la estatura del padre suelen corresponder linealmente a estaturas relativas más altas en el hijo, aunque con cierta dispersión que es esperable en el estudio de datos poblacionales."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "import pandas as pd\n",
            "import numpy as np\n",
            "import matplotlib.pyplot as plt\n",
            "import scipy.stats as stats\n",
            "import statsmodels.api as sm\n",
            "import statsmodels.stats.api as sms\n",
            "from sklearn.linear_model import LinearRegression\n",
            "from sklearn.metrics import mean_squared_error\n",
            "\n",
            "# Cargar los datos\n",
            "df = pd.read_csv('Dataset 3 P1.csv')\n",
            "X = df['Father'].values\n",
            "y = df['Son'].values\n",
            "\n",
            "print(\"Primeros datos del dataset:\")\n",
            "print(df.head())\n",
            "\n",
            "# Gráfico de dispersión\n",
            "plt.figure(figsize=(7,5))\n",
            "plt.plot(X, y, '*')\n",
            "plt.xlabel(\"Estatura del padre\")\n",
            "plt.ylabel(\"Estatura del hijo\")\n",
            "plt.title(\"Relación entre estatura del padre y del hijo\")\n",
            "plt.show()"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## B. Crear un modelo de regresión lineal para así obtener los parámetros de dicho modelo.",
            "\n\n**Análisis de los resultados:** La regresión lineal es el algoritmo utilizado para calcular la línea que mejor se ajuste a los datos brindados, buscando reducir las distancias entre dicha línea y los puntos. El modelo entrenado entrega un coeficiente de pendiente, que representa numéricamente el aumento esperado en la altura del hijo por cada unidad que sube la altura del padre, y un intercepto que sirve como origen matemático en la recta."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "#Creamos una instancia de LinearRegression\n",
            "lineal_regresion = LinearRegression()\n",
            "#Instruimos a la regresión lineal que aprenda de los datos (X, y)\n",
            "lineal_regresion.fit(X.reshape(-1,1), y)\n",
            "\n",
            "print(\"El coeficiente es %s y el intercepto es %s\"%(lineal_regresion.coef_, lineal_regresion.intercept_))\n",
            "print(\"La recta de regresión es y= %s x + %s\"%(lineal_regresion.coef_[0], lineal_regresion.intercept_))"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## C. Representar en un diagrama la recta de regresión junto a los datos.",
            "\n\n**Análisis de los resultados:** Al superponer la predicción de la recta al esquema visual de la muestra, se aprecia gráficamente que el modelo captura correctamente la tendencia principal. Esta recta viene a indicar un promedio de centralidad diagonal alrededor del cual oscilan las diferentes variables biológicas de la vida real."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Representar x e y\n",
            "fig = plt.figure(figsize=(7,5))\n",
            "plt.scatter(X, y, alpha=0.5)\n",
            "\n",
            "# Representar la recta de regresion\n",
            "y_pred = lineal_regresion.predict(X.reshape(-1,1))\n",
            "plt.plot(X, y_pred, color='red', linewidth=3)\n",
            "\n",
            "# Definir ejes\n",
            "plt.xlabel(\"Estatura del padre\")\n",
            "plt.ylabel(\"Estatura del hijo\")\n",
            "plt.title(\"Recta de regresión y datos reales\")\n",
            "\n",
            "# Mostrar grafico\n",
            "plt.show()"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## D. Realizar una predicción para la trimedia y la centrimedia de la variable independiente.",
            "\n\n**Análisis de los resultados:** El cálculo de medidas robustas de estimación como la trimedia y centrimedia logran proporcionar indicadores de tendencia central estables, sin dejarse desviar o corromper por valores extravagantes. Realizar las predicciones a partir de de estas medidas robustas permite observar cuál sería la altura un tanto más verídica de un hijo tomando como referencia a los padres más convencionales, mitigando el peso de estaturas atípicas."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Ordenar los valores de la muestra X\n",
            "X_sorted = np.sort(X)\n",
            "\n",
            "# Trimedia\n",
            "q1_x = np.quantile(X_sorted, 0.25)\n",
            "me_x = np.quantile(X_sorted, 0.50)\n",
            "q3_x = np.quantile(X_sorted, 0.75)\n",
            "trimedia = (q1_x + 2*me_x + q3_x)/4\n",
            "print(\"La trimedia de X es %s\" %trimedia)\n",
            "\n",
            "# Centrimedia (alfa=25%)\n",
            "n = len(X_sorted)\n",
            "alfa = 0.25\n",
            "c = alfa * n\n",
            "entero = int(c)\n",
            "p = 1 + entero - c\n",
            "\n",
            "# Eliminar 'entero' de cada lado\n",
            "X3 = X_sorted[entero:n-entero].copy()\n",
            "if len(X3) > 1 and p != 1.0:\n",
            "    # Ponderar el primer y último valor\n",
            "    X3[0] = p * X3[0]\n",
            "    X3[-1] = p * X3[-1]\n",
            "\n",
            "centrimedia = np.sum(X3) / (n - 2*c)\n",
            "print(\"La centrimedia de X es %s\" %centrimedia)\n",
            "\n",
            "# Predicciones\n",
            "pred_trimedia = lineal_regresion.predict(np.array([trimedia]).reshape(-1,1))[0]\n",
            "pred_centrimedia = lineal_regresion.predict(np.array([centrimedia]).reshape(-1,1))[0]\n",
            "\n",
            "print(\"\\nPredicción para la trimedia: %s\" %pred_trimedia)\n",
            "print(\"Predicción para la centrimedia: %s\" %pred_centrimedia)"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## E. Obtener y analizar el coeficiente R^2, el error cuadrático medio y la estimación de la varianza por máxima verosimilitud.",
            "\n\n**Análisis de los resultados:** El coeficiente de determinación ($R^2$) expone porcentualmente en qué medida la dependencia de las alturas de los hijos es explicada por la línea de regresión de los padres. Por otro lado, la obtención del error cuadrático medio y la varianza mediante máxima verosimilitud muestran un estimado de cuán amplias son las distancias con las que las predicciones producidas fallan y se alejan de los valores reales medidos en el modelo."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Coeficiente R^2\n",
            "r2 = lineal_regresion.score(X.reshape(-1,1), y)\n",
            "print(\"El coeficiente de determinación R^2 es %s\" %r2)\n",
            "\n",
            "# Error cuadrático medio\n",
            "mse = mean_squared_error(y_true=y, y_pred=y_pred)\n",
            "print(\"El error cuadrático medio es %s\" %mse)\n",
            "\n",
            "# Estimador de la varianza por MLE (método de máxima verosimilitud)\n",
            "y_resta = (y - y_pred) ** 2\n",
            "var_mle = sum(y_resta) / len(y)\n",
            "print(\"La estimación de la varianza por MLE es %s\" %var_mle)"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## F. Determinar si se cumple la homocedasticidad y normalidad de los residuos.",
            "\n\n**Análisis de los resultados:** Para asegurar la fiabilidad estadística general se deben estudiar los residuos arrojados. La prueba Shapiro-Wilk evalúa la premisa de normalidad en la variabilidad de estos residuos. En la misma vía, la experimentación con el test de Breusch-Pagan corrobora la idea de homocedasticidad, asegurando que la desviación residual permanezca constante entre las variables. Cumplir con estos requisitos blinda contra el sesgo de fiabilidad."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Obtener residuos\n",
            "residuos = y - y_pred\n",
            "\n",
            "# Test Shapiro-Wilk para normalidad\n",
            "sh_result = stats.shapiro(residuos)\n",
            "print(\"Test Shapiro-Wilk (Normalidad), p-valor: %5.5f\" %sh_result.pvalue)\n",
            "if sh_result.pvalue < 0.05:\n",
            "    print(\"Como p.valor < 0.05, se rechaza la hipótesis nula y no se da normalidad en los residuos.\\n\")\n",
            "else:\n",
            "    print(\"Como p.valor > 0.05, no se rechaza la hipótesis nula; se da normalidad en los residuos.\\n\")\n",
            "\n",
            "# Test Breusch-Pagan para homocedasticidad\n",
            "X_sm = sm.add_constant(X)\n",
            "m1 = sm.OLS(y, X_sm).fit()\n",
            "bp1 = sms.het_breuschpagan(resid = m1.resid, exog_het = m1.model.exog)[1]\n",
            "print(\"Test Breusch-Pagan (Homocedasticidad), p-valor: %5.5f\" %bp1)\n",
            "if bp1 < 0.05:\n",
            "    print(\"Como p.valor < 0.05, se rechaza la hipótesis nula de homocedasticidad.\")\n",
            "else:\n",
            "    print(\"Como p.valor > 0.05, no se rechaza la hipótesis nula y se da homocedasticidad.\")"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## G. Comprobar si la variable independiente es significativa o no significativa en el modelo creado.",
            "\n\n**Análisis de los resultados:** El desarrollo del intervalo de confianza para la variable es elemental para validar si la significancia aportada para el modelo es real. Al constatar que el rango de la amplitud obtenida no cruza con el número cero (0), se logra corroborar bajo bases matemáticas que la variable independiente –la estatura del padre– tiene sin duda un impacto en las mediciones resultantes."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# calcular ICbeta1\n",
            "y_resta = (y - y_pred)**2\n",
            "s2 = sum(y_resta)/(len(y)-2)\n",
            "den = np.var(X) * len(X)\n",
            "sb1 = (s2/den) ** 0.5\n",
            "amplitud = 1.96 * sb1\n",
            "\n",
            "print(\"El IC al 0.95 de b1 es: %s +/- %s\" %(lineal_regresion.coef_[0], amplitud))\n",
            "lim_inf = lineal_regresion.coef_[0] - amplitud\n",
            "lim_sup = lineal_regresion.coef_[0] + amplitud\n",
            "print(\"El intervalo es [%.4f, %.4f]\" %(lim_inf, lim_sup))\n",
            "\n",
            "if lim_inf <= 0 <= lim_sup:\n",
            "    print(\"El intervalo de confianza contiene al 0 para beta_1, luego, la variable NO es significativa.\")\n",
            "else:\n",
            "    print(\"El intervalo de confianza NO contiene al 0 para beta_1, luego, la variable SÍ es significativa.\")"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## H. Tomando en cuenta todo lo anterior, ¿Este modelo es útil para realizar predicciones y cómo se podría realizar una mejora del mismo?\n",
            "\n",
            "**Análisis de la utilidad del modelo:**\n",
            "Con las evaluaciones hechas, puede concluirse que el modelo tiene utilidad ya que la significancia estadística comprobó matemáticamente la influencia del padre en este conjunto de datos. No obstante, el coeficiente $R^2$ muestra una limitación y las oscilaciones residuales reflejan que este factor no lo es todo; existiendo muchas otras circunstancias ajenas al predictor actual en el campo de este estudio vitalicio de salud.\n\n",
            "**¿Cómo lo podría mejorar?:**\n",
            "1. **Emplear variables múltiples:** Adicionar variables informacionales de valor relacionadas a la altura de la madre del niño, características de peso/nutrición durante el crecimiento, o al menos su género biológico.\n",
            "2. **Limpiar datos excesivos o atípicos:** Apoyándose en las medidas de centrimedia y trimedia calculables en la fase exploratoria, la depuración intencionada de la data para excluir los puntos alejados disminuirá el sesgo del error global de la recta.\n",
            "3. **Evaluaciones de algoritmos y escalas logarítmicas:** Utilizar regularizaciones o en todo caso evaluar el desempeño de algoritmos que admitan formas polinomiales pueden reducir notablemente los rezagos residuales de un algoritmo puramente recto."
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "---\n\n",
            "# Ejercicio 2: Modelo de Regresión Lineal Múltiple\n",
            "**Dataset:** Dataset 4 P2.csv\n"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## A. Analizar el conjunto de datos proporcionados usando los métodos y los gráficos pertinentes.",
            "\n\n**Análisis de los resultados:** La fase de análisis exploratorio nos arroja información estructural descriptiva. Al imprimir la información de la base, se comprueba que todas las variables estén en los formatos correctos numéricos, y de no haber datos nulos. Finalmente la matriz de correlación nos evidencia a color las variables que guardan mayor relación con la métrica dependiente de eficiencia calórica (como efficiency_score, active_minutes, etc)."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "from sklearn.metrics import r2_score\n",
            "from sklearn.model_selection import train_test_split\n",
            "from statsmodels.stats.outliers_influence import variance_inflation_factor\n\n",
            "datos2 = pd.read_csv('Dataset 4 P2.csv')\n",
            "# Convertir la variable categórica a numérica para permitir regresión y correlación\n",
            "mapping = {'Low Efficiency': 0, 'Moderate': 1, 'High Efficiency': 2}\n",
            "datos2['calorie_efficiency'] = datos2['calorie_efficiency'].map(mapping)\n",
            "print(\"---- INFO DEL DATASET ----\")\n",
            "datos2.info()\n",
            "print(\"\\n---- DESCRIPCIÓN ----\")\n",
            "display(datos2.describe().round(2))\n",
            "\n",
            "# Matriz de correlación\n",
            "corr2 = datos2.corr(numeric_only=True)\n",
            "try:\n",
            "    display(corr2.style.background_gradient(cmap='coolwarm'))\n",
            "except AttributeError:\n",
            "    display(corr2.round(3))"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## B. En caso de seleccionar una única variable independiente para intentar predecir la variable Y, ¿cuál sería y por qué?",
            "\n\n**Análisis de los resultados:** Si se forzara a usar una regresión lineal simple en un entorno con múltiples columnas, se debe elegir el valor con la influencia más directa sobre $Y$. Para identificarlo, la métrica con un grado de correlación absoluta (sea positiva o negativa) más elevado dicta de forma pragmática la columna que más predice el comportamiento aislado del objetivo."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "correlaciones2 = corr2['calorie_efficiency'].drop('calorie_efficiency')\n",
            "mejor_variable2 = correlaciones2.abs().idxmax()\n",
            "print(f\"La variable independiente recomendada sería '{mejor_variable2}' dado que posee la mayor correlación absoluta con la eficiencia de calorías (valor de: {correlaciones2[mejor_variable2]:.4f}). Esto indica que es el elemento que, de forma solitaria, mejor puede predecir el resultado final de Y.\")"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## C. Realizar una partición de los datos previamente procesados en un 2a% para la validación.",
            "\n\n**Análisis de los resultados:** El código *a* extraído de identificar el carnet (U20231085) nos da la cifra $a=5$, resultando en un 25% de segmentación para testing y 75% para training. Dejar reservado el segmento sirve como un filtro contra el sobreajuste (overfitting)."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "x2_ind = datos2.drop(\"calorie_efficiency\", axis=1)\n",
            "y2_dep = datos2[\"calorie_efficiency\"].copy()\n",
            "\n",
            "# Según el carnet u20231085, a=5, test_size=0.25 (25%)\n",
            "# Y el random_state asume el carnet (20231085)\n",
            "X2_train, X2_test, y2_train, y2_test = train_test_split(x2_ind, y2_dep, test_size=0.25, random_state=20231085)\n",
            "print(\"Partición lista. Registros para entrenamiento:\", len(X2_train), \"| Registros para prueba:\", len(X2_test))"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## D. Crear un modelo de regresión lineal múltiple para así obtener los parámetros de dicho modelo.",
            "\n\n**Análisis de los resultados:** Obtener los coeficientes otorga el poder de comprender qué rol juego cada variable en la quema de energía. Un coeficiente positivo alto refleja un aspecto que sube con creces la métrica final; mientras que uno negativo hace lo contrapuesto. Esta lista de números junto con el intercepto ensamblan la base estructural del algoritmo."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "lm_multiple2 = LinearRegression()\n",
            "lm_multiple2.fit(X2_train, y2_train)\n",
            "\n",
            "print(\"El intercepto obtenido es:\", lm_multiple2.intercept_)\n",
            "display(pd.DataFrame({\"Variables\": x2_ind.columns, \"Coeficientes\": lm_multiple2.coef_}))"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## E. Determinar las variables que son significativas para el modelo y analizar el R^2 obtenido.",
            "\n\n**Análisis de los resultados:** El reporte OLS permite calcular los intervalos de p-valor, catalogando como *significativas* a aquellas columnas cuyo $P>|t|$ es inferior o igual a $0.05$. Estas variables de hecho intervienen estadísticamente en la formula. El valor $R^2$ describe de forma general la precisión del ensamblaje del modelo al compararlo con nuestra red de datos de testing."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Añadir el intercepto a statsmodels\n",
            "X2_sm = sm.add_constant(X2_train)\n",
            "est_mult2 = sm.OLS(y2_train, X2_sm)\n",
            "est_res2 = est_mult2.fit()\n",
            "print(est_res2.summary())\n",
            "\n",
            "# Análisis R^2 del modelo\n",
            "y_pred_mult2 = lm_multiple2.predict(X2_test)\n",
            "r2_mult2 = r2_score(y2_test, y_pred_mult2)\n",
            "print(\"\\nEl coeficiente de determinación R^2 del modelo es:\", r2_mult2)"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## F. Eliminar las variables que no son significativas y comparar el R^2 con el del modelo original.",
            "\n\n**Análisis de los resultados:** Extraer aquellas métricas que no logran la significancia del $0.05$ depura el modelo de \"ruido\". Al entrenar el modelo con este set pulido, se puede confirmar si el $R^2$ decae gravemente o si, más bien, conserva sus predicciones evitando información no esencial."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "p_valores2 = est_res2.pvalues.drop('const')\n",
            "significativas2 = p_valores2[p_valores2 <= 0.05].index.tolist()\n",
            "print(\"Variables significativas (P <= 0.05):\", significativas2)\n",
            "\n",
            "if len(significativas2) < len(x2_ind.columns):\n",
            "    # Crear nuevo modelo depurado\n",
            "    X_train_sig2 = X2_train[significativas2]\n",
            "    X_test_sig2 = X2_test[significativas2]\n",
            "    \n",
            "    lm_sig2 = LinearRegression()\n",
            "    lm_sig2.fit(X_train_sig2, y2_train)\n",
            "    \n",
            "    y_pred_sig2 = lm_sig2.predict(X_test_sig2)\n",
            "    r2_sig2 = r2_score(y2_test, y_pred_sig2)\n",
            "    \n",
            "    print(\"\\nR^2 del modelo original:\", r2_mult2)\n",
            "    print(\"R^2 del modelo depurado:\", r2_sig2)\n",
            "else:\n",
            "    print(\"\\nTodas las variables son significativas. El R^2 del modelo permanece idéntico.\")"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## G. Analizar la colinealidad de las variables independientes con los métodos correspondientes.",
            "\n\n**Análisis de los resultados:** A través del VIF (Factor de Inflación de Varianza) se analiza el grado en que las variables redundan entre sí en lugar de agregar información diferente. Cuando un VIF es extremadamente alto (> 5 o > 10) significa que estos elementos podrían confundir los coeficientes entrenados y deberían considerarse en su exclusión paralela."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "VIF2 = pd.DataFrame()\n",
            "VIF2[\"Variable\"] = x2_ind.columns\n",
            "VIF2[\"VIF\"] = [variance_inflation_factor(x2_ind.values, i) for i in range(len(x2_ind.columns))]\n",
            "display(VIF2)"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## H. Comparar los valores reales vs predichos (MSE y gráfico de dispersión).",
            "\n\n**Análisis de los resultados:** La gráfica que contrasta la prueba en el eje horizontal contra un valor inferido ideal permite revisar rápidamente el paralelismo de la información predicha. Si los puntos se ciñen íntimamente a la diagonal principal ($y=x$), esto validaría empíricamente una precisión fuerte por parte del código desplegado."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "mse_mult2 = mean_squared_error(y2_test, y_pred_mult2)\n",
            "print(\"El error cuadrático medio (MSE) calculado es:\", mse_mult2)\n",
            "\n",
            "plt.figure(figsize=(8,6))\n",
            "plt.scatter(y2_test, y_pred_mult2, alpha=0.5, edgecolor=\"none\")\n",
            "plt.xlabel(\"Valores Reales (Eficiencia Calórica)\")\n",
            "plt.ylabel(\"Valores Predichos (Eficiencia Calórica)\")\n",
            "plt.title(\"Valores Reales vs Predichos\")\n",
            "plt.plot([min(y2_test), max(y2_test)], [min(y2_test), max(y2_test)], color='salmon', linewidth=3)\n",
            "plt.show()"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## I. Realizar una predicción de la variable tomando la mediana de las variables independientes.",
            "\n\n**Análisis de los resultados:** Extraer la mediana de cada una de las columnas y realizar un despliegue pronosticador ofrece como valor devuelto una aproximación a la eficiencia energética que poseería una persona con características y hábitos \"estándar\" mediales en la sociedad mostrada por la base de datos."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Obtener medianas como array y predecir\n",
            "medianas2 = np.array(np.median(x2_ind, axis=0))\n",
            "pred_mediana_mult2 = lm_multiple2.predict(medianas2.reshape(1, -1))\n",
            "\n",
            "print(\"La predicción de eficiencia calórica usando todos los ejes bajo sus medianas es de:\", pred_mediana_mult2[0])"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## J. Tomando en cuenta todo lo anterior, ¿Este modelo es útil para realizar predicciones y cómo se podría realizar una mejora del mismo?\n",
            "\n",
            "**Análisis de la utilidad y mejoras:**\n",
            "- Las métricas conjuntas de testeo confirmaron que contar con un abanico dinámico de variables para este modelo de predicción calórica potencia monumentalmente el puntaje estadístico. Evaluar la similitud de los valores reales con los generados indica que este algoritmo múltiple puede dar un pronóstico con alta certeza.\n",
            "- A pesar de esto, se localizó que no todas las variables proporcionaban influencia valiosa y varias exhibían una colinealidad peligrosa (VIF excesivo). Para mejorar en gran medida las operaciones matemáticas en futuros usos, es altamente recomendable entrenar y pulir el modelo únicamente con los vectores marcados como significativos y estables, garantizando las respuestas y esquivando redundancias por elementos colineales como los latidos del corazón frente al porcentaje de grasa o ejercicio."
        ]
    }
]

notebook = {
    "cells": cells,
    "metadata": {},
    "nbformat": 4,
    "nbformat_minor": 4
}

file_path = r'c:\Users\Michelle Jiménez\Desktop\CLASES DE MICHELLE\Ciclo VII\Machine Learning\Actividad practica 2\jimenez_arias_actividad2.ipynb'

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1, ensure_ascii=False)
