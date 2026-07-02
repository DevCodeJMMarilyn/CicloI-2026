"""
Amazon Price Scraper + BI Analysis - Versión Web (Multipágina)
Extrae precios de productos en Amazon a través de múltiples páginas (1-10)
y genera un informe HTML interactivo.
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import statistics
from datetime import datetime
import os
import time

# ─────────────────────────────────────────
#  CONFIGURACIÓN
# ─────────────────────────────────────────

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/136.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Connection": "keep-alive",
}

SEP = "─" * 56


# ─────────────────────────────────────────
#  SCRAPING
# ─────────────────────────────────────────

def obtener_html(producto: str, pagina: int = 1) -> str | None:
    """Realiza la petición a Amazon para una página específica y devuelve el HTML crudo."""
    # Estructura de URL para paginación en Amazon
    url = f"https://www.amazon.com/s?k={quote(producto)}&page={pagina}"
    print(f"\n🔍 [1/6] Buscando página {pagina} para: '{producto}'")
    print(f"      URL: {url}")

    try:
        respuesta = requests.get(url, headers=HEADERS, timeout=15)
        print(f"      ✅ Estado HTTP: {respuesta.status_code}")

        if respuesta.status_code == 200:
            print(f"      ✅ HTML de página {pagina} obtenido correctamente")
            return respuesta.text
        elif respuesta.status_code == 404:
            print(f"      ⚠️  La página {pagina} no existe (Fin de resultados).")
        elif respuesta.status_code == 503:
            print("      ⚠️  Amazon bloqueó la solicitud (503). Intenta usar proxies o user-agents dinámicos.")
        else:
            print(f"      ⚠️  Respuesta inesperada: {respuesta.status_code}")

    except requests.exceptions.Timeout:
        print("      ❌ Tiempo de espera agotado.")
    except requests.exceptions.ConnectionError:
        print("      ❌ Error de conexión.")

    return None


def parsear_productos(html: str) -> list[dict]:
    """Extrae nombre, precio, rating y reviews de cada tarjeta de producto en el HTML."""
    soup = BeautifulSoup(html, "html.parser")
    resultados = []

    tarjetas = soup.select('[data-component-type="s-search-result"]')
    print(f"      📦 Tarjetas encontradas en esta página: {len(tarjetas)}")

    for tarjeta in tarjetas:
        # ── Nombre ──
        nombre = None
        h2 = tarjeta.select_one("h2[aria-label]")
        if h2:
            nombre = h2.get("aria-label", "").strip()
        if not nombre:
            span = tarjeta.select_one("h2 a span, h2 span")
            nombre = span.get_text(strip=True) if span else None

        # ── Precio ──
        precio = None
        offscreen = tarjeta.select_one(".a-price .a-offscreen")
        if offscreen:
            raw = offscreen.get_text(strip=True).replace("US$", "").replace("$", "").replace(",", "").replace("€",
                                                                                                              "").strip()
            try:
                precio = float(raw)
            except ValueError:
                pass

        if precio is None:
            atc = tarjeta.select_one("[data-csa-c-price-to-pay]")
            if atc:
                try:
                    precio = float(atc.get("data-csa-c-price-to-pay", "").replace("€", ""))
                except ValueError:
                    pass

        if precio is None:
            whole = tarjeta.select_one(".a-price-whole")
            frac = tarjeta.select_one(".a-price-fraction")
            if whole:
                entero = whole.get_text(strip=True).replace(",", "").replace(".", "")
                fraccion = frac.get_text(strip=True) if frac else "00"
                try:
                    precio = float(f"{entero}.{fraccion}")
                except ValueError:
                    pass

        # ── Rating ──
        rating = None
        reviews_block = tarjeta.select_one('[data-cy="reviews-block"]')
        if reviews_block:
            for span in reviews_block.select('span[aria-hidden="true"]'):
                texto = span.get_text(strip=True)
                try:
                    val = float(texto)
                    if 1.0 <= val <= 5.0:
                        rating = val
                        break
                except ValueError:
                    pass

        if rating is None:
            for alt in tarjeta.select(".a-icon-alt"):
                texto = alt.get_text(strip=True)
                if "estrellas" in texto or "stars" in texto:
                    try:
                        rating = float(texto.split()[0])
                        break
                    except ValueError:
                        pass

        # ── Reviews ──
        reviews = None
        a_reviews = tarjeta.select_one('a[aria-label*="valoraciones"], a[aria-label*="ratings"]')
        if a_reviews:
            try:
                reviews = int(a_reviews.get("aria-label", "").split()[0].replace(",", "").replace(".", ""))
            except ValueError:
                pass

        if reviews is None:
            span_r = tarjeta.select_one(".a-size-mini.puis-normal-weight-text")
            if span_r:
                try:
                    reviews = int(span_r.get_text(strip=True).strip("()").replace(",", "").replace(".", ""))
                except ValueError:
                    pass

        if nombre and precio:
            resultados.append({
                "nombre": nombre,
                "precio": precio,
                "rating": rating,
                "reviews": reviews,
            })

    return resultados


# ─────────────────────────────────────────
#  ANÁLISIS BI
# ─────────────────────────────────────────

def analisis_bi(productos: list[dict], nombre_producto: str) -> dict:
    """Genera estadísticas y segmentación para Business Intelligence."""

    print(f"\n📊 [3/6] Realizando análisis estadístico sobre {len(productos)} productos...")

    precios = [p["precio"] for p in productos]
    ratings = [p["rating"] for p in productos if p["rating"] is not None]

    if not precios:
        return {}

    precio_min = min(precios)
    precio_max = max(precios)
    precio_prom = statistics.mean(precios)
    precio_med = statistics.median(precios)
    precio_std = statistics.stdev(precios) if len(precios) > 1 else 0

    q1 = statistics.quantiles(precios, n=4)[0] if len(precios) >= 4 else precio_min
    q3 = statistics.quantiles(precios, n=4)[2] if len(precios) >= 4 else precio_max
    iqr = q3 - q1

    umbral_bajo = precio_prom - (precio_std * 0.5)
    umbral_alto = precio_prom + (precio_std * 0.5)

    segmentos = {"Económico": [], "Medio": [], "Premium": []}
    for p in productos:
        if p["precio"] < umbral_bajo:
            segmentos["Económico"].append(p)
        elif p["precio"] > umbral_alto:
            segmentos["Premium"].append(p)
        else:
            segmentos["Medio"].append(p)

    mejores = [
        p for p in productos
        if p["rating"] is not None and p["rating"] >= 4.0 and p["precio"] <= precio_med
    ]
    mejores.sort(key=lambda x: (-x["rating"], x["precio"]))

    rating_stats = {}
    if ratings:
        rating_stats = {
            "promedio": round(statistics.mean(ratings), 2),
            "maximo": max(ratings),
            "minimo": min(ratings),
            "con_rating_pct": round(len(ratings) / len(productos) * 100, 1),
        }

    print(f"      ✅ Análisis estadístico completado")

    return {
        "metadata": {
            "producto_buscado": nombre_producto,
            "fecha_analisis": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_productos": len(productos),
        },
        "precios": {
            "minimo": round(precio_min, 2),
            "maximo": round(precio_max, 2),
            "promedio": round(precio_prom, 2),
            "mediana": round(precio_med, 2),
            "desv_std": round(precio_std, 2),
            "q1": round(q1, 2),
            "q3": round(q3, 2),
            "rango_iqr": round(iqr, 2),
        },
        "segmentacion": {
            seg: {
                "cantidad": len(items),
                "pct": round(len(items) / len(productos) * 100, 1),
                "precio_prom": round(statistics.mean([i["precio"] for i in items]), 2) if items else 0,
            }
            for seg, items in segmentos.items()
        },
        "rating": rating_stats,
        "top_valor": mejores[:5],
        "productos_raw": productos,
    }


# ─────────────────────────────────────────
#  GENERAR HTML
# ─────────────────────────────────────────

def generar_html(bi: dict, nombre_archivo: str = "analisis_producto.html") -> str:
    """Genera un informe HTML completo con el análisis utilizando Tailwind CSS."""

    print(f"\n🌐 [4/6] Generando informe HTML...")

    if not bi:
        return ""

    productos = bi['productos_raw']

    # Preparar datos para JavaScript (gráficos)
    nombres_productos = [p['nombre'][:40] + "..." if len(p['nombre']) > 40 else p['nombre'] for p in productos[:10]]
    precios_productos = [p['precio'] for p in productos[:10]]

    # Generar filas de productos para la tabla
    tablas_html = ""
    for i, p in enumerate(productos[:20], 1):
        rating_stars = "⭐" * int(p['rating'] or 0) if p['rating'] else "Sin rating"
        tablas_html += f"""
        <tr class="border-b border-gray-200 hover:bg-gray-50 transition-colors">
            <td class="p-3 text-sm text-gray-600">{i}</td>
            <td class="p-3 text-sm text-gray-800 max-w-xs truncate" title="{p['nombre']}">{p['nombre'][:80]}{"..." if len(p['nombre']) > 80 else ""}</td>
            <td class="p-3 text-sm font-semibold text-slate-900">${p['precio']:.2f}</td>
            <td class="p-3 text-sm text-amber-500">{rating_stars} <span class="text-gray-500 text-xs">({p['rating'] if p['rating'] else 'N/A'})</span></td>
            <td class="p-3 text-sm text-gray-600">{p['reviews'] if p['reviews'] else 'N/A'}</td>
        </tr>
        """

    # Generar Top 5 productos
    top_html = ""
    for i, prod in enumerate(bi['top_valor'], 1):
        top_html += f"""
        <div class="flex items-center gap-4 p-4 bg-gray-50 rounded-lg border border-gray-100 hover:bg-gray-100 transition-all">
            <div class="text-xl font-bold text-slate-700 w-10 text-center">#{i}</div>
            <div class="flex-1 min-w-0">
                <div class="font-medium text-gray-900 truncate" title="{prod['nombre']}">{prod['nombre'][:60]}{"..." if len(prod['nombre']) > 60 else ""}</div>
                <div class="text-sm text-gray-500">⭐ {prod['rating']} | <span class="font-semibold text-slate-800">${prod['precio']:.2f}</span></div>
            </div>
        </div>
        """

    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Análisis BI - {bi['metadata']['producto_buscado']}</title>
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
</head>
<body class="bg-slate-100 font-sans min-h-screen p-4 md:p-8 text-gray-800">

    <div class="max-w-7xl mx-auto bg-white rounded-xl shadow-md border border-gray-200 overflow-hidden">

        <div class="bg-slate-900 text-white p-8 border-b border-slate-800">
            <h1 class="text-2xl md:text-3xl font-bold tracking-tight mb-2">📊 Análisis Business Intelligence</h1>
            <div class="text-slate-400 font-medium tracking-wide uppercase text-sm">{bi['metadata']['producto_buscado']}</div>
            <div class="mt-4 pt-4 border-t border-slate-800 text-xs md:text-sm text-slate-400 flex flex-wrap gap-4">
                <span>📅 <strong>Fecha:</strong> {bi['metadata']['fecha_analisis']}</span>
                <span class="hidden md:inline">|</span>
                <span>📦 <strong>Muestra:</strong> {bi['metadata']['total_productos']} productos analizados</span>
            </div>
        </div>

        <div class="p-6 md:p-8 space-y-8">

            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <div class="bg-white p-5 rounded-xl border border-gray-200 text-center hover:shadow-sm transition-shadow">
                    <div class="text-xs uppercase tracking-wider text-gray-500 font-semibold mb-1">💰 Precio Mínimo</div>
                    <div class="text-2xl font-bold text-slate-900">${bi['precios']['minimo']}</div>
                </div>
                <div class="bg-white p-5 rounded-xl border border-gray-200 text-center hover:shadow-sm transition-shadow">
                    <div class="text-xs uppercase tracking-wider text-gray-500 font-semibold mb-1">💰 Precio Máximo</div>
                    <div class="text-2xl font-bold text-slate-900">${bi['precios']['maximo']}</div>
                </div>
                <div class="bg-white p-5 rounded-xl border border-gray-200 text-center hover:shadow-sm transition-shadow">
                    <div class="text-xs uppercase tracking-wider text-gray-500 font-semibold mb-1">📊 Precio Promedio</div>
                    <div class="text-2xl font-bold text-indigo-700">${bi['precios']['promedio']}</div>
                </div>
                <div class="bg-white p-5 rounded-xl border border-gray-200 text-center hover:shadow-sm transition-shadow">
                    <div class="text-xs uppercase tracking-wider text-gray-500 font-semibold mb-1">🎯 Precio Mediana</div>
                    <div class="text-2xl font-bold text-slate-900">${bi['precios']['mediana']}</div>
                </div>
            </div>

            <div class="space-y-4">
                <h2 class="text-lg font-bold text-slate-900 uppercase tracking-wide border-b-2 border-slate-900 pb-2">📈 Análisis de Precios</h2>
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    <div class="bg-gray-50 p-4 rounded-xl border border-gray-200 shadow-inner">
                        <canvas id="priceChart" class="max-h-[300px] w-full"></canvas>
                    </div>
                    <div class="bg-gray-50 p-4 rounded-xl border border-gray-200 shadow-inner">
                        <canvas id="distributionChart" class="max-h-[300px] w-full"></canvas>
                    </div>
                </div>
            </div>

            <div class="space-y-4">
                <h2 class="text-lg font-bold text-slate-900 uppercase tracking-wide border-b-2 border-slate-900 pb-2">🏷️ Segmentación de Mercado</h2>
                <div class="bg-white border border-gray-200 rounded-xl p-6 space-y-5 shadow-sm">
                    <div>
                        <div class="font-semibold text-gray-700 text-sm mb-1">💰 Económico</div>
                        <div class="w-full bg-gray-200 h-6 rounded-full overflow-hidden mb-1 shadow-inner">
                            <div class="bg-slate-500 h-full flex items-center justify-end pr-3 text-white text-xs font-bold" style="width: {bi['segmentacion']['Económico']['pct']}%">
                                {bi['segmentacion']['Económico']['pct']}%
                            </div>
                        </div>
                        <div class="text-xs text-gray-500">{bi['segmentacion']['Económico']['cantidad']} productos | Precio promedio: ${bi['segmentacion']['Económico']['precio_prom']}</div>
                    </div>
                    <div>
                        <div class="font-semibold text-gray-700 text-sm mb-1">📊 Medio</div>
                        <div class="w-full bg-gray-200 h-6 rounded-full overflow-hidden mb-1 shadow-inner">
                            <div class="bg-slate-700 h-full flex items-center justify-end pr-3 text-white text-xs font-bold" style="width: {bi['segmentacion']['Medio']['pct']}%">
                                {bi['segmentacion']['Medio']['pct']}%
                            </div>
                        </div>
                        <div class="text-xs text-gray-500">{bi['segmentacion']['Medio']['cantidad']} productos | Precio promedio: ${bi['segmentacion']['Medio']['precio_prom']}</div>
                    </div>
                    <div>
                        <div class="font-semibold text-gray-700 text-sm mb-1">⭐ Premium</div>
                        <div class="w-full bg-gray-200 h-6 rounded-full overflow-hidden mb-1 shadow-inner">
                            <div class="bg-indigo-950 h-full flex items-center justify-end pr-3 text-white text-xs font-bold" style="width: {bi['segmentacion']['Premium']['pct']}%">
                                {bi['segmentacion']['Premium']['pct']}%
                            </div>
                        </div>
                        <div class="text-xs text-gray-500">{bi['segmentacion']['Premium']['cantidad']} productos | Precio promedio: ${bi['segmentacion']['Premium']['precio_prom']}</div>
                    </div>
                </div>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div class="space-y-4">
                    <h2 class="text-lg font-bold text-slate-900 uppercase tracking-wide border-b-2 border-slate-900 pb-2">🏆 Top 5 Mejor Valor</h2>
                    <div class="space-y-3">
                        {top_html}
                    </div>
                </div>

                <div class="space-y-4">
                    <h2 class="text-lg font-bold text-slate-900 uppercase tracking-wide border-b-2 border-slate-900 pb-2">⭐ Estadísticas de Ratings</h2>
                    <div class="bg-white border border-gray-200 rounded-xl p-5 space-y-4 shadow-sm">
                        <div class="p-4 bg-gray-50 rounded-lg border border-gray-100 flex items-center justify-between">
                            <span class="font-medium text-gray-700 text-sm">Promedio de Rating</span>
                            <div class="text-right">
                                <span class="text-2xl font-bold text-slate-900">{bi['rating']['promedio'] if bi['rating'] else 'N/A'}</span>
                                <span class="text-xs text-gray-500 block">⭐ / 5.0</span>
                            </div>
                        </div>
                        <div class="p-4 bg-gray-50 rounded-lg border border-gray-100 flex items-center justify-between">
                            <span class="font-medium text-gray-700 text-sm">Rango de Ratings</span>
                            <span class="font-semibold text-slate-800 text-sm">{bi['rating']['minimo'] if bi['rating'] else 'N/A'} - {bi['rating']['maximo'] if bi['rating'] else 'N/A'} ⭐</span>
                        </div>
                        <div class="p-4 bg-gray-50 rounded-lg border border-gray-100 flex items-center justify-between">
                            <span class="font-medium text-gray-700 text-sm">Productos con Rating</span>
                            <span class="font-semibold text-slate-800 text-sm">{bi['rating']['con_rating_pct'] if bi['rating'] else 0}% del total</span>
                        </div>
                    </div>
                </div>
            </div>

            <div class="space-y-4">
                <h2 class="text-lg font-bold text-slate-900 uppercase tracking-wide border-b-2 border-slate-900 pb-2">📋 Lista de Productos</h2>
                <div class="overflow-x-auto border border-gray-200 rounded-xl shadow-sm">
                    <table class="w-full text-left border-collapse bg-white">
                        <thead>
                            <tr class="bg-slate-900 text-white text-xs uppercase tracking-wider">
                                <th class="p-3 font-semibold w-12">#</th>
                                <th class="p-3 font-semibold">Producto</th>
                                <th class="p-3 font-semibold w-28">Precio</th>
                                <th class="p-3 font-semibold w-40">Rating</th>
                                <th class="p-3 font-semibold w-24">Reviews</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-gray-100">
                            {tablas_html}
                        </tbody>
                    </table>
                </div>
            </div>

        </div>

        <div class="bg-gray-50 border-t border-gray-200 p-4 text-center text-xs text-gray-500 font-medium">
            <p>📊 Informe generado automáticamente • Datos obtenidos de Amazon • Análisis BI</p>
        </div>
    </div>

    <script>
        // Gráfico de precios (Paleta Corporativa)
        const ctx1 = document.getElementById('priceChart').getContext('2d');
        new Chart(ctx1, {{
            type: 'line',
            data: {{
                labels: {nombres_productos},
                datasets: [{{
                    label: 'Precio (USD)',
                    data: {precios_productos},
                    borderColor: '#4338ca', // indigo-700
                    backgroundColor: 'rgba(67, 56, 202, 0.05)', 
                    tension: 0.2,
                    fill: true,
                    borderWidth: 2
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: true,
                plugins: {{
                    legend: {{ position: 'top' }},
                    title: {{
                        display: true,
                        text: 'Top 10 Productos - Precios',
                        font: {{ weight: 'bold', size: 13 }}
                    }}
                }}
            }}
        }});

        // Gráfico de distribución de segmentos (Gris, Pizarra e Índigo)
        const ctx2 = document.getElementById('distributionChart').getContext('2d');
        new Chart(ctx2, {{
            type: 'doughnut',
            data: {{
                labels: ['Económico', 'Medio', 'Premium'],
                datasets: [{{
                    data: [{bi['segmentacion']['Económico']['pct']}, {bi['segmentacion']['Medio']['pct']}, {bi['segmentacion']['Premium']['pct']}],
                    backgroundColor: ['#64748b', '#334155', '#1e1b4b'], // slate-500, slate-700, indigo-950
                    borderWidth: 1,
                    borderColor: '#ffffff'
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: true,
                plugins: {{
                    legend: {{ position: 'bottom' }},
                    title: {{
                        display: true,
                        text: 'Distribución por Segmento',
                        font: {{ weight: 'bold', size: 13 }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>"""

    # Guardar el archivo HTML
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"      ✅ HTML generado con Tailwind: {nombre_archivo}")
    return nombre_archivo

