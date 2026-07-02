import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque

class SimpleCrawler:
    def __init__(self, seed_url, max_pages=50):
        self.seed_url = seed_url
        self.max_pages = max_pages
        self.visited = set()
        self.queue = deque([seed_url])
        self.domain = urlparse(seed_url).netloc
    
    def crawl(self):
        pages_visited = 0
        while self.queue and pages_visited < self.max_pages:
            url = self.queue.popleft()
            
            if url in self.visited:
                continue
            
            print(f"🕷️ Visitando: {url}")
            self.visited.add(url)
            pages_visited += 1
            
            try:
                # 1. Descargar página
                response = requests.get(url, headers={'User-Agent': 'MiCrawler/1.0'})
                if response.status_code != 200:
                    continue
                
                # 2. Parsear HTML
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 3. Extraer enlaces
                for link in soup.find_all('a', href=True):
                    href = link.get('href')
                    absolute_url = urljoin(url, href)
                    
                    # 4. Filtrar: solo enlaces del mismo dominio y no visitados
                    if urlparse(absolute_url).netloc == self.domain and absolute_url not in self.visited:
                        self.queue.append(absolute_url)
                        print(f"   🔗 Nuevo enlace encontrado: {absolute_url}")
            
            except Exception as e:
                print(f"   ❌ Error: {e}")
        
        print(f"\n✅ Crawler finalizado. {len(self.visited)} páginas visitadas.")

# Ejecutar
if __name__ == "__main__":
    crawler = SimpleCrawler("https://www.univo.edu.sv/", max_pages=10)
    crawler.crawl()