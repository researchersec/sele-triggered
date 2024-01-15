
import sqlite3
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

def scrape_website(url, num_scrolls):
    service = Service(executable_path=r'chromedriver')
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)

    SCROLL_PAUSE_TIME = 3
    PRODUCT_HEIGHT = 300

    try:
        for _ in range(num_scrolls):
            driver.execute_script(f"window.scrollBy(0, {PRODUCT_HEIGHT});")
            time.sleep(SCROLL_PAUSE_TIME)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        articles = soup.find_all('article', class_='col-12 col-sm-6 col-lg-4')

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()
        return articles

def main():
    url = "https://www.supervin.dk/vin/rodvin?Products%5BrefinementList%5D%5Bfacet_types%5D%5B0%5D=R%C3%B8dvin"

    # Experiment with different numbers of scrolls
    for num_scrolls in range(5, 2500, 5):
        articles = scrape_website(url, num_scrolls)
        print(f"Number of scrolls: {num_scrolls}, Number of wines: {len(articles)}")

if __name__ == "__main__":
    main()
