import requests
from bs4 import BeautifulSoup


# # 1. Descargar la página
url = "https://www.univo.edu.sv/"
response = requests.get(url)

print("Estado: ",{response.status_code})
# 2. Parsear HTML
soup = BeautifulSoup(response.text, 'lxml')
# time = sleep(1)
# 3. Extraer datos
print("Título Ej de clase: ")
print(soup.title.text)

#tarea scraping: extraer los enlaces de 5 pág. 
###########################################
#Pag #1
url1 = "https://classroom.google.com/"
response1 = requests.get(url1)
print("Estado: ",{response1.status_code})
soup1 = BeautifulSoup(response1.text, 'lxml')
print("Área de clases: ")
print(soup1.title.text)

# #Pag #2
url2 = "https://games4ndchill.com/en/"
response2 = requests.get(url2)
print("Estado: ",{response2.status_code})
soup2 = BeautifulSoup(response2.text, 'lxml')
print("Guia de VideoJuegos: ")
print(soup2.title.text)

#Pag #3
url3 = "https://www.cinemarkca.com/el-salvador/"
response3 = requests.get(url3)
print("Estado: ",{response3.status_code})
soup3 = BeautifulSoup(response3.text, 'lxml')
print("Cine: ")
print(soup3.title.text)

# #Pag #4
url4 = "https://www.thecoffeecup.com.sv/"
response4 = requests.get(url4)
print("Estado: ",{response4.status_code})
soup4 = BeautifulSoup(response4.text, 'lxml')
print("Cafeteria: ")
print(soup4.title.text)

# #Pag #5
url5 = "https://sp.victoriassecret.com/sv/"
response5 = requests.get(url5)
print("Estado: ",{response5.status_code})
soup5 = BeautifulSoup(response5.text, 'lxml')
print("Titulo: ")
print(soup5.title.text)