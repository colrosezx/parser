import aiohttp
import requests
from bs4 import BeautifulSoup
import asyncio
from selenium import webdriver
from selenium_stealth import stealth
import undetected_chromedriver as uc
import time


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

            if card_name is None:
                print("Card name not found in card")
                continue

            card_name_value = card_name.text
            print(f'Ссылка на карточку: {'https://www.ozon.ru'+card_url_value}, Название карточки: {card_name_value}')



        

    
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
 