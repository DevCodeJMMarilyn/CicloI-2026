# Laboratorio #3 - Descargador Automatico de Imagenes

## Tema

Web Scraping | BeautifulSoup | Descarga de imagenes | Estadisticas

## Contexto

La empresa DataVision desea crear un repositorio de imagenes institucionales obtenidas desde sitios web publicos.

El programa permite ingresar una pagina web, analizar su codigo HTML, detectar imagenes, mostrar informacion importante y descargar automaticamente las primeras imagenes encontradas.

## Objetivos

- Solicitar una URL al usuario.
- Descargar el codigo HTML de la pagina.
- Analizar la estructura con BeautifulSoup.
- Localizar las etiquetas `<img>`.
- Mostrar URL, texto alternativo y formato de cada imagen.
- Filtrar imagenes PNG, JPG, JPEG y WEBP.
- Descargar automaticamente las primeras 10 imagenes validas.
- Generar estadisticas por formato.
- Manejar errores de URL invalida o descarga fallida.

## Librerias utilizadas

```bash
pip install requests beautifulsoup4
```

Tambien se utilizan modulos nativos de Python:

- `os`
- `urllib.parse`
- `collections`

## Estructura del proyecto

```text
Lab3/
|
+-- main.py
+-- README.md
+-- requirements.txt
+-- imagenes/        # Se crea automaticamente al ejecutar el programa
```

## Partes desarrolladas

### Parte I - Exploracion de imagenes

El programa solicita una URL, descarga el HTML y busca las etiquetas `<img>` usando:

```python
soup.find_all("img")
```

En consola muestra la cantidad total de etiquetas encontradas y la cantidad de imagenes validas.

### Parte II - Informacion de imagenes

Por cada imagen valida muestra:

- URL de la imagen.
- Texto alternativo `alt`.
- Formato: PNG, JPG, JPEG o WEBP.

### Parte III - Descarga automatica

El programa crea la carpeta `imagenes` y descarga las primeras 10 imagenes validas con nombres consecutivos:

```text
imagenes/
|
+-- imagen1.jpg
+-- imagen2.png
+-- imagen3.jpeg
+-- imagen4.webp
```

### Parte IV - Filtrado de imagenes

Solo se aceptan:

- PNG
- JPG
- JPEG
- WEBP

Se ignoran SVG, GIF, ICO y otros formatos.

### Parte V - Analisis de datos

El programa genera:

- Total de imagenes validas.
- Cantidad de imagenes PNG.
- Cantidad de imagenes JPG.
- Cantidad de imagenes JPEG.
- Cantidad de imagenes WEBP.
- Formato predominante.

## Ejemplo de salida

```text
Total imagenes: 12
PNG: 4
JPG: 5
JPEG: 2
WEBP: 1

Formato predominante:
JPG
```

## Como ejecutar

Desde la carpeta `Lab3`:

```bash
python main.py
```
