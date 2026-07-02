import pandas as pd
import streamlit as st
import plotly.express as px

# Título del dashboard
st.title("Dashboard de Análisis Académico")

try:

    # Cargar datos
    df = pd.read_excel(
        "estudiantes.xlsx",
        engine="openpyxl"
    )

    # Limpiar nombres de columnas
    df.columns = df.columns.str.strip()

    # Crear columna Rinde
    df["Rinde"] = df[
        "Nota_Definitiva"
    ].apply(
        lambda x: 1 if x >= 6 else 0
    )

    # Filtro interactivo
    st.subheader(
        "Filtro por Género"
    )

    genero = st.selectbox(
        "Selecciona un género",
        ["Todos", "F", "M"]
    )

    if genero != "Todos":

        df_filtrado = df[
            df["Género"] == genero
        ]

    else:

        df_filtrado = df

    # Mostrar datos
    st.subheader(
        "Datos de los Estudiantes"
    )

    st.dataframe(df_filtrado)

    # KPI's
    st.subheader(
        "Indicadores Académicos"
    )

    tasa_aprobacion = (
        df_filtrado["Rinde"]
        .mean() * 100
    )

    promedio_general = (
        df_filtrado[
            "Nota_Definitiva"
        ].mean()
    )

    col1, col2 = st.columns(2)

    col1.metric(
        "Tasa de Aprobación",
        f"{tasa_aprobacion:.2f}%"
    )

    col2.metric(
        "Promedio General",
        f"{promedio_general:.2f}"
    )

    # Gráfico 1
    st.subheader(
        "Horas de Estudio vs "
        "Nota Definitiva"
    )

    fig1 = px.scatter(
        df_filtrado,
        x="Horas_Estudio_Semana",
        y="Nota_Definitiva",
        color="Estado_Final",
        hover_data=[
            "ID_Estudiante",
            "Asistencia_Porcentaje"
        ]
    )

    st.plotly_chart(fig1)

    # Gráfico 2
    st.subheader(
        "Promedio de Nota por "
        "Estrato Socioeconómico"
    )

    promedio_estrato = (
        df_filtrado.groupby(
            "Estrato_Socioeconomico"
        )[
            "Nota_Definitiva"
        ]
        .mean()
        .reset_index()
    )

    fig2 = px.bar(
        promedio_estrato,
        x="Estrato_Socioeconomico",
        y="Nota_Definitiva",
        color="Estrato_Socioeconomico"
    )

    st.plotly_chart(fig2)

    # Tabla de estudiantes en riesgo
    st.subheader(
        "Estudiantes en Riesgo"
    )

    riesgo = df_filtrado[
        (
            df_filtrado[
                "Asistencia_Porcentaje"
            ] < 75
        )
        |
        (
            df_filtrado[
                "Horas_Estudio_Semana"
            ] < 5
        )
    ]

    st.dataframe(riesgo)

    # Análisis
    st.subheader(
        "Análisis de Resultados"
    )

    st.write(
        "Los estudiantes con "
        "más horas de estudio y "
        "mayor asistencia tienden "
        "a obtener mejores notas."
    )

except FileNotFoundError:

    st.error(
        "No se encontró el archivo "
        "estudiantes.xlsx"
    )

except KeyError as e:

    st.error(
        f"Falta la columna: {e}"
    )

except Exception as e:

    st.error(
        f"Ocurrió un error "
        f"inesperado: {e}"
    )
    
#Michelle Jimenez U20231085