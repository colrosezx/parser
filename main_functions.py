from selenium import webdriver
from selenium_stealth import stealth
import time
from selenium.webdriver.chrome.options import Options
import asyncio

def get_chrome_options():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Запуск в фоновом режиме
    return chrome_options

def init_webdriver():
    chrome_options = get_chrome_options()
    driver = webdriver.Chrome(options=chrome_options)
    stealth(driver, platform='Win64')
    return driver

def scrolldown(driver, deep):
    for _ in range(deep):
        driver.execute_script('window.scrollBy(0, 500)')
        time.sleep(0.1)