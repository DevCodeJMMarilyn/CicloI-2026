# ENUNCIADO 1 — CRAWLER AUTOMÁTICO UNIVO
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque
import time

class UnivoCrawler:
    def __init__(self, seed_url, palabras_clave):
        self.seed_url = seed_url
        self.palabras_clave = palabras_clave
        self.visited = set()
        self.queue = deque([seed_url])
        self.domain = urlparse(seed_url).netloc

    def crawl(self, max_pages=30):

        while self.queue and len(self.visited) < max_pages:

            url = self.queue.popleft()

            if url in self.visited:
                continue

            print(f"\n🕷️ Visitando: {url}")

            self.visited.add(url)

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

                for palabra in self.palabras_clave:

                    if palabra.lower() in texto:

                        titulo = soup.title.string if soup.title else "Sin título"

                        print("\n✅ PALABRA ENCONTRADA")
                        print(f"🔍 Palabra: {palabra}")
                        print(f"📄 URL: {url}")
                        print(f"📌 Título: {titulo}")

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


if __name__ == "__main__":

    SITIO = "https://www.univo.edu.sv/"

    PALABRAS = [
        "carrera",
        "ingeniería",
        "facultad",
        "maestría",
        "técnico"
    ]

    crawler = UnivoCrawler(SITIO, PALABRAS)
    crawler.crawl(max_pages=30)