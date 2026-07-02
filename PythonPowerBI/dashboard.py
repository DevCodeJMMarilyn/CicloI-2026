import sqlite3
import pandas as pd
import plotly.express as px
import streamlit as st

# =========================================
# CONFIGURACIÓN DE LA PÁGINA
# =========================================
st.set_page_config(page_title="Dashboard BI - Tienda", layout="wide")
st.title("Dashboard BI - Tienda")

# =========================================
# CONEXIÓN A BASE DE DATOS
# =========================================
conn = sqlite3.connect("tienda.db")

# =========================================
# 1. VENTAS TOTALES
# =========================================
ventas_totales = pd.read_sql("""
SELECT SUM(cantidad * precio_unitario) AS total
FROM Ventas
""", conn)

# =========================================
# 2. TICKET PROMEDIO
# =========================================
ticket = pd.read_sql("""
SELECT 
    COUNT(*) AS total_ventas,
    SUM(cantidad * precio_unitario)/COUNT(*) AS ticket_promedio
FROM Ventas
""", conn)

# =========================================
# 3. VENTAS POR CATEGORÍA
# =========================================
ventas_categoria = pd.read_sql("""
SELECT p.categoria, SUM(v.cantidad * v.precio_unitario) AS ingresos
FROM Ventas v
JOIN Productos p ON v.id_producto = p.id_producto
GROUP BY p.categoria
""", conn)

# =========================================
# 4. VENTAS POR MES
# =========================================
ventas_mes = pd.read_sql("""
SELECT t.mes_nombre, SUM(v.cantidad * v.precio_unitario) AS ingresos
FROM Ventas v
JOIN Tiempo t ON v.id_tiempo = t.id_tiempo
GROUP BY t.mes, t.mes_nombre
ORDER BY t.mes
""", conn)

# =========================================
# 5. TOP PRODUCTOS
# =========================================
top_productos = pd.read_sql("""
SELECT p.producto, SUM(v.cantidad) AS total_vendido
FROM Ventas v
JOIN Productos p ON v.id_producto = p.id_producto
GROUP BY p.producto
ORDER BY total_vendido DESC
LIMIT 5
""", conn)

# =========================================
# DASHBOARD - KPIs
# =========================================
st.subheader("Indicadores Clave")

col1, col2 = st.columns(2)

col1.metric(" Ventas Totales", f"${ventas_totales['total'][0]:,.2f}")
col2.metric("Ticket Promedio", f"${ticket['ticket_promedio'][0]:,.2f}")

# =========================================
# GRÁFICOS
# =========================================

# Gráfico de barras: Ventas por categoría
st.subheader(" Ventas por Categoría")
fig_cat = px.bar(
    ventas_categoria,
    x="categoria",
    y="ingresos",
    title="Ventas por Categoría",
    color="categoria",
    text_auto=True
)
st.plotly_chart(fig_cat, use_container_width=True)

# Gráfico de líneas: Ventas por mes
st.subheader("Ventas por Mes")
fig_mes = px.line(
    ventas_mes,
    x="mes_nombre",
    y="ingresos",
    title="Ventas por Mes",
    markers=True
)
st.plotly_chart(fig_mes, use_container_width=True)

# Gráfico de barras: Top productos
st.subheader("Top 5 Productos Más Vendidos")
fig_top = px.bar(
    top_productos,
    x="producto",
    y="total_vendido",
    title="Top 5 Productos",
    color="producto",
    text_auto=True
)
st.plotly_chart(fig_top, use_container_width=True)

# Cerrar conexión a la base de datos
conn.close()