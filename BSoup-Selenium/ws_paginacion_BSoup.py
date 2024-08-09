import time
from bs4 import BeautifulSoup
import requests

root = 'https://subslikescript.com'
website = root + '/movies_letter-A'
result = requests.get(website)
content = result.text

soup = BeautifulSoup(content, 'lxml')

pagination=soup.find('ul', class_='pagination')
pages = pagination.find_all('li',class_='page-item')
last_page = pages[-2].text

for page in range(1, int(last_page)+1)[:2]:
    result = requests.get(f'{website}?page={page}')
    content = result.text
    soup = BeautifulSoup(content, 'lxml')
    box = soup.find('article', class_='main-article')
    links = []

    for link in box.find_all('a', href=True):
        links.append(link['href'])

    #print(links)

    for link in links:
        try:
            #websites = f'{root}{link}'
            #print(websites)
            print(link)
            results = requests.get(f'{root}{link}')
            contents = results.text

            soups = BeautifulSoup(contents, 'lxml')
            #print(soups.prettify())
            boxs = soups.find('article', class_='main-article')
            titles = boxs.find('h1').get_text()
            transcripts = boxs.find('div', class_='full-script').get_text(strip=True, separator=' ')
            with open(titles + '.txt', 'w') as file:
                file.write(transcripts)
        except:
            #print("Dato no encontrado")         
            #pass
            print('-----------LINK NO FUNCIONA-----------------')
            print(link)
        
    for link in links:
        time.sleep(1)