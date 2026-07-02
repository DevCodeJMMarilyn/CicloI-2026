# IMPORTACIÓN DE LIBRERÍAS
# ========================
import pandas as pd
import plotly.express as px
import webbrowser
import os


# CREACIÓN DE LOS DATOS DE EJEMPLO
# ================================
data = {
    'juego': ['Juego A', 'Juego B', 'Juego C', 'Juego D', 'Juego E'],
    'ventas_globales': [1.5, 2.5, 4.5, 0.8, 8.7],
    'ventas_america': [0.6, 0.9, 0.6, 0.5, 1.2],
    'ventas_europa': [2.4, 1.3, 0.2, 0.7, 2.2],
    'genero': ['Accion', 'Aventura', 'Puzzle', 'Accion', 'Deportes']
}

# CONVERSIÓN A DATAFRAME
# ======================
df = pd.DataFrame(data)

# CREACIÓN DEL GRÁFICO
# ====================
fig = px.scatter(
    df,
    x='ventas_america',
    y='ventas_europa',
    size='ventas_globales',
    color='genero',
    hover_name='juego',
    title="Ventas de Videojuegos"
)

# GUARDADO Y VISUALIZACIÓN
# ========================
fig.write_html("grafico_videojuegos.html")
webbrowser.open('file://' + os.path.realpath("grafico_videojuegos.html"))