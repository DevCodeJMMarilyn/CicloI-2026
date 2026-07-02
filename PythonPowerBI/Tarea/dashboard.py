import sqlite3
import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.io as pio

# =========================================
# CONFIGURACIÓN
# =========================================
st.set_page_config(page_title="Dashboard BI - Tienda", layout="wide")
pio.templates.default = "plotly_dark"

st.title("Dashboard BI - Tienda")

# =========================================
# CONEXIÓN
# =========================================
conn = sqlite3.connect("tienda.db")

# =========================================
# DATA BASE
# Se centraliza para permitir filtros dinámicos
# =========================================
df = pd.read_sql("""
SELECT
    v.id_venta,
    p.producto,
    p.categoria,
    v.cantidad,
    v.precio_unitario,
    v.cantidad * v.precio_unitario AS total,
    t.mes,
    t.mes_nombre
FROM Ventas v
JOIN Productos p ON v.id_producto = p.id_producto
JOIN Tiempo t ON v.id_tiempo = t.id_tiempo
""", conn)

# =========================================
# FILTROS
# =========================================
st.sidebar.header("Filtros")

categorias = sorted(df["categoria"].unique())

meses_orden = [
    "Enero","Febrero","Marzo","Abril","Mayo","Junio",
    "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"
]

meses = sorted(df["mes_nombre"].unique(), key=lambda x: meses_orden.index(x))

cat_sel = st.sidebar.selectbox("Categoría", ["Todas"] + categorias)
mes_sel = st.sidebar.selectbox("Mes", ["Todos"] + meses)

df_f = df.copy()

if cat_sel != "Todas":
    df_f = df_f[df_f["categoria"] == cat_sel]

if mes_sel != "Todos":
    df_f = df_f[df_f["mes_nombre"] == mes_sel]

if df_f.empty:
    st.warning("No hay datos con esos filtros")
    st.stop()

# =========================================
# KPIs
# =========================================
ventas_totales = df_f["total"].sum()
ticket = df_f["total"].mean()

ventas_m = df_f.groupby(["mes","mes_nombre"], as_index=False)["total"].sum().sort_values("mes")
ventas_m["crecimiento"] = ventas_m["total"].pct_change() * 100

crec = ventas_m["crecimiento"].dropna()
ultimo_crec = crec.iloc[-1] if not crec.empty else 0

col1, col2, col3 = st.columns(3)

col1.metric("Ventas Totales", f"${ventas_totales:,.0f}")
col2.metric("Ticket Promedio", f"${ticket:,.0f}")
col3.metric("Crecimiento", f"{ultimo_crec:.1f}%", delta=f"{ultimo_crec:.1f}%")

st.markdown("---")

# =========================================
# PALETA DE COLORES
# =========================================
colores = ["#6C63FF", "#0051AD", "#C700E6", "#FFBE0B"]

# =========================================
# GRÁFICAS LADO A LADO
# Se mejora distribución visual del dashboard
# =========================================

# --- FILA 1 ---
colA, colB = st.columns(2)

# Ventas por categoría (horizontal)
ventas_cat = df_f.groupby("categoria", as_index=False)["total"].sum()

fig1 = px.bar(
    ventas_cat,
    x="total",
    y="categoria",
    orientation="h",
    color="categoria",
    color_discrete_sequence=colores,
    text_auto=True
)

fig1.update_layout(title="Ventas por Categoría", title_x=0.5)

colA.plotly_chart(fig1, use_container_width=True)

# Pie (donut mejorado)
fig2 = px.pie(
    ventas_cat,
    values="total",
    names="categoria",
    hole=0.55,
    color_discrete_sequence=colores
)

fig2.update_traces(textinfo="percent+label")

fig2.update_layout(title="Distribución de Ventas", title_x=0.5)

colB.plotly_chart(fig2, use_container_width=True)

# --- FILA 2 ---
colC, colD = st.columns(2)

# Ventas por mes (área)
fig3 = px.area(
    ventas_m,
    x="mes_nombre",
    y="total",
    line_shape="spline"
)

fig3.update_traces(line=dict(color="#71A7FF"))

fig3.update_layout(title="Ventas en el Tiempo", title_x=0.5)

colC.plotly_chart(fig3, use_container_width=True)

# Crecimiento con línea base
fig4 = px.line(
    ventas_m,
    x="mes_nombre",
    y="crecimiento",
    markers=True
)

fig4.add_hline(y=0, line_dash="dash", line_color="gray")

fig4.update_traces(line=dict(color="#FFBE0B", width=3))

fig4.update_layout(title="Crecimiento (%)", title_x=0.5)

colD.plotly_chart(fig4, use_container_width=True)

# --- FILA 3 ---
st.markdown("---")

colE, colF = st.columns(2)

# Ticket promedio
ticket_cat = df_f.groupby("categoria", as_index=False)["total"].mean()
ticket_cat.columns = ["categoria","ticket"]

fig5 = px.bar(
    ticket_cat,
    x="categoria",
    y="ticket",
    color="categoria",
    color_discrete_sequence=colores,
    text_auto=".2f"
)

fig5.update_layout(title="Ticket Promedio", title_x=0.5, showlegend=False)

colE.plotly_chart(fig5, use_container_width=True)

# Top productos
top = df_f.groupby("producto", as_index=False)["cantidad"].sum().sort_values("cantidad", ascending=False).head(5)

fig6 = px.bar(
    top,
    x="producto",
    y="cantidad",
    color="cantidad",
    color_continuous_scale="Blues",
    text_auto=True
)

fig6.update_layout(title="Top Productos", title_x=0.5)

colF.plotly_chart(fig6, use_container_width=True)

# =========================================
# CIERRE
# =========================================
conn.close()