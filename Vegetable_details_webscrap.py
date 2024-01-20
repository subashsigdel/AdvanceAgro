import requests
from bs4 import BeautifulSoup
import json

URL = "https://kalimatimarket.gov.np/"
r = requests.get(URL)

soup = BeautifulSoup(r.content, 'lxml')

# Check if the 'commodityDailyPrice' div exists on the page
table = soup.find('table', attrs={'id': 'commodityDailyPrice'})
if table:
    rows = table.find_all('tr')
    
    vegetables_data = []

    # Iterate through rows and extract data
    for row in rows:
        columns = row.find_all('td')
        
        if columns:  # Check if the row has columns
            vegetable_name = columns[0].text.strip()
            vegetable_price = columns[1].text.strip()

            # Add the data to the vegetables_data list
            vegetables_data.append({
                'name': vegetable_name,
                'price': vegetable_price
            })

    # Save data in JSON format
    with open('vegetables_data.json', 'w', encoding='utf-8') as json_file:
        json.dump(vegetables_data, json_file, ensure_ascii=False, indent=2)

    print("Data saved successfully in vegetables_data.json")
else:
    print("Table with id 'commodityDailyPrice' not found on the page.")
