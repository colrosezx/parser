from curl_cffi import requests
from bs4 import BeautifulSoup
from main_functions import scrolldown
from main_functions import init_webdriver
import json
import time
import asyncio


async def get_page_cards(driver, url):
    driver.get(url)
    scrolldown(driver, 100)

    page_html = BeautifulSoup(driver.page_source, 'html.parser')
    content = page_html.find('div', {'class': 'product-card-list'})
    content = content.findChildren('article')
    tasks = []

    for card in content:
        product_url = card.find('div').find('a')['href']
        task = asyncio.create_task(process_card(driver, product_url))
        tasks.append(task)

    await asyncio.gather(*tasks)


async def process_card(driver, url):

    driver.get(url)
    page_html = BeautifulSoup(driver.page_source, 'html.parser')
    product_page = page_html.find('div', {'class': 'product-page'})
    card_name = product_page.find('h1', {'class': 'product-page__title'})

    print(f"Processing card: {card_name}")
    await asyncio.sleep(1)


async def main():
    base_url = 'https://www.wildberries.ru/catalog/elektronika/smartfony-i-telefony/vse-smartfony?page='
    num_pages = 3  # Количество страниц, которые вы хотите пропарсить

    driver = init_webdriver()
    tasks = []

    for num_page in range(1, num_pages + 1):
        task = asyncio.create_task(get_page_cards(driver, f'{base_url}{num_page}'))
        tasks.append(task)
    
    await asyncio.gather(*tasks)


start_time = time.time()
asyncio.run(main())
end_time = time.time()

print(end_time-start_time)