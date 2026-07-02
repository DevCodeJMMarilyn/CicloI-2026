import sqlite3
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


DB_PATH = Path(__file__).with_name("novaretail.db")


@st.cache_data
def cargar_datos():
    query = """
        SELECT
            v.VentaID,
            v.FechaVenta,
            c.NombreCliente,
            c.Genero,
            c.Edad,
            c.Segmento,
            r.Pais,
            r.Departamento,
            r.Municipio,
            r.Moneda,
            p.NombreProducto,
            p.Categoria,
            p.Marca,
            v.Cantidad,
            v.PrecioUnitario,
            v.Descuento,
            v.TotalVenta,
            v.MetodoPago,
            v.CanalVenta
        FROM FactVentas v
        INNER JOIN DimCliente c ON v.ClienteID = c.ClienteID
        INNER JOIN DimRegion r ON c.RegionID = r.RegionID
        INNER JOIN DimProducto p ON v.ProductoID = p.ProductoID;
    """

    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql_query(query, conn)

    df["FechaVenta"] = pd.to_datetime(df["FechaVenta"])
    df["TotalVenta"] = pd.to_numeric(df["TotalVenta"], errors="coerce")
    return df


def calcular_crecimiento_mensual(ventas_mensuales):
    if len(ventas_mensuales) < 2:
        return 0

    venta_actual = ventas_mensuales["TotalVentas"].iloc[-1]
    venta_anterior = ventas_mensuales["TotalVentas"].iloc[-2]

    if venta_anterior == 0:
        return 0

    return ((venta_actual - venta_anterior) / venta_anterior) * 100


st.set_page_config(
    page_title="NovaRetail Analytics",
    layout="wide",
)

st.title("NovaRetail Analytics")
st.caption("Dashboard BI de ventas - Python | SQL | Pandas | Plotly | Streamlit")

if not DB_PATH.exists():
    st.error("No se encontro novaretail.db. Ejecuta primero: python crear_base_datos.py")
    st.stop()

df = cargar_datos()

st.sidebar.header("Filtros")

categorias = sorted(df["Categoria"].dropna().unique())
categorias_seleccionadas = st.sidebar.multiselect(
    "Categoria",
    options=categorias,
    default=categorias,
)

fecha_min = df["FechaVenta"].min().date()
fecha_max = df["FechaVenta"].max().date()
rango_fechas = st.sidebar.date_input(
    "Rango de fechas",
    value=(fecha_min, fecha_max),
    min_value=fecha_min,
    max_value=fecha_max,
)

if len(rango_fechas) == 2:
    fecha_inicio, fecha_fin = rango_fechas
else:
    fecha_inicio, fecha_fin = fecha_min, fecha_max

df_filtrado = df[
    (df["Categoria"].isin(categorias_seleccionadas))
    & (df["FechaVenta"].dt.date >= fecha_inicio)
    & (df["FechaVenta"].dt.date <= fecha_fin)
].copy()

if df_filtrado.empty:
    st.warning("No hay datos para los filtros seleccionados.")
    st.stop()

ventas_totales = df_filtrado["TotalVenta"].sum()
ticket_promedio = df_filtrado["TotalVenta"].mean()

ventas_categoria = (
    df_filtrado.groupby("Categoria", as_index=False)
    .agg(TotalVentas=("TotalVenta", "sum"), TicketPromedio=("TotalVenta", "mean"))
    .sort_values("TotalVentas", ascending=False)
)

categoria_lider = ventas_categoria.iloc[0]["Categoria"]

ventas_mensuales = (
    df_filtrado.groupby(pd.Grouper(key="FechaVenta", freq="ME"))
    .agg(TotalVentas=("TotalVenta", "sum"))
    .reset_index()
)

crecimiento_mensual = calcular_crecimiento_mensual(ventas_mensuales)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Ventas totales", f"${ventas_totales:,.2f}")
col2.metric("Ticket promedio", f"${ticket_promedio:,.2f}")
col3.metric("Categoria lider", categoria_lider)
col4.metric("Crecimiento mensual", f"{crecimiento_mensual:.2f}%")

st.divider()

col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    fig_bar = px.bar(
        ventas_categoria,
        x="Categoria",
        y="TotalVentas",
        text_auto=",.2f",
        title="Ventas por categoria",
        labels={"Categoria": "Categoria", "TotalVentas": "Ventas totales (USD)"},
        color="Categoria",
    )
    fig_bar.update_layout(
        template="plotly_white",
        title_x=0.5,
        showlegend=False,
        yaxis_tickprefix="$",
        yaxis_tickformat=",.2f",
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with col_graf2:
    fig_pie = px.pie(
        ventas_categoria,
        names="Categoria",
        values="TotalVentas",
        title="Participacion porcentual por categoria",
        hole=0.35,
    )
    fig_pie.update_layout(template="plotly_white", title_x=0.5)
    fig_pie.update_traces(textposition="inside", textinfo="percent+label")
    st.plotly_chart(fig_pie, use_container_width=True)

fig_line = px.line(
    ventas_mensuales,
    x="FechaVenta",
    y="TotalVentas",
    markers=True,
    title="Crecimiento mensual de ventas",
    labels={"FechaVenta": "Mes", "TotalVentas": "Ventas totales (USD)"},
)
fig_line.update_traces(line=dict(width=3), marker=dict(size=8))
fig_line.update_layout(
    template="plotly_white",
    title_x=0.5,
    hovermode="x unified",
    yaxis_tickprefix="$",
    yaxis_tickformat=",.2f",
    xaxis_tickformat="%b %Y",
)
st.plotly_chart(fig_line, use_container_width=True)

st.subheader("Ticket promedio por categoria")
fig_ticket = px.bar(
    ventas_categoria.sort_values("TicketPromedio", ascending=False),
    x="Categoria",
    y="TicketPromedio",
    text_auto=",.2f",
    title="Ticket promedio por categoria",
    labels={"Categoria": "Categoria", "TicketPromedio": "Ticket promedio (USD)"},
    color="Categoria",
)
fig_ticket.update_layout(
    template="plotly_white",
    title_x=0.5,
    showlegend=False,
    yaxis_tickprefix="$",
    yaxis_tickformat=",.2f",
)
st.plotly_chart(fig_ticket, use_container_width=True)

st.subheader("Detalle de ventas filtradas")
st.dataframe(
    df_filtrado.sort_values("FechaVenta", ascending=False),
    use_container_width=True,
    hide_index=True,
)
