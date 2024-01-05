from types import NotImplementedType
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
import sqlite3

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
num_scrolls = 3500 

for _ in range(num_scrolls):
    driver.execute_script(f"window.scrollBy(0, {PRODUCT_HEIGHT});")
    time.sleep(SCROLL_PAUSE_TIME)

soup = BeautifulSoup(driver.page_source, 'html.parser')
articles = soup.find_all('article', class_='col-12 col-sm-6 col-lg-4')

# Create or connect to a SQLite database file
conn = sqlite3.connect('wine_data.db')
cursor = conn.cursor()

# Create a table for wines if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS wines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        price_1 TEXT,
        price_6 TEXT,
        image_href TEXT,
        country TEXT
    )
''')


for article in articles:
    wine_name = article.find('h4').text.strip() if article.find('h4') else None
    
    # Find all spans with class 'price' within the article
    prices = article.find_all('span', class_='price')

    # Find all img tags within the article
    images = article.find_all('img')
    
    # Check if the prices list has at least two elements before accessing them
    if len(prices) >= 2 and len(images) >= 2:
        wine_price_1 = prices[0].text.strip().replace('DKK', '').strip()
        wine_price_6 = prices[1].text.strip().replace('DKK', '').strip()
        
        img_href_1 = images[0]['src'] if 'src' in images[0].attrs else None
        img_alt_2 = images[1]['alt'] if 'alt' in images[1].attrs else None

        # Check if the wine exists in the database
        cursor.execute('SELECT * FROM wines WHERE name = ?', (wine_name,))
        existing_wine = cursor.fetchone()

        print(wine_name)
        
        if existing_wine:
            # Update prices if the wine already exists
            cursor.execute('''
                UPDATE wines
                SET price_1 = ?, price_6 = ?, image_href = ?, country = ?
                WHERE id = ?
            ''', (wine_price_1, wine_price_6, img_href_1, img_alt_2, existing_wine[0]))
        else:
            # Insert data into the 'wines' table if the wine doesn't exist
            cursor.execute('''
                INSERT INTO wines (name, price_1, price_6, image_href, country)
                VALUES (?, ?, ?, ?, ?)
            ''', (wine_name, wine_price_1, wine_price_6, img_href_1, img_alt_2))
            
            wine_id = cursor.lastrowid  # Get the ID of the inserted wine
            

# Commit changes and close connection
conn.commit()
conn.close()

driver.quit()
