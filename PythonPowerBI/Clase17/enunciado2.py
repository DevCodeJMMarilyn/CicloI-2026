import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque
import time

class MiniBuscador:

    def __init__(self, seed_url, palabra_buscar):

        self.seed_url = seed_url
        self.palabra_buscar = palabra_buscar.lower()
        self.visited = set()
        self.queue = deque([seed_url])
        self.domain = urlparse(seed_url).netloc

    def buscar(self, max_pages=30):

        while self.queue and len(self.visited) < max_pages:

            url = self.queue.popleft()

            if url in self.visited:
                continue

            self.visited.add(url)

            print(f"\n Visitando: {url}")

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

                if self.palabra_buscar in texto:

                    print("\n✅ PALABRA ENCONTRADA")
                    print(f"🔍 Palabra: {self.palabra_buscar}")
                    print(f"📄 URL: {url}")

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

    palabra = input("Ingrese palabra a buscar: ")

    buscador = MiniBuscador(
        "https://www.univo.edu.sv/",
        palabra
    )

    buscador.buscar(max_pages=30)