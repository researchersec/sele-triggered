from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import psutil

url = "https://www.supervin.dk/vin/rodvin?Products%5BrefinementList%5D%5Bfacet_types%5D%5B0%5D=R%C3%B8dvin"

service = Service(executable_path=r'chromedriver')
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')

driver = webdriver.Chrome(service=service, options=options)
driver.get(url)

# Wait for the page to fully load
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

# Function to check if new content is still loading
def is_loading():
    loading_divs = driver.find_elements(By.CLASS_NAME, 'loading-wrapper')
    return any(loading_div.is_displayed() for loading_div in loading_divs)

# Scroll until no more content is loaded
while True:
    # Scroll to the end of the page using "END" key
    print("Scrolling to the end of the page...")
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    
    # Wait for a short time to let the content load after scrolling to the end
    driver.implicitly_wait(2)

    # Let new content load by scrolling up three times using "PAGE_UP" key
    for _ in range(3):
        print("Scrolling up to let new content load...")
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_UP)
        # Wait for a short time to let the content load after scrolling up
        driver.implicitly_wait(2)

    # Check if more content is still loading
    if not is_loading():
        break

    # Get the HTML content of the page
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    articles = soup.find_all('article', class_='col-12 col-sm-6 col-lg-4')

    # Print the number of articles and memory usage
    process = psutil.Process()
    print(f"Number of articles after scroll: {len(articles)}, Memory Usage: {process.memory_info().rss / 1024 / 1024} MB")

# Get the final height of the loaded page
final_page_height = driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );")

print(f"The height of the loaded page is: {final_page_height} pixels")

# Close the browser
driver.quit()