# ─────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────

def main():
    print("\n" + "=" * 60)
    print("   AMAZON PRICE SCRAPER - ANÁLISIS BI MULTIPÁGINA")
    print("=" * 60)

    producto = input("\n🔎 Ingrese el producto a buscar: ").strip()
    if not producto:
        print("❌ No ingresaste ningún producto.")
        return

    # Entrada y Validación del número de páginas (Mínimo 1, Máximo 10)
    while True:
        try:
            total_paginas = int(input("📄 Ingrese el número de páginas a extraer (mínimo 1, máximo 10): "))
            if 1 <= total_paginas <= 10:
                break
            else:
                print("⚠️  Por favor, elija un número entre 1 y 10.")
        except ValueError:
            print("❌ Entrada inválida. Ingrese un número entero.")

    productos_totales = []

    # Iteración sobre el rango de páginas seleccionado
    for pagina in range(1, total_paginas + 1):
        html = obtener_html(producto, pagina)

        if not html:
            print(f"⚠️  Saltando página {pagina} debido a un inconveniente con la solicitud.")
            continue

        productos_pagina = parsear_productos(html)
        productos_totales.extend(productos_pagina)

        # Guardar la última para debug tracking
        if pagina == 1:
            with open("amazon_debug.html", "w", encoding="utf-8") as f:
                f.write(html)
            print("      💾 HTML de la página 1 respaldado en (amazon_debug.html)")

        # Pequeño delay de cortesía para evitar penalizaciones inmediatas/bloqueos rápidos de Amazon
        if pagina < total_paginas:
            print("⏳ Esperando 2 segundos antes de la siguiente página...")
            time.sleep(2)

    if not productos_totales:
        print("\n⚠️  No se logró capturar productos con precio en ninguna página.")
        print("\n[5/6] Diagnóstico rápido:")
        print("      Verifica amazon_debug.html en tu navegador para evaluar la respuesta de la plataforma.")
        return

    # Paso 3: Análisis BI unificado
    bi = analisis_bi(productos_totales, producto)

    # Paso 4: Generar HTML dinámico
    archivo_html = generar_html(bi)

    # Paso 5: Lanzar en el navegador predeterminado
    print(f"\n🌐 [5/6] Lanzando informe en el navegador...")
    import webbrowser
    webbrowser.open(f"file://{os.path.abspath(archivo_html)}")

    print(f"\n✅ [6/6] PROCESO COMPLETADO")
    print("=" * 60)
    print(f"📊 INFORME UNIFICADO DISPONIBLE EN: {archivo_html}")
    print(f"📦 Total productos analizados: {len(productos_totales)}")
    print(f"💰 Rango de precios global: €{bi['precios']['minimo']} - €{bi['precios']['maximo']}")
    print(f"📈 Precio promedio: €{bi['precios']['promedio']}")
    if bi.get('rating'):
        print(f"⭐ Rating promedio ponderado: {bi['rating']['promedio']}/5.0")
    print("=" * 60)


if __name__ == "__main__":
    main()