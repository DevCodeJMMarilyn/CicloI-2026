import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque
from datetime import datetime
import time

class DetectorOfertas:

    def __init__(self, seed_url, palabras_clave):

        self.seed_url = seed_url
        self.palabras_clave = palabras_clave

        self.visited = set()
        self.queue = deque([seed_url])
        self.domain = urlparse(seed_url).netloc

        self.resultados = []

    def crawl(self, max_pages=40):

        while self.queue and len(self.visited) < max_pages:

            url = self.queue.popleft()

            if url in self.visited:
                continue

            self.visited.add(url)

            print(f"\n🕷️ Visitando: {url}")

            try:

                response = requests.get(
                    url,
                    timeout=10,
                    headers={'User-Agent': 'Mozilla/5.0'}
                )

                if response.status_code != 200:
                    continue

                soup = BeautifulSoup(response.text, 'html.parser')

                texto = soup.get_text().lower()

                coincidencias = []

                for palabra in self.palabras_clave:

                    if palabra.lower() in texto:
                        coincidencias.append(palabra)

                if coincidencias:

                    titulo = soup.title.string if soup.title else "Sin título"

                    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    relevancia = len(coincidencias)

                    resultado = {
                        "fecha": fecha_actual,
                        "url": url,
                        "titulo": titulo,
                        "palabras": coincidencias,
                        "relevancia": relevancia
                    }

                    self.resultados.append(resultado)

                    print("✅ Oferta encontrada")

                # Buscar enlaces internos
                for link in soup.find_all('a', href=True):

                    href = link['href']

                    nueva_url = urljoin(url, href)

                    if urlparse(nueva_url).netloc == self.domain:

                        if nueva_url not in self.visited:
                            self.queue.append(nueva_url)

                time.sleep(1)

            except Exception as e:
                print(f"❌ Error: {e}")

    def guardar_resultados(self):

        self.resultados.sort(
            key=lambda x: x['relevancia'],
            reverse=True
        )

        with open("ofertas_encontradas.txt", "w", encoding="utf-8") as archivo:

            archivo.write("="*60 + "\n")
            archivo.write("OFERTAS LABORALES ENCONTRADAS\n")
            archivo.write("="*60 + "\n\n")

            for r in self.resultados:

                archivo.write(f"📅 Fecha: {r['fecha']}\n")
                archivo.write(f"🔗 URL: {r['url']}\n")
                archivo.write(f"📌 Título: {r['titulo']}\n")
                archivo.write(f"🎯 Palabras: {', '.join(r['palabras'])}\n")
                archivo.write(f"⭐ Relevancia: {r['relevancia']}\n")
                archivo.write("-"*50 + "\n")

        print("\n✅ Resultados guardados en ofertas_encontradas.txt")


if __name__ == "__main__":

    PALABRAS = [
        "empleo",
        "oferta",
        "trabajo",
        "convocatoria",
        "prácticas",
        "pasantía"
    ]

    detector = DetectorOfertas(
        "https://www.univo.edu.sv/",
        PALABRAS
    )

    detector.crawl(max_pages=40)

    detector.guardar_resultados()