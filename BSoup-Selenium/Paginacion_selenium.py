from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd
import time
optiones = Options()
optiones.headless = False     #activa o desactiva q se compile en segudno plano
#optiones.add_argument('window-size=1920x1080')


#web='https://www.audible.com/search'
web='https://www.audible.com/es_US/adblbestsellers?ref_pageloadid=not_applicable&ref=a_search_t1_navTop_pl0cg1c0r0&pf_rd_p=3c510bf6-cff4-47d1-bb27-1ba091ebb823&pf_rd_r=RN2RXND2QNBSHQP6R4JK&pageLoadId=TCnbnwzmyJy1GnVP&creativeId=7ba42fdf-1145-4990-b754-d2de428ba482'
path = r"C:\Users\ERICK\Downloads\chromedriver-win64\chromedriver.exe"

driver= webdriver.Chrome(service=Service(path),options=optiones)

driver.get(web)
driver.maximize_window()

##paginacion
pagination = driver.find_element(By.XPATH,'//ul[contains(@class,"pagingElements")]')
pages = pagination.find_elements(By.TAG_NAME,'li')
last_page = int(pages[-2].text)


current_page =1
book_title = []
book_author = []
book_length = []

while current_page <=last_page:
    time.sleep(2) ##espera implicita
    
    
    #container = driver.find_element(By.CLASS_NAME,'adbl-impression-container')
    container = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CLASS_NAME,'adbl-impression-container')))    ##espera explicita
    #productos = container.find_elements (By.XPATH,'.//li[contains(@class, "productListItem")]')
    productos = WebDriverWait(driver,5).until(EC.presence_of_all_elements_located((By.XPATH,'.//li[contains(@class, "productListItem")]'))) ##espera explicita
    for product in productos:
        book_title.append(product.find_element(By.XPATH,'.//h3[contains(@class, "bc-heading")]').text)
        book_author.append(product.find_element(By.XPATH,'.//li[contains(@class, "authorLabel")]').text)
        book_length.append(product.find_element(By.XPATH,'.//li[contains(@class, "runtimeLabel")]').text)

    current_page=current_page+1
    
    try:
        next_page = driver.find_element(By.XPATH,'//span[contains(@class,"nextButton")]')
        next_page.click()
    except:
        pass

driver.quit()

df_books = pd.DataFrame({'title':book_title,'Author':book_author,'lenght':book_length})
df_books.to_csv('books_pagination.csv',index=False)    
