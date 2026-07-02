import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="Rutas del Sabor - Restaurantes",
    layout="wide"
)

st.title("Rutas del Sabor - Division Restaurantes")
st.caption("Dashboard Grupo A: analisis de reclamos en productos perecederos")


def porcentaje_reclamos(serie):
    return serie.mean() * 100


try:
    df = pd.read_excel("restaurantes.xlsx", engine="openpyxl")
    df.columns = df.columns.str.strip()

    df["Reclamo_Binario"] = (
        df["Reclamo"]
        .astype(str)
        .str.strip()
        .str.lower()
        .str.startswith("s")
        .astype(int)
    )

    df["Hora_Entrega_Redondeada"] = (
        df["Tiempo_Entrega_horas"]
        .round()
        .astype(int)
    )

    df["Rango_Temperatura"] = pd.cut(
        df["Temperatura_Salida_C"],
        bins=[-100, 2, 4, 6, 100],
        labels=["Hasta 2 C", "3 a 4 C", "5 a 6 C", "Mas de 6 C"]
    )

    zonas = ["Todas"] + sorted(df["Zona"].dropna().unique().tolist())
    productos = ["Todos"] + sorted(df["Tipo_Producto"].dropna().unique().tolist())

    col_filtro1, col_filtro2 = st.columns(2)

    zona = col_filtro1.selectbox("Filtrar por zona", zonas)
    producto = col_filtro2.selectbox("Filtrar por tipo de producto", productos)

    df_filtrado = df.copy()

    if zona != "Todas":
        df_filtrado = df_filtrado[df_filtrado["Zona"] == zona]

    if producto != "Todos":
        df_filtrado = df_filtrado[df_filtrado["Tipo_Producto"] == producto]

    total_pedidos = len(df_filtrado)
    total_reclamos = int(df_filtrado["Reclamo_Binario"].sum())
    tasa_reclamos = porcentaje_reclamos(df_filtrado["Reclamo_Binario"])
    correlacion = df_filtrado["Distancia_km"].corr(df_filtrado["Reclamo_Binario"])

    reclamos_por_hora = (
        df_filtrado.groupby("Hora_Entrega_Redondeada")
        .agg(
            Reclamos_Pct=("Reclamo_Binario", porcentaje_reclamos),
            Pedidos=("ID_Pedido", "count")
        )
        .reset_index()
        .sort_values("Hora_Entrega_Redondeada")
    )

    umbral_reclamos = reclamos_por_hora[
        reclamos_por_hora["Reclamos_Pct"] > tasa_reclamos
    ]

    if not umbral_reclamos.empty:
        umbral = int(umbral_reclamos.iloc[0]["Hora_Entrega_Redondeada"])
    else:
        umbral = None

    zona_mayor = (
        df_filtrado.groupby("Zona")["Reclamo_Binario"]
        .mean()
        .sort_values(ascending=False)
    )

    producto_mayor = (
        df_filtrado.groupby("Tipo_Producto")["Reclamo_Binario"]
        .mean()
        .sort_values(ascending=False)
    )

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Pedidos analizados", f"{total_pedidos}")
    col2.metric("Reclamos", f"{total_reclamos}")
    col3.metric("Porcentaje de reclamos", f"{tasa_reclamos:.1f}%")
    col4.metric(
        "Correlacion distancia-reclamo",
        "N/D" if pd.isna(correlacion) else f"{correlacion:.2f}"
    )

    st.subheader("Preguntas clave")

    respuesta1 = (
        "N/D"
        if zona_mayor.empty
        else f"{zona_mayor.index[0]} ({zona_mayor.iloc[0] * 100:.1f}%)"
    )

    respuesta3 = (
        "No se detecta un umbral claro"
        if umbral is None
        else f"A partir de {umbral} horas"
    )

    respuesta4 = (
        "N/D"
        if producto_mayor.empty
        else f"{producto_mayor.index[0]} ({producto_mayor.iloc[0] * 100:.1f}%)"
    )

    col_a, col_b, col_c = st.columns(3)
    col_a.info(f"Zona con mayor porcentaje de reclamos: {respuesta1}")
    col_b.info(f"Umbral de tiempo: {respuesta3}")
    col_c.info(f"Producto mas sensible: {respuesta4}")

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "Zonas y dias",
            "Distancia y tiempo",
            "Productos",
            "Temperatura"
        ]
    )

    with tab1:
        col_zona, col_dia = st.columns(2)

        reclamos_zona = (
            df_filtrado.groupby("Zona")
            .agg(
                Reclamos=("Reclamo_Binario", "sum"),
                Pedidos=("ID_Pedido", "count"),
                Porcentaje_Reclamos=("Reclamo_Binario", porcentaje_reclamos)
            )
            .reset_index()
            .sort_values("Porcentaje_Reclamos", ascending=False)
        )

        fig_zona = px.bar(
            reclamos_zona,
            x="Zona",
            y="Porcentaje_Reclamos",
            color="Zona",
            text="Porcentaje_Reclamos",
            title="Porcentaje de reclamos por zona"
        )
        fig_zona.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig_zona.update_layout(yaxis_title="% reclamos", showlegend=False)
        col_zona.plotly_chart(fig_zona, use_container_width=True)

        orden_dias = [
            "Lunes",
            "Martes",
            "Miercoles",
            "Miércoles",
            "Jueves",
            "Viernes",
            "Sábado",
            "Domingo"
        ]

        reclamos_dia = (
            df_filtrado.groupby("Dia_Semana")
            .agg(
                Reclamos=("Reclamo_Binario", "sum"),
                Pedidos=("ID_Pedido", "count"),
                Porcentaje_Reclamos=("Reclamo_Binario", porcentaje_reclamos)
            )
            .reset_index()
        )

        fig_dia = px.bar(
            reclamos_dia,
            x="Dia_Semana",
            y="Reclamos",
            color="Porcentaje_Reclamos",
            category_orders={"Dia_Semana": orden_dias},
            text="Reclamos",
            title="Cantidad de reclamos por dia de la semana"
        )
        fig_dia.update_layout(xaxis_title="Dia", yaxis_title="Reclamos")
        col_dia.plotly_chart(fig_dia, use_container_width=True)

        st.dataframe(reclamos_zona, use_container_width=True)

    with tab2:
        col_distancia, col_tiempo = st.columns(2)

        fig_distancia = px.scatter(
            df_filtrado,
            x="Distancia_km",
            y="Tiempo_Entrega_horas",
            color="Reclamo",
            size="Cantidad_kg",
            hover_data=[
                "ID_Pedido",
                "Restaurante",
                "Zona",
                "Tipo_Producto",
                "Temperatura_Salida_C"
            ],
            title="Distancia recorrida vs tiempo de entrega"
        )
        fig_distancia.update_layout(
            xaxis_title="Distancia (km)",
            yaxis_title="Tiempo de entrega (horas)"
        )
        col_distancia.plotly_chart(fig_distancia, use_container_width=True)

        fig_tiempo = px.line(
            reclamos_por_hora,
            x="Hora_Entrega_Redondeada",
            y="Reclamos_Pct",
            markers=True,
            text="Pedidos",
            title="Porcentaje de reclamos segun horas de entrega"
        )
        fig_tiempo.update_layout(
            xaxis_title="Horas de entrega",
            yaxis_title="% reclamos"
        )
        if umbral is not None:
            fig_tiempo.add_vline(
                x=umbral,
                line_dash="dash",
                line_color="red",
                annotation_text=f"Umbral: {umbral} h"
            )
        col_tiempo.plotly_chart(fig_tiempo, use_container_width=True)

        st.write(
            "Interpretacion: una correlacion positiva indica que, al aumentar "
            "la distancia, tambien tienden a aumentar los reclamos."
        )

    with tab3:
        sensibilidad_producto = (
            df_filtrado.groupby("Tipo_Producto")
            .agg(
                Reclamos=("Reclamo_Binario", "sum"),
                Pedidos=("ID_Pedido", "count"),
                Porcentaje_Reclamos=("Reclamo_Binario", porcentaje_reclamos),
                Tiempo_Promedio=("Tiempo_Entrega_horas", "mean")
            )
            .reset_index()
            .sort_values("Porcentaje_Reclamos", ascending=False)
        )

        fig_producto = px.bar(
            sensibilidad_producto,
            x="Tipo_Producto",
            y="Porcentaje_Reclamos",
            color="Tiempo_Promedio",
            text="Porcentaje_Reclamos",
            title="Sensibilidad del producto al tiempo de entrega"
        )
        fig_producto.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig_producto.update_layout(
            xaxis_title="Tipo de producto",
            yaxis_title="% reclamos"
        )
        st.plotly_chart(fig_producto, use_container_width=True)
        st.dataframe(sensibilidad_producto, use_container_width=True)

    with tab4:
        col_temp1, col_temp2 = st.columns(2)

        reclamos_temperatura = (
            df_filtrado.groupby("Rango_Temperatura", observed=True)
            .agg(
                Reclamos=("Reclamo_Binario", "sum"),
                Pedidos=("ID_Pedido", "count"),
                Porcentaje_Reclamos=("Reclamo_Binario", porcentaje_reclamos)
            )
            .reset_index()
        )

        fig_temp = px.bar(
            reclamos_temperatura,
            x="Rango_Temperatura",
            y="Porcentaje_Reclamos",
            color="Rango_Temperatura",
            text="Porcentaje_Reclamos",
            title="Reclamos por rango de temperatura de salida"
        )
        fig_temp.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig_temp.update_layout(
            xaxis_title="Temperatura de salida",
            yaxis_title="% reclamos",
            showlegend=False
        )
        col_temp1.plotly_chart(fig_temp, use_container_width=True)

        fig_box = px.box(
            df_filtrado,
            x="Reclamo",
            y="Temperatura_Salida_C",
            color="Reclamo",
            points="all",
            title="Temperatura de salida en pedidos con y sin reclamo"
        )
        fig_box.update_layout(
            xaxis_title="Hubo reclamo",
            yaxis_title="Temperatura de salida (C)"
        )
        col_temp2.plotly_chart(fig_box, use_container_width=True)

        st.dataframe(reclamos_temperatura, use_container_width=True)

    st.subheader("Datos filtrados")
    st.dataframe(df_filtrado.drop(columns=["Reclamo_Binario"]), use_container_width=True)

except FileNotFoundError:
    st.error("No se encontro el archivo restaurantes.xlsx")

except KeyError as e:
    st.error(f"Falta la columna requerida: {e}")

except Exception as e:
    st.error(f"Ocurrio un error inesperado: {e}")
