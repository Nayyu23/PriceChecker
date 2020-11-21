import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from requests_html import HTMLSession
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

#global

options = Options()
options.binary_location = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"
options = webdriver.ChromeOptions()
options.add_argument('-headless')
driver = webdriver.Chrome(chrome_options=options, executable_path="C:/WebTools/chromedriver.exe")
#driver.get('http://google.com/')

headers = {
    'Host': 'www.amazon.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'TE': 'Trailers'
}

# main

item = input('Enter item name: ')
print('Searching for ' + item + '...')

def ebaySearch(item):
    item = item.replace(' ', '+') #only for ebay

    print('Searching eBay...')
    URL = 'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313.TR12.TRC2.A0.H0.XTRS0&_nkw=' + item
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='mainContent')
    allListings = results.find_all('li', class_='s-item')

    runs = 0
    for listing in allListings:
        if runs >= 1: break
        element = listing.find('h3', class_='s-item__title')
        price = listing.find('span', class_='s-item__price')
        link = str(listing.find('a', class_='s-item__link'))
        if None in (element, price):
            continue
        print('eBay results:')
        print('Name: ' + element.text.strip())
        print('Price: ' + price.text.strip())
        start = link.find( 'http' )
        end = link.find( '">', start )
        res = link[start:end]
        print('Link: ' + res)
        print()
        print()
        runs += 1

    # save price
    ebay_price = price.text.strip()
    ebay_price = ebay_price.replace('$', '')
    try:
        ebay_price = float(ebay_price)
    except ValueError:
        if ('to' in ebay_price):
            start = ebay_price.find( '' )
            end = ebay_price.find( ' ', start )
            res = ebay_price[start:end]
            ebay_price = float(res)

def amazonSearch(item):
    item = item.replace(' ', '+')
    print("Searching Amazon...")

    URL = 'https://www.amazon.com/s?k=' + item
    driver.get(URL)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    runs = 0
    results = soup.findAll('span', attrs={'class': 'a-size-medium a-color-base a-text-normal'})
    for listing in results:
        if runs >= 1: break
        print(soup.select_one('span.a-size-medium').get_text())
        runs += 1

    runs = 0
    results = soup.findAll('span', attrs={'class': 'a-offscreen'})
    for listing in results:
        if runs >= 1: break
        element = soup.select_one('span.a-offscreen')
        if None in element:
            continue
        print(element.get_text())
        print()
        print()
        runs += 1

    # save price
    amazon_price = item_price.text.strip()
    amazon_price = amazon_price.replace('$', '')
    amazon_price = float(amazon_price)
    
ebaySearch(item)
amazonSearch(item)