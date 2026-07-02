import os
from collections import Counter
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

# LAB 3 MARILYN JIMENEZ U20231085
# ==========================================
# CONFIGURACION
# ==========================================

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

FORMATOS_PERMITIDOS = {
    ".png": "PNG",
    ".jpg": "JPG",
    ".jpeg": "JPEG",
    ".webp": "WEBP",
}

CARPETA_IMAGENES = "imagenes"
LIMITE_DESCARGA = 10
ARCHIVO_HTML = "pagina.html"


# ==========================================
# OBTENER HTML
# ==========================================

def obtener_html(url):

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

    except requests.exceptions.MissingSchema:
        print("Error: la URL debe iniciar con http:// o https://")
        return None

    except requests.exceptions.RequestException as error:
        print("Error al descargar la pagina:", error)
        return None


# ==========================================
# GUARDAR HTML
# ==========================================

def obtener_nombre_disponible(nombre_archivo, carpeta=None):

    if carpeta:
        ruta_archivo = os.path.join(
            carpeta,
            nombre_archivo
        )
    else:
        ruta_archivo = nombre_archivo

    if not os.path.exists(ruta_archivo):
        return ruta_archivo

    nombre, extension = os.path.splitext(nombre_archivo)
    contador = 1

    while True:

        nuevo_nombre = f"{nombre}_{contador}{extension}"

        if carpeta:
            nueva_ruta = os.path.join(
                carpeta,
                nuevo_nombre
            )
        else:
            nueva_ruta = nuevo_nombre

        if not os.path.exists(nueva_ruta):
            return nueva_ruta

        contador += 1


def guardar_html(html):

    ruta_html = obtener_nombre_disponible(ARCHIVO_HTML)

    with open(ruta_html, "w", encoding="utf-8") as archivo:
        archivo.write(html)

    print("HTML descargado y guardado en:", ruta_html)


# ==========================================
# EXTRAER FORMATO
# ==========================================

def obtener_formato(url_imagen):

    ruta = urlparse(url_imagen).path
    extension = os.path.splitext(ruta)[1].lower()

    if extension in FORMATOS_PERMITIDOS:
        return FORMATOS_PERMITIDOS[extension], extension

    return None, extension


# ==========================================
# EXTRAER IMAGENES
# ==========================================

def extraer_imagenes(html, url_base):

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    etiquetas_img = soup.find_all("img")
    todas_las_imagenes = []
    imagenes = []

    for etiqueta in etiquetas_img:

        src = (
            etiqueta.get("src")
            or etiqueta.get("data-src")
            or etiqueta.get("data-lazy-src")
        )

        if not src:
            continue

        url_imagen = urljoin(
            url_base,
            src
        )

        todas_las_imagenes.append(url_imagen)

        formato, extension = obtener_formato(url_imagen)

        if not formato:
            continue

        imagenes.append({
            "url": url_imagen,
            "alt": etiqueta.get("alt") or "Sin texto alternativo",
            "formato": formato,
            "extension": extension
        })

    return todas_las_imagenes, imagenes


# ==========================================
# MOSTRAR INFORMACION
# ==========================================

def mostrar_imagenes(todas_las_imagenes, imagenes):

    print("\n==========================================")
    print("PARTE I - EXPLORACION DE IMAGENES")
    print("==========================================")
    print("Imagenes encontradas:", len(todas_las_imagenes))

    for indice, url_imagen in enumerate(todas_las_imagenes, start=1):

        print("\nImagen", str(indice) + ":")
        print(url_imagen)

    print("\n==========================================")
    print("PARTE II - INFORMACION DE LAS IMAGENES")
    print("==========================================")
    print("Imagenes validas PNG, JPG, JPEG o WEBP:", len(imagenes))

    if len(imagenes) == 0:
        print("\nNo se encontraron imagenes PNG, JPG, JPEG o WEBP.")
        return

    for indice, imagen in enumerate(imagenes, start=1):

        print("\nImagen valida", str(indice) + ":")
        print("URL:")
        print(imagen["url"])
        print("ALT:")
        print(imagen["alt"])
        print("Formato:")
        print(imagen["formato"])

# ==========================================
# DESCARGAR IMAGENES
# ==========================================

def obtener_ruta_disponible(nombre_archivo):

    return obtener_nombre_disponible(
        nombre_archivo,
        CARPETA_IMAGENES
    )


def descargar_imagenes(imagenes):

    os.makedirs(
        CARPETA_IMAGENES,
        exist_ok=True
    )

    descargadas = 0

    for indice, imagen in enumerate(imagenes[:LIMITE_DESCARGA], start=1):

        extension = imagen["extension"]

        if extension == ".jpeg":
            extension = ".jpg"

        nombre_archivo = f"imagen{indice}{extension}"
        ruta_archivo = obtener_ruta_disponible(nombre_archivo)

        try:

            respuesta = requests.get(
                imagen["url"],
                headers=HEADERS,
                timeout=10
            )

            if respuesta.status_code != 200:
                print("No se pudo descargar:", imagen["url"])
                continue

            with open(ruta_archivo, "wb") as archivo:
                archivo.write(respuesta.content)

            descargadas += 1
            print("Descargada:", ruta_archivo)

        except requests.exceptions.RequestException as error:
            print("Error al descargar imagen:", error)

    print("\nTotal de imagenes descargadas:", descargadas)


# ==========================================
# ESTADISTICAS
# ==========================================

def mostrar_estadisticas(imagenes):

    conteo = Counter(
        imagen["formato"]
        for imagen in imagenes
    )

    total = len(imagenes)

    print("\n==========================================")
    print("ESTADISTICAS")
    print("==========================================")
    print("Total imagenes:", total)
    print("PNG:", conteo.get("PNG", 0))
    print("JPG:", conteo.get("JPG", 0))
    print("JPEG:", conteo.get("JPEG", 0))
    print("WEBP:", conteo.get("WEBP", 0))

    if total == 0:
        print("\nFormato predominante: Ninguno")
        return

    cantidad_maxima = max(conteo.values())
    formatos_predominantes = [
        formato
        for formato, cantidad in conteo.items()
        if cantidad == cantidad_maxima
    ]

    if len(formatos_predominantes) == 1:
        print("\nFormato predominante:")
        print(formatos_predominantes[0])
    else:
        print("\nFormatos predominantes:")
        print(", ".join(formatos_predominantes))


# ==========================================
# MAIN
# ==========================================

def main():

    url = input("Ingrese la URL de la pagina web: ").strip()

    html = obtener_html(url)

    if not html:
        print("No se pudo analizar la pagina.")
        return

    guardar_html(html)

    todas_las_imagenes, imagenes = extraer_imagenes(
        html,
        url
    )

    mostrar_imagenes(
        todas_las_imagenes,
        imagenes
    )

    mostrar_estadisticas(imagenes)

    if len(imagenes) > 0:
        print("\n==========================================")
        print("DESCARGA AUTOMATICA")
        print("==========================================")
        descargar_imagenes(imagenes)


if __name__ == "__main__":
    main()
