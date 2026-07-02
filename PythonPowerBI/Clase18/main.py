import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import statistics
import re
import webbrowser

# ==========================================
# HEADERS
# ==========================================

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept-Language": "es-ES,es;q=0.9",
}

# ==========================================
# OBTENER HTML
# ==========================================

def obtener_html(producto):

    url = f"https://www.amazon.com/s?k={quote(producto)}"

    try:

        respuesta = requests.get(
            url,
            headers=HEADERS,
            timeout=10
        )

        if respuesta.status_code == 200:
            return respuesta.text

        print("Error HTTP:", respuesta.status_code)
        return None

    except Exception as e:

        print("Error:", e)
        return None


# ==========================================
# LIMPIAR PRECIO
# ==========================================

def limpiar_precio(texto):

    try:

        texto = texto.replace("$", "")
        texto = texto.replace(",", "")

        numero = re.findall(
            r'\d+\.?\d*',
            texto
        )[0]

        return float(numero)

    except:
        return None


# ==========================================
# EXTRAER PRODUCTOS
# ==========================================

def extraer_productos(html):

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    tarjetas = soup.select(
        '[data-component-type="s-search-result"]'
    )

    productos = []

    for tarjeta in tarjetas:

        try:

            nombre_tag = tarjeta.select_one(
                "h2 span"
            )

            if not nombre_tag:
                continue

            nombre = nombre_tag.get_text(
                strip=True
            )

            precio_tag = tarjeta.select_one(
                ".a-price .a-offscreen"
            )

            if not precio_tag:
                precio_tag = tarjeta.select_one(
                    "[data-csa-c-price-to-pay]"
                )

            precio = None

            if precio_tag:
                precio = limpiar_precio(
                    precio_tag.get_text(strip=True)
                )

            rating_tag = tarjeta.select_one(
                ".a-icon-alt"
            )

            rating = None

            if rating_tag:

                numeros = re.findall(
                    r'\d+\.?\d*',
                    rating_tag.get_text()
                )

                if numeros:
                    rating = float(numeros[0])

            productos.append({

                "nombre": nombre,
                "precio": precio,
                "rating": rating

            })

        except:
            continue

    return productos


# ==========================================
# ANALISIS BI
# ==========================================

def analizar_datos(productos):

    precios = [

        p["precio"]

        for p in productos

        if p["precio"] is not None

    ]

    ratings = [

        p["rating"]

        for p in productos

        if p["rating"] is not None

    ]

    if len(precios) == 0:
        return None

    promedio = statistics.mean(precios)
    mediana = statistics.median(precios)

    if len(precios) > 1:
        desviacion = statistics.stdev(precios)
    else:
        desviacion = 0

    minimo = min(precios)
    maximo = max(precios)

    umbral_bajo = promedio - (desviacion * 0.5)
    umbral_alto = promedio + (desviacion * 0.5)

    for p in productos:

        if p["precio"] is None:
            continue

        if p["precio"] < umbral_bajo:

            p["segmento"] = "Económico"

        elif p["precio"] > umbral_alto:

            p["segmento"] = "Premium"

        else:

            p["segmento"] = "Medio"

    top_valor = [

        p

        for p in productos

        if p["precio"] is not None
        and p["rating"] is not None
        and p["rating"] >= 4
        and p["precio"] <= mediana

    ]

    top_valor = sorted(

        top_valor,

        key=lambda x: x["rating"],

        reverse=True

    )[:5]

    return {

        "precio_minimo": round(minimo, 2),
        "precio_maximo": round(maximo, 2),
        "precio_promedio": round(promedio, 2),
        "precio_mediana": round(mediana, 2),
        "desviacion": round(desviacion, 2),
        "rating_promedio": round(statistics.mean(ratings), 2) if ratings else 0,
        "top_valor": top_valor

    }


# ==========================================
# REPORTE HTML
# ==========================================

def generar_reporte(producto, productos, analisis):

    nombres = [
        p["nombre"][:40]
        for p in productos[:10]
    ]

    precios = [
        p["precio"] if p["precio"] else 0
        for p in productos[:10]
    ]

    filas = ""

    for p in productos:

        filas += f"""
<tr>
<td>{p['nombre']}</td>
<td>{p['precio']}</td>
<td>{p['rating']}</td>
<td>{p.get('segmento','')}</td>
</tr>
"""

    top_html = ""

    for p in analisis["top_valor"]:

        top_html += f"""
<li>
<strong>{p['nombre']}</strong><br>
Precio: ${p['precio']} |
Rating: {p['rating']}
</li>
"""

    html = f"""
<!DOCTYPE html>
<html>
<head>

<meta charset="utf-8">

<title>Dashboard BI</title>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<style>

body {{
font-family: Arial;
background:#f4f6f9;
margin:20px;
}}

.card {{
background:white;
padding:15px;
margin:10px;
border-radius:10px;
box-shadow:0 0 10px rgba(0,0,0,.1);
}}

table {{
width:100%;
border-collapse:collapse;
}}

th,td {{
padding:10px;
border:1px solid #ddd;
}}

th {{
background:#0033A0;
color:white;
}}

</style>

</head>

<body>

<h1>Dashboard BI - {producto}</h1>

<div class="card">
<h2>KPIs</h2>

<p>Precio mínimo: ${analisis["precio_minimo"]}</p>
<p>Precio máximo: ${analisis["precio_maximo"]}</p>
<p>Precio promedio: ${analisis["precio_promedio"]}</p>
<p>Mediana: ${analisis["precio_mediana"]}</p>
<p>Desviación: {analisis["desviacion"]}</p>
<p>Rating promedio: {analisis["rating_promedio"]}</p>

</div>

<div class="card">

<canvas id="priceChart"></canvas>

</div>

<div class="card">

<h2>Productos</h2>

<table>

<tr>
<th>Producto</th>
<th>Precio</th>
<th>Rating</th>
<th>Segmento</th>
</tr>

{filas}

</table>

</div>

<div class="card">

<h2>Top 5 Mejor Valor</h2>

<ul>

{top_html}

</ul>

</div>

<script>

const ctx = document.getElementById('priceChart');

new Chart(ctx, {{

type:'line',

data: {{

labels: {nombres},

datasets:[{{

label:'Precio USD',

data:{precios},

borderColor:'#0033A0',

fill:false

}}]

}}

}});

</script>

</body>
</html>
"""

    with open(
        "reporte_amazon.html",
        "w",
        encoding="utf-8"
    ) as f:

        f.write(html)

    print("Reporte generado.")

    webbrowser.open(
        "reporte_amazon.html"
    )


# ==========================================
# MAIN
# ==========================================

def main():

    producto = input(
        "Ingrese producto: "
    )

    html = obtener_html(producto)

    if not html:
        print("No se pudo obtener HTML.")
        return

    productos = extraer_productos(html)

    if len(productos) == 0:
        print("No se encontraron productos.")
        return

    analisis = analizar_datos(productos)

    if not analisis:
        print("No se encontraron precios.")
        return

    generar_reporte(
        producto,
        productos,
        analisis
    )


if __name__ == "__main__":
    main()

