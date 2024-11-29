import aiohttp
# import requests
from bs4 import BeautifulSoup
import asyncio
from selenium import webdriver
from selenium_stealth import stealth
import undetected_chromedriver as uc
import time
from curl_cffi import requests
import json



url = 'https://www.ozon.ru/category/smartfony-15502/'

def init_webdriver():
    driver = webdriver.Chrome()
    stealth(driver,
            platform='Win64')
    
    return driver


def scrolldown(driver, deep):
    for _ in range(deep):
        driver.execute_script('window.scrollBy(0, 500)')
        time.sleep(0.1)



def get_page_cards(driver, url):
    massive_of_blocks_cards = []
    driver.get(url)
    scrolldown(driver, 100)
    
    page_html = BeautifulSoup(driver.page_source, 'html.parser')
    content = page_html.find('div', {'class': 'container'})
    content = content.findChildren(recursive=False)[-1].findChildren(recursive=False)[-1]
    content = content.findChildren(recursive=False)[2]
    content = content.find('div')
    content = content.findChildren(recursive=False)
    
    for list_of_cards in content: #Перебираем списки карточек в во всей странице
        list_of_cards = list_of_cards.find('div') 
        list_of_cards = list_of_cards.findChildren(recursive=False)

        for card in list_of_cards: #Перебираем карточки в списке карточек
            card_url = card.find('a', href=True)
            card_name = card.find('span', class_='tsBody500Medium')

            if card_url is None:
                print("Link not found in card")
                continue

            card_url_value = card_url["href"]

            # if card_name is None:
            #     print("Card name not found in card")
            #     continue

            # card_name_value = card_name.text
            get_info_about_card(card_url_value)
        

def get_info_about_card(card_url_value):
    session = requests.Session()
    try:
        raw_data = session.get(f'https://www.ozon.ru/api/composer-api.bx/page/json/v2?url={card_url_value}')
        raw_data.raise_for_status()  # Проверка на успешный HTTP-ответ
        json_data = raw_data.json()  # Метод .json() автоматически декодирует JSON

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при выполнении запроса: {e}")
        return
    
    except json.JSONDecodeError as e:
        print(f"Ошибка декодирования JSON: {e}")
        return

    if json_data is None:
        print("Card is not found")
        return

    # full_name = json_data['seo']['title']
    # print(full_name)
    product = json_data['seo']['title']


def collect_information_about_products(product_url, article, marketplace, 
                                       product_name, price_without_discount, 
                                       price_with_discount, quantity_of_goods) -> list:
    pass
    
    

        

    
    # content = content.find('div')
    

    
    # content = content.find('div')
    # content = content.findChildren(recursive=False)
    # content = content.find('a')
    # url_on_item = content
    # content = content.findChildren(recursive=False)

    

    # print(len(content))
    return






driver = init_webdriver()
get_page_cards(driver, url)
# driver.get(url)

time.sleep(100)
 