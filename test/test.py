import time
from selenium import webdriver
from bs4 import BeautifulSoup

URL = "https://kalimatimarket.gov.np/"
headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}

# Use the appropriate path to your WebDriver executable
driver = webdriver.Chrome(executable_path='/path/to/chromedriver')

try:
    driver.get(URL)
    time.sleep(5)  # Allow time for dynamic content to load
    page_source = driver.page_source
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    driver.quit()

soup = BeautifulSoup(page_source, 'html.parser')
price = []

# Adjust the HTML structure based on the actual structure of the website
price_table = soup.find('table', {'class': 'dt table-striped table-hover dataTable no-footer dtr-inline'})

if price_table:
    rows = price_table.find_all('tr')
    for row in rows:
        columns = row.find_all('td')
        if len(columns) >= 2:
            vegetable_name = columns[0].text.strip()
            vegetable_price = columns[1].text.strip()
            price.append({'vegetable': vegetable_name, 'price': vegetable_price})

# Now 'price' list contains the scraped data
print(price)
