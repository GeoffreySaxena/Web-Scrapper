import csv
from bs4 import BeautifulSoup
from msedge.selenium_tools import Edge, EdgeOptions

def get_url(webpage):
    
    url = webpage
    url += '?page{}'
    return url

def extract_record(item):
    atag = item.h5
    description = atag.text
    
    try:
        category = item.find('div', {'title': 'The Souled Store', 'class': 'col-12 listprice ecltext' }).text
        discounted_price_parent = item.find('div', {'class': 'row'}).text
        discounted_price = discounted_price_parent.split(" ", 1)[1] 
        
    except AttributeError:
        category =''
        discounted_price = ''
        
    result = (description, category, discounted_price)
    
    return result


def main(search_term):
    options = EdgeOptions()
    options.use_chromium = True
    driver = Edge(options = options)
    
    records = []
    url = get_url(search_term)
    
    for page in range(1, 7):
        driver.get(url.format(page))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find_all('div', {'class' : 'col-lg-3 col-md-6 col-6'})
        
        for item in results:
            record = extract_record(item)
            if record: 
                records.append(record)
    
    driver.close()
    
    with open('souled.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['description', 'category', 'discounted_price'])
        writer.writerows(records)
        
main('https://www.thesouledstore.com/men/t-shirts')
