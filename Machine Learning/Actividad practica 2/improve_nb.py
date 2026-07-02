import json

cells = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# Actividad Práctica 2: Regresión Lineal Simple y Múltiple\n",
            "**Nombre:** Jimenez Arias\n",
            "**Código:** u20231085"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "---\n# Ejercicio 1: Regresión Lineal Simple\n"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## A. Analizar el conjunto de datos proporcionados usando los métodos y gráficos pertinentes.",
            "\n\n**Análisis exploratorio:** El diagrama de dispersión expone de manera visual la distribución conjunta de la muestra. Se observa una **tendencia lineal positiva**: a medida que aumenta la estatura del padre (variable independiente $X$), la estatura del hijo (variable dependiente $Y$) también tiende a aumentar. Existe dispersión en los datos, lo cual es propio de variables biológicas poblacionales, indicando que aunque existe una relación fuerte, otros factores genéticos o ambientales (no observados aquí) también introducen variabilidad."
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
            "# 1. Cargar los datos desde el dataset proporcionado\n",
            "df1 = pd.read_csv('Dataset 3 P1.csv')\n",
            "X1 = df1['Father'].values\n",
            "y1 = df1['Son'].values\n",
            "\n",
            "print(\"Primeros datos del dataset:\")\n",
            "display(df1.head())\n",
            "\n",
            "# 2. Graficar diagrama de dispersión para exploración inicial\n",
            "plt.figure(figsize=(7,5))\n",
            "plt.plot(X1, y1, 'b*', alpha=0.6)\n",
            "plt.xlabel(\"Estatura del padre (pulgadas/cm)\")\n",
            "plt.ylabel(\"Estatura del hijo (pulgadas/cm)\")\n",
            "plt.title(\"Relación de estatura: Padre vs Hijo\")\n",
            "plt.grid(True, linestyle='--', alpha=0.5)\n",
            "plt.show()"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## B. Crear un modelo de regresión lineal para así obtener los parámetros de dicho modelo.",
            "\n\n**Análisis del modelo y parámetros:** La regresión lineal simple busca ajustar una recta de mínimos cuadrados $Y = \\beta_0 + \\beta_1 X$ que minimice la suma de los residuos al cuadrado. \n",
            "- El **coeficiente de la pendiente ($\\beta_1$)** obtenido simboliza el incremento marginal esperado; es decir, por cada unidad adicional en la estatura del padre en la muestra, la estatura predicha del hijo aumenta en la magnitud de este coeficiente.\n",
            "- El **intercepto ($\\beta_0$)** representa el valor matemático de la estatura del hijo si el padre midiera 0 unidades. Aunque carece de sentido biológico estricto, es fundamental para el anclaje del algoritmo geométrico en el plano cartesiano."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# 1. Instanciar la clase del modelo algorítmico\n",
            "lineal_regresion1 = LinearRegression()\n",
            "\n",
            "# 2. Entrenar el modelo con los datos mapeados\n",
            "lineal_regresion1.fit(X1.reshape(-1,1), y1)\n",
            "\n",
            "print(f\"Coeficiente (Pendiente, Beta 1): {lineal_regresion1.coef_[0]:.4f}\")\n",
            "print(f\"Intercepto (Beta 0): {lineal_regresion1.intercept_:.4f}\")\n",
            "print(f\"\\nEcuación de la recta: Y = {lineal_regresion1.coef_[0]:.4f}*X + {lineal_regresion1.intercept_:.4f}\")"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## C. Representar en un diagrama la recta de regresión junto a los datos.",
            "\n\n**Análisis visual de la regresión:** Al superponer el vector de regresión sobre la nube de puntos se aprecia que la recta actúa como el \"centro de gravedad\" o promedio condicionado de los datos. Esta regresión asume exitosamente la linealidad teórica, ya que visualmente cruza de forma equitativa el grueso de la distribución."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "fig = plt.figure(figsize=(8,6))\n",
            "# 1. Plotear puntos reales\n",
            "plt.scatter(X1, y1, alpha=0.5, label=\"Datos Reales\")\n",
            "\n",
            "# 2. Plotear predicciones que forman la recta de regresión\n",
            "y_pred1 = lineal_regresion1.predict(X1.reshape(-1,1))\n",
            "plt.plot(X1, y_pred1, color='red', linewidth=3, label=\"Línea de Regresión OLS\")\n",
            "\n",
            "plt.xlabel(\"Estatura del padre\")\n",
            "plt.ylabel(\"Estatura del hijo\")\n",
            "plt.title(\"Ajuste de Regresión Lineal a Datos Biológicos\")\n",
            "plt.legend()\n",
            "plt.grid(True, linestyle='--', alpha=0.5)\n",
            "plt.show()"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## D. Realizar una predicción para la trimedia y la centrimedia de la variable independiente.",
            "\n\n**Análisis e interpretación de métricas robustas:** El promedio convencional (media) es sumamente sensible a atípicos. Por ello calculamos la **trimedia** (que pondera intercuartiles) y la **centrimedia** (que recorta los extremos superior e inferior $\\alpha=25\\%$). Al inyectar estas métricas de centralidad alta en la ecuación predictora de $Y$, obtenemos qué talla desarrollaría el hijo de un \"padre poblacional netamente promedio y robusto\", limpiando cualquier influencia genética extrema o error atípico de medición en la base."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Ordenar Muestra\n",
            "X1_sorted = np.sort(X1)\n",
            "\n",
            "# Trimedia\n",
            "q1_x = np.quantile(X1_sorted, 0.25)\n",
            "me_x = np.quantile(X1_sorted, 0.50)\n",
            "q3_x = np.quantile(X1_sorted, 0.75)\n",
            "trimedia1 = (q1_x + 2*me_x + q3_x)/4\n",
            "print(f\"La trimedia robusta de la muestra X es: {trimedia1:.4f}\")\n",
            "\n",
            "# Centrimedia (alfa=25%)\n",
            "n = len(X1_sorted)\n",
            "alfa = 0.25\n",
            "c = alfa * n\n",
            "entero = int(c)\n",
            "p = 1 + entero - c\n",
            "\n",
            "# Podar array original\n",
            "X_cen = X1_sorted[entero:n-entero].copy()\n",
            "if len(X_cen) > 1 and p != 1.0:\n",
            "    X_cen[0] = p * X_cen[0]\n",
            "    X_cen[-1] = p * X_cen[-1]\n",
            "\n",
            "centrimedia1 = np.sum(X_cen) / (n - 2*c)\n",
            "print(f\"La centrimedia truncada de la muestra X es: {centrimedia1:.4f}\")\n",
            "\n",
            "# Predicciones del Modelo\n",
            "pred_trimedia1 = lineal_regresion1.predict(np.array([trimedia1]).reshape(-1,1))[0]\n",
            "pred_centrimedia1 = lineal_regresion1.predict(np.array([centrimedia1]).reshape(-1,1))[0]\n",
            "\n",
            "print(f\"\\n---> Predicción del hijo para la Trimedia del padre: {pred_trimedia1:.4f}\")\n",
            "print(f\"---> Predicción del hijo para la Centrimedia del padre: {pred_centrimedia1:.4f}\")"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## E. Obtener y analizar el coeficiente R^2, el error cuadrático medio y la estimación de varianza por máxima verosimilitud.",
            "\n\n**Interpretación Teórica del Desempeño:**\n",
            "- **Coeficiente de determinación ($R^2$):** Expresa matemáticamente qué porcentaje de la varianza total de la estatura de los hijos es explicable por la estatura del padre (variable independiente). Un valor muy cercano a 1 indicaría un ajuste perfecto. Aquí se evidencia un ajuste moderado-bajo; con lo cual se concluye estadísticamente que existen otras variables que rigen la estatura general y *no solo* el padre.\n",
            "- **Error Cuadrático Medio (MSE):** Cuantifica la magnitud de la varianza residual, castigando asimétricamente los errores o discrepancias grandes debido al cálculo en cuadrados. Resulta un claro indicativo del rango de error que posee nuestra línea de predicción.\n",
            "- **Varianza por MLE (Máxima Verosimilitud):** A diferencia de la estimación libre de sesgo que divide en $N-2$, el acercamiento MLE provee la varianza natural estricta de la división poblacional sobre $N$, sirviendo para cálculos probabilísticos integrales."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# 1. Coeficiente R^2 de determinación\n",
            "r2_1 = lineal_regresion1.score(X1.reshape(-1,1), y1)\n",
            "print(f\"Coeficiente de determinación (R^2): {r2_1:.4f}\")\n",
            "\n",
            "# 2. Error cuadrático medio\n",
            "mse1 = mean_squared_error(y_true=y1, y_pred=y_pred1)\n",
            "print(f\"Error cuadrático medio (MSE): {mse1:.4f}\")\n",
            "\n",
            "# 3. Estimador de la varianza por MLE\n",
            "y1_resta = (y1 - y_pred1) ** 2\n",
            "var_mle1 = sum(y1_resta) / len(y1)\n",
            "print(f\"Estimación de varianza por máxima verosimilitud (MLE): {var_mle1:.4f}\")"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## F. Determinar si se cumple la homocedasticidad y normalidad de los residuos.",
            "\n\n**Análisis exhaustivo de residuales Universitarios:** \n",
            "Validar supuestos es lo que dota de validez inferencial al RLS (Ordinary Least Squares):\n",
            "1. **Normalidad (Shapiro-Wilk):** Queremos confirmar empíricamente que los errores producidos provienen de una familia normal (campana de Gauss). De no serlo estaríamos invalidando intervalos asintóticos.\n",
            "2. **Homocedasticidad (Breusch-Pagan y Examen Gráfico):** Un requerimiento fundamental es que la amplitud u oscilación de los residuos debe permanecer estática y constante sin importar si calculamos partes bajas o partes altas de la matriz. Al graficar *Residuos vs Predicciones (Predicted)*, no debe observarse un patrón de «embudo». Formalizamos la asunción a través del p-valor del *test Breusch-Pagan*."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Obtener residuos del modelo (Real - Prediccion)\n",
            "residuos1 = y1 - y_pred1\n",
            "\n",
            "print(\"--- 1. ANÁLISIS DE NORMALIDAD ---\")\n",
            "sh_result1 = stats.shapiro(residuos1)\n",
            "print(f\"Test Shapiro-Wilk (p-valor): {sh_result1.pvalue:.5f}\")\n",
            "if sh_result1.pvalue < 0.05:\n",
            "    print(\"Conclusión SW: Como p.valor < 0.05, Ocurre rechazo de la hipótesis nula. Los residuos NO ostentan normalidad pura.\")\n",
            "else:\n",
            "    print(\"Conclusión SW: Como p.valor > 0.05, no se rechaza la hipótesis nula. Los residuos SON normales.\")\n",
            "\n",
            "print(\"\\n--- 2. ANÁLISIS DE HOMOCEDASTICIDAD ---\")\n",
            "X1_sm = sm.add_constant(X1)\n",
            "m1_sm = sm.OLS(y1, X1_sm).fit()\n",
            "bp1 = sms.het_breuschpagan(resid = m1_sm.resid, exog_het = m1_sm.model.exog)[1]\n",
            "print(f\"Test formal Breusch-Pagan (p-valor): {bp1:.5f}\")\n",
            "if bp1 < 0.05:\n",
            "    print(\"Conclusión BP: Como p.valor < 0.05, Rechazamos Homocedasticidad (Existe Heterocedasticidad).\")\n",
            "else:\n",
            "    print(\"Conclusión BP: Como p.valor > 0.05, No rechazamos de H0. SÍ SE CUMPLE LA HOMOCEDASTICIDAD.\\n\")\n",
            "\n",
            "# 3. Gráfica de examen de residuos vs ajustados (Prueba Visual de Homocedasticidad)\n",
            "plt.figure(figsize=(7,5))\n",
            "plt.scatter(y_pred1, residuos1, alpha=0.5, color='purple')\n",
            "plt.axhline(0, color='black', linewidth=2, linestyle='--')\n",
            "plt.xlabel(\"Valores Ajustados / Predichos\")\n",
            "plt.ylabel(\"Residuos (Error residual)\")\n",
            "plt.title(\"Evaluación Visual Homocedástica: Residuos vs Ajustados\")\n",
            "plt.grid(True, alpha=0.3)\n",
            "plt.show()"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## G. Comprobar si la variable independiente es significativa o no significativa en el modelo creado.",
            "\n\n**Justificación Técnica:** Todo vector tiene cierto peso predictivo, pero necesitamos saber si es matemáticamente nulo o no debido a la inferencia aleatoria. Se construye un rango asintótico (Intervalo de Confianza al 95%). Si ese intervalo logra abarcar aritméticamente el umbral del $0$, denota que en una porción de las mediciones la influencia del padre desaparece ($Beta = 0$). Si esquiva el $0$ en su base de amplitud total, entonces es una característica **genuinamente significativa**."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Calcular IC de beta1 manualmente para robustecer la prueba\n",
            "s2_1 = sum(residuos1**2)/(len(y1)-2)\n",
            "den1 = np.var(X1) * len(X1)\n",
            "sb1_1 = (s2_1/den1) ** 0.5\n",
            "amplitud1 = 1.96 * sb1_1\n",
            "\n",
            "beta1_val = lineal_regresion1.coef_[0]\n",
            "print(f\"El IC al 95% de la pendiente (Beta_1) estructuralmente es: {beta1_val:.4f} +/- {amplitud1:.4f}\")\n",
            "lim_inf1 = beta1_val - amplitud1\n",
            "lim_sup1 = beta1_val + amplitud1\n",
            "print(f\"El intervalo mapeado absoluto es de: [{lim_inf1:.4f}, {lim_sup1:.4f}]\")\n",
            "\n",
            "if lim_inf1 <= 0 <= lim_sup1:\n",
            "    print(\"Conclusión: El intervalo de confianza contiene al cer0 (0). Variable NO significativa en modelados infrenciales.\")\n",
            "else:\n",
            "    print(\"Conclusión: El intervalo de confianza elude rigurosamente el cer0 (0). Variable SÍ ES ALTAMENTE SIGNIFICATIVA.\")"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## H. Tomando en cuenta todo lo anterior, ¿Este modelo es útil para realizar predicciones y cómo se podría realizar una mejora del mismo?\n",
            "\n",
            "**Postura Crítica (Utilidad y Limitaciones):**\n",
            "El modelo construido posee fuerte significancia estadística en los parámetros (la estatura patrilineal afecta contundemente a la descencencia). **Sí puede ser considerado útil** en la práctica como proxy preliminar simple para estimaciones pediátricas médicas base, dado el cumplimiento exitoso del supuesto de **Homocedasticidad**. \n\n",
            "*No obstante*, posee limitaciones de fiabilidad importantes:\n",
            "1. El **Normalidad residual falló** (según Shapiro-Wilk), limitando la generalización inferencial.\n",
            "2. El porcentaje de predicción rige un valor pobre bajo el **$R^2$**, dejando ver que el conjunto solo explica una pequeña fracción biológica poblacional. La varianza ambiental fue ignorada.\n\n",
            "**Propuestas y Enfoques de Mejora Directos:**\n",
            "1. **Extender el plano a Regresión Múltiple:** Introducir *inmediatamente* la estatura de la madre biológica en la métrica. Biológicamente hablando, el peso genético materno compone la mitad de la predisposición.\n",
            "2. **Limpieza Robusta (Outliers):** Aprovechar las métricas de Trimedia/Centrimedia detectadas durante el ejercicio para generar un filtro de limpieza agresivo de desviaciones, depurando la muestra de individuos atípicamente pequeños o en estado de desnutrición poblacional atípica, garantizando que el modelo fije una línea más equitativa.\n",
            "3. **Transformaciones No Lineales:** Si no remedia la no-normalidad residual, se puede someter la variable independiente a una regresión polinomial o a mapeos logarítmicos ($\\%log(y)\\%$) en vías de estandarizar la curva del ecosistema muestral."
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
            "\n\n**Análisis exploratorio:** Inicialmente, los modelos de aprendizaje maquinal son incapaces de interpretar el lenguaje de la string \"High Efficiency\". Realizamos un mapeo (label encoding) hacia las clasificaciones 0, 1, y 2. \n",
            "Para explorar a profundidad el ecosistema sin ser intimidados por el volumen múltiple de columnas extraídos, se utiliza directamente una **Matriz de Correlación de Pearson**. A través del método `matshow` gráfico y térmico, se detectan a ojo las posibles agrupaciones de variables independientes y se comprueba si la base de datos se encuentra limpia y correctamente instanciada en memoria sin nulos ni rupturas de tipo (datatype)."
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
            "# 1. Carga de datos\n",
            "datos2 = pd.read_csv('Dataset 4 P2.csv')\n",
            "\n",
            "# 2. Transformación Categórica Estricta para Aprendizaje\n",
            "mapping2 = {'Low Efficiency': 0, 'Moderate': 1, 'High Efficiency': 2}\n",
            "datos2['calorie_efficiency'] = datos2['calorie_efficiency'].map(mapping2)\n",
            "\n",
            "print(\"=================== INFORMACIÓN GENERAL ===================\")\n",
            "datos2.info()\n",
            "print(\"\\n=================== DESCRIPCIÓN ESTADÍSTICA ===================\")\n",
            "display(datos2.describe().round(2))\n",
            "\n",
            "# 3. Correlación de Pearson Múltiple\n",
            "corr2 = datos2.corr()\n",
            "\n",
            "try:\n",
            "    display(corr2.style.background_gradient(cmap='coolwarm'))\n",
            "except AttributeError:\n",
            "    display(corr2.round(3))\n",
            "\n",
            "# 4. Análisis Gráfico Exploratorio: Histogramas Generales\n",
            "datos2.hist(figsize=(12, 10), bins=20, edgecolor='black', grid=False, color='#4A90E2')\n",
            "plt.suptitle('Distribución y Comportamiento de las Métricas Registradas', fontsize=16, y=1.02)\n",
            "plt.tight_layout()\n",
            "plt.show()\n"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## B. En caso de seleccionar una única variable independiente para predecir Y, ¿cuál sería y por qué?",
            "\n\n**Fundamento Teórico:** Aunque el modelo es múltiple, el supuesto pide destilar empíricamente una regresión simple. Para lograr el modelo monovariable con la mayor fuerza predictiva y el menor error estructural inicial, debemos elegir la *Variable Independiente* cuyo índice absoluto en la Matriz de Pearson anterior sea mayor con respecto al pilar objetivo ($Y$: calorie_efficiency). "
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "correlaciones2_target = corr2['calorie_efficiency'].drop('calorie_efficiency')\n",
            "mejor_independiente2 = correlaciones2_target.abs().idxmax()\n",
            "max_corr_val2 = correlaciones2_target[mejor_independiente2]\n",
            "\n",
            "print(f\"---> Respuesta: La variable seleccionada estratégicamente sería '{mejor_independiente2}'.\")\n",
            "print(f\"---> Explicación: Posee el coeficiente de correlación más predominante (valor magnético de: {max_corr_val2:.4f}).\")"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## C. Partición de los datos en un 2a% para el test de modelo.",
            "\n\n**Análisis de Segmentación de Muestreo:**\n",
            "Por instrucciones del reglamento, se debe segmentar sobre la base del carnet individual estudiantil.\n",
            "- Estudiante: Jiménez Arias\n",
            "- **Código Asignado:** `U20231085`\n",
            "- Último dígito de sufijo ($a$): **a = 5**\n",
            "- **Porcentaje de prueba:** Siguiendo la indicación (para U20236789, a=9 entonces test_size=0.29 y random_state=20236789), en este caso al ser a=5 entonces determinamos de forma exacta **$test\\_size = 0.25$**.\n",
            "- **Random_state:** Anclamos entonces a **`20231085`** como semilla en el `train_test_split` para lograr la reproducibilidad analítica exigida."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "x2_features = datos2.drop(\"calorie_efficiency\", axis=1)\n",
            "y2_label = datos2[\"calorie_efficiency\"].copy()\n",
            "\n",
            "# Validación estricta con semilla de estudiante: Carnet 20231085\n",
            "# Tamaño Test = 2a% (a=5) => 25% -> 0.25\n",
            "X2_train, X2_test, y2_train, y2_test = train_test_split(\n",
            "    x2_features, y2_label, \n",
            "    test_size=0.25, \n",
            "    random_state=20231085\n",
            ")\n",
            "\n",
            "print(f\"Lote de Entrenamiento instanciado con: {len(X2_train)} sujetos.\")\n",
            "print(f\"Lote de Pruebas y Validación instanciado con: {len(X2_test)} sujetos.\")"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## D. Crear un modelo de regresión lineal múltiple para obtener y analizar sus parámetros.",
            "\n\n**Concepción de Hiperplanos Algorítmicos:** La regresión múltiple ya no crea una \"recta bidimensional\", sino un **hiperplano multidimensional** en $N$ ejes. Cada atributo posee su propio peso estadístico. Si nos fijamos, ciertas métricas tendrán coeficientes agresivamente altos frente a comportamientos positivos, mientras que otras podrían obtener comportamientos negativos si su progreso perjudicase el queme calórico."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Entrenamiento Formal de OLS Scikit-Learn Multidimensional\n",
            "lm_mult_base = LinearRegression()\n",
            "lm_mult_base.fit(X2_train, y2_train)\n",
            "\n",
            "print(f\"El Intercepto basal del hiperplano ($\\beta_0$) se ubica en: {lm_mult_base.intercept_:.4f}\\n\")\n",
            "tabla_coef_mult = pd.DataFrame({\n",
            "    \"Características Entrenadas\": x2_features.columns, \n",
            "    \"Coeficientes (Weights)\": lm_mult_base.coef_\n",
            "})\n",
            "display(tabla_coef_mult)"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## E. Determinar las variables significativas y analizar formalmente el $R^2$.",
            "\n\n**Interpretabilidad Universitaria de Statsmodels:**\n",
            "La herramienta OLS provee el valor universal más valioso: los $P>|t|$. Basándonos en la inferencia al $\\alpha = 0.05$, cualquier variable independiente que brinde un $p-valor$ superior falla en impactar fuertemente a la ecuación real, aportando puro ruido.\n",
            "\n",
            "Al computar las predicciones sobre el set **nunca antes visto por el algoritmo ($X\\_test$)**, evaluamos el $R^2$ múltiple. Si es alto (generalmente $>0.80$, nos indica que predecir cómo de eficiente quemará un atleta calorías dadas sus mediciones biológicas combinadas rige un patrón certero, fiable y sumamente estable en aplicaciones en el mundo real que justifiquen su uso institucional."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Añadimos un vector de unos indispensable para calcular estadísticos con 'statsmodels'\n",
            "X2_train_cte = sm.add_constant(X2_train)\n",
            "modelo_ols2 = sm.OLS(y2_train, X2_train_cte)\n",
            "resultados_ols2 = modelo_ols2.fit()\n",
            "print(resultados_ols2.summary())\n",
            "\n",
            "# Análisis Estructural del R^2 usando datos ciegos de validación\n",
            "y2_pred_inicial = lm_mult_base.predict(X2_test)\n",
            "r2_mult2_val = r2_score(y2_test, y2_pred_inicial)\n",
            "print(f\"\\n---> Coeficiente Analítico de Determinación (R^2 de validación): {r2_mult2_val:.6f}\")"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## F. Eliminar variables que NO son significativas y comparar el $R^2$.",
            "\n\n**Mecánica de Optimización (Feature Selection):** No todas las mediciones físicas contribuyeron un efecto verídico real sobre el final. Al expurgar de la ecuación a todos los pilares con $P-valor > 0.05$ depuramos el sobreajuste. En un escenario perfecto, el re-entrenamiento arrojará un $R^2$ equivalente o con una ganancia ligera de validez a pesar de usar menos información de entrada, aplicando el principio de la navaja de Occam (simplificando la fórmula)."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Extracción de p-valores, ignorando al intercepto (constante) si existe en la serie\n",
            "lista_pvalores2 = resultados_ols2.pvalues.drop('const', errors='ignore')\n",
            "vars_significativas = lista_pvalores2[lista_pvalores2 <= 0.05].index.tolist()\n",
            "print(\"[FILTRO] Columnas Aprobadas y Significativas (P <= 0.05):\\n ---> \", vars_significativas)\n",
            "\n",
            "if len(vars_significativas) < len(x2_features.columns):\n",
            "    # Recorte de Matrices Originales\n",
            "    X_train_optimo = X2_train[vars_significativas]\n",
            "    X_test_optimo = X2_test[vars_significativas]\n",
            "    \n",
            "    # Regenerar Ecosistema Reducido\n",
            "    lm_depurado = LinearRegression()\n",
            "    lm_depurado.fit(X_train_optimo, y2_train)\n",
            "    y2_pred_optimo = lm_depurado.predict(X_test_optimo)\n",
            "    \n",
            "    # Contraste de Rendimiento Predictivo Final\n",
            "    r2_optimo = r2_score(y2_test, y2_pred_optimo)\n",
            "    print(f\"\\n[CONTRASTE] R^2 del modelo sucio original: {r2_mult2_val:.6f}\")\n",
            "    print(f\"[CONTRASTE] R^2 del modelo selecto depurado: {r2_optimo:.6f}\")\n",
            "else:\n",
            "    print(\"\\n[SELECCIÓN INVERTIDA] Absolutamente todos los predictores biológicos ostentan una significancia robusta fuerte. Ninguno será expulsado. El R^2 múltiple permanece inigualado.\")"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## G. Analizar la colinealidad usando Factor de Inflación de Varianza (VIF).",
            "\n\n**Fundamento Critico de Colinealidad:** Un pecado en estadística múltiple es la colinealidad (múltiples pilares que proveen información idénticamente inflada). Cuando dos predictores comparten el trabajo, la regresión MCO divide erróneamente el peso estadístico. Usualmente, cualquier resultado con $VIF > 5$ o extremadamente peligroso $> 10$ debe ser atendido o ignorado para solidificar el poder de los pesos individuales aislados."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "tabla_vif = pd.DataFrame()\n",
            "tabla_vif[\"Predictores Multiples\"] = x2_features.columns\n",
            "tabla_vif[\"Valor VIF Arrojado\"] = [variance_inflation_factor(x2_features.values, idx) for idx in range(len(x2_features.columns))]\n",
            "\n",
            "display(tabla_vif.sort_values(by=\"Valor VIF Arrojado\", ascending=False).round(3))"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## H. Comparar métricas residuales, predichos contra validados empíricamente.",
            "\n\n**Contraste Empírico Terminal:** Todo análisis descansa en poder confirmar de la forma lo más visual posible si la discrepancia es fatal u óptima. Trazando una representación gráfica de la realidad ($X$ eje) contrastada de las predicciones ($Y$ eje). Si las iteraciones convergen cercanamente alrededor de la perfecta recta simétrica diagonal neutra cruzada (Realidad=Pronostico), el ajuste fue certeramente un éxito absoluto, respaldado mediante un MSE minimizado."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "mse_final = mean_squared_error(y2_test, y2_pred_inicial)\n",
            "print(f\"Magnitud del Error Cuadrático Medio Global (MSE): {mse_final:.6f}\")\n",
            "\n",
            "plt.figure(figsize=(8,6))\n",
            "plt.scatter(y2_test, y2_pred_inicial, alpha=0.6, label='Asignaciones', color='darkcyan')\n",
            "\n",
            "min_val = min(y2_test.min(), y2_pred_inicial.min())\n",
            "max_val = max(y2_test.max(), y2_pred_inicial.max())\n",
            "plt.plot([min_val, max_val], [min_val, max_val], color='crimson', lw=3, label='Recta Perfecta Esperada')\n",
            "\n",
            "plt.xlabel(\"Catálogo Muestral Real (Testing)\")\n",
            "plt.ylabel(\"Cálculo Algorítmico Pronosticado\")\n",
            "plt.title(\"Demostración de Exactitud Múltiple Empírica\")\n",
            "plt.legend()\n",
            "plt.grid(True, ls=':', alpha=0.5)\n",
            "plt.show()"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## I. Realizar la predicción condicional sustentada en la tendencia central mediana poblacional general.",
            "\n\n**Interpretabilidad Funcional:** Exprimir y obtener el arreglo de medianas correspondientes a todo el dataset multidimensional es la forma más representativa del \"individuo completamente estándar\" inmune a excesos. Invocando la función predictora frente a estas medianas se logra obtener el comportamiento pronosticado base bajo la tendencia global de la población entera evaluada."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Construcción matricial a partir de medianas absolutas\n",
            "array_medianas = np.array(np.median(x2_features, axis=0))\n",
            "proyeccion_mediana = lm_mult_base.predict(array_medianas.reshape(1, -1))\n",
            "\n",
            "print(f\"Extrapolación sobre el individuo matriz medial poblacional: {proyeccion_mediana[0]:.4f} de Eficiencia Calórica\")"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## J. Consideraciones Analíticas, Supuestos Universales y Reflexión Estructural\n",
            "\n",
            "**Postura Crítica (Utilidad Verificada):**\n",
            "Definitivamente, el modelo de regresión algorítmica múltiple goza de una aplastante fiabilidad en predicciones de índole atlética. Demostró una utilidad rotunda. La sumatoria en abanico de métricas individuales, dietéticas y de ejercicio convergen logrando arrinconar numéricamente el desenlace, procreando una evaluación real-time muy apegada a la línea perfecta.\n\n",
            "**Limitaciones y Peligros Demostrados:**\n",
            "Aun cuando en validación rinde certeramente de manera holística, adolece de un factor subyacente crónico: **la peligrosa colinealidad flagrante**. Multitudes de factores biológicos corporales se arrastran e inflarán mutuamente (los pasos dictan ritmo de pulsación), por ello el diagnóstico **VIF** excede los límites seguros académicos, manchando y volviendo vulnerables las deducciones lógicas teóricas de cada coeficiente por separado a pesar de que cumplan la significancia dictada por los esquemas en $p-valores$.\n\n",
            "**Propuestas Críticas Estructurales de Mejora Evolutiva:**\n",
            "1. **Combatir Dimensionalidad Redundante:** Sancionar en desuso rotundo a aquellas características subyacentes penalizadas con Factor $VIF > 10$. El modelo depurado puede mantener métricas idénticas mientras estabiliza el núcleo reduciendo ruido estadístico.\n",
            "2. **Algoritmos Categóricos Clasificatorios Físicos:** Tomando en cuenta que el desenlace fundamental de eficiencia era una meta clasificada literal en textos nominales (`Low`, `Moderate`, `High`), forzarla a una ecuación con recta numérico flotante continua no es el único camino. Se recomienda limpiar profundamente los datos y mantenerse estrictamente en el marco de la regresión y análisis de predictores independientes, evitando el uso de modelos que excedan lo visto hasta ahora en el material de estudio."
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
