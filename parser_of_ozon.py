from bs4 import BeautifulSoup
from selenium import webdriver
from selenium_stealth import stealth
import time
from curl_cffi import requests
import json
from database import insert_into_database
from main_functions import init_webdriver
from main_functions import scrolldown

url = 'https://www.ozon.ru/category/smartfony-15502/'

def get_page_cards(driver, url):
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
            card_price_without_discount = card.find('span', class_='tsBodyControl400Small')
            card_price_with_discount = card.find('span', class_='tsHeadline500Medium')
            quantity_of_goods = card.find('span', class_='tsBody400Small')

            if card_url is None:
                print("url not found in card")
                continue

            if card_price_without_discount is None:
                card_price_without_discount = None
                continue

            if quantity_of_goods is None:
                quantity_of_goods = 0
                continue

            card_url_value = card_url["href"]
            card_price_without_discount = card_price_without_discount.text
            card_price_with_discount = card_price_with_discount.text
            quantity_of_goods = quantity_of_goods.text

            get_info_about_card(card_url_value, card_price_without_discount, 
                                card_price_with_discount, quantity_of_goods)

def get_info_about_card(card_url_value, card_price_without_discount,
                        card_price_with_discount, quantity_of_goods):
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

    try:
        product_name = json_data['seo']['title']
        if 'false' in product_name:
            product_name = product_name.replace('false', '')
        product_article = json.loads(json_data["seo"]["script"][0]["innerHTML"])['sku']
        product_description = json.loads(json_data['seo']['script'][0]['innerHTML'])['description']
    except:
        print('information_not_found')

    product_url = f'https://ozon.ru{card_url_value}'
    marketplace = 'Ozon'


    collect_information_about_products(marketplace, product_url, product_article, product_name, 
            card_price_without_discount, card_price_with_discount, 
            quantity_of_goods, product_description)


    


def collect_information_about_products(marketplace, product_url, product_article, 
                                        product_name, card_price_without_discount, 
                                        card_price_with_discount, quantity_of_goods,
                                        product_description) -> list:
    
    product_article = int(product_article)
    card_price_with_discount = card_price_with_discount.replace('\u2009', '')
    card_price_without_discount = card_price_without_discount.replace('\u2009', '')
    product_description = product_description.replace('\n', ' ')

    insert_into_database(marketplace, product_url, product_article, 
                        product_name, card_price_without_discount, 
                        card_price_with_discount, quantity_of_goods,
                        product_description)
    
    

driver = init_webdriver()
get_page_cards(driver, url)
time.sleep(100)