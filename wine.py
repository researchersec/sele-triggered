import re
import html
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import os

service = Service(executable_path=r'chromedriver')
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')

driver = webdriver.Chrome(service=service, options=options)

url = "https://www.supervin.dk/vin/rodvin?Products%5BrefinementList%5D%5Bfacet_types%5D%5B0%5D=R%C3%B8dvin"

driver.get(url)

SCROLL_PAUSE_TIME = 3  # Increase pause time
PRODUCT_HEIGHT = 300  # Adjust this value if needed

# Arbitrarily set a high number for num_scrolls to ensure reaching the end
num_scrolls = 1000

for _ in range(num_scrolls):
    driver.execute_script(f"window.scrollBy(0, {PRODUCT_HEIGHT});")
    time.sleep(SCROLL_PAUSE_TIME)

soup = BeautifulSoup(driver.page_source, 'html.parser')
articles = soup.find_all('article', class_='col-12 col-sm-6 col-lg-4')

for article in articles:
    wine_name = article.find('h4').text.strip() if article.find('h4') else None
    wine_price = article.find('span', class_='price').text.strip() if article.find('span', class_='price') else None
    print(wine_name, wine_price)

driver.quit()
