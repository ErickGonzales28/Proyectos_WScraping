from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import pandas as pd


website = 'https://www.adamchoi.co.uk/teamgoals/detailed'
path = r"C:\Users\ERICK\Downloads\chromedriver-win64\chromedriver.exe"

#service = Service(path)

driver = webdriver.Chrome(service=Service(path))
 
driver.get(website)

all_matches_button = driver.find_element(By.XPATH, '//label[@analytics-event="All matches"]')

all_matches_button.click()

time.sleep(2)

dropdown = Select(driver.find_element(By.ID,'country'))
dropdown.select_by_visible_text('Spain')

time.sleep(2)

partidos = driver.find_elements(By.TAG_NAME,'tr')

partds =[]

for match in partidos:
    #print(match.text)
    partds.append(match.text)

driver.quit()

df=pd.DataFrame({'PARTIDOS':partds})
print(df)
df.to_csv('partidos.csv', index=False)
