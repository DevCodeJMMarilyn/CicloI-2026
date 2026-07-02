import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.title("Dashboard de Ventas")

try:
    df = pd.read_excel("ventas.xlsx", engine="openpyxl")
    df.columns = df.columns.str.strip()

    st.write("Columnas detectadas:")
    st.write(df.columns)

    df["Total"] = df["Cantidad"] * df["Precio"]

    st.subheader("Datos de las Ventas")
    st.dataframe(df)

    # KPI's
    ventas_totales = df["Total"].sum()
    ventas_promedio = df["Total"].mean()

    col1, col2 = st.columns(2)

    col1.metric("Ventas Totales", f"${ventas_totales:,.2f}")
    col2.metric("Ventas Promedio", f"${ventas_promedio:,.2f}")

    st.subheader("Productos más Vendidos")

    productos_mas_vendidos = (
        df.groupby("Producto")["Cantidad"]
        .sum()
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots()

    productos_mas_vendidos.plot(kind="bar", ax=ax)

    plt.title("Cantidad vendida por producto")
    plt.xlabel("Producto")
    plt.ylabel("Cantidad")

    st.pyplot(fig)

    st.subheader("Ventas por Ciudad")

    ventas_ciudad = df.groupby("Ciudad")["Total"].sum()

    fig2, ax2 = plt.subplots()

    ventas_ciudad.plot(kind="pie", autopct="%1.1f%%", ax=ax2)

    plt.ylabel("")

    st.pyplot(fig2)

    ciudades_unicas = df["Ciudad"].unique()

    ciudad = st.selectbox(
        "Selecciona una ciudad para filtrar",
        ciudades_unicas
    )

    df_filtrado = df[df["Ciudad"] == ciudad]

    st.subheader(f"Datos filtrados por Ciudad: {ciudad}")

    st.dataframe(df_filtrado)

except FileNotFoundError:
    st.error("No se encontró el archivo ventas.xlsx")

except KeyError as e:
    st.error(f"Falta la columna: {e}")

except Exception as e:
    st.error(f"Ocurrió un error inesperado: {e}")