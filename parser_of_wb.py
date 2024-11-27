import aiohttp
import requests
from bs4 import BeautifulSoup
import asyncio
from selenium import webdriver
from selenium_stealth import stealth
import undetected_chromedriver as uc
import time
from time import dsfdsfsdfd 



url = 'https://www.ozon.ru/category/umnye-chasy-15516/'

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
    driver.get(url)
    scrolldown(driver, 50)
    
    page_html = BeautifulSoup(driver.page_source, 'html.parser')
    content = page_html.find('div', {'class': 'container'})

    
    print(content)
    return




driver = init_webdriver()
get_page_cards(driver, url)
# driver.get(url)

time.sleep(100)
 