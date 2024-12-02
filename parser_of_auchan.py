import asyncio
import aiohttp
from main_functions import init_webdriver
import json
from database import insert_into_database



async def fetch_requests(session, url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            try:
                return await response.json()

            except aiohttp.ClientError as e:
                print(f'Error: {e}')

            except json.JSONDecodeError as Jse:
                print(f'Error: {Jse}')

async def get_page_info(url):
    async with aiohttp.ClientSession() as session:
        json_data = await fetch_requests(session, url)
        
        for item in json_data:
            product_name = item['Name']
            product_url = item['Url']
            product_article = item['ItemId']
            product_description = item['Description']
            price_without_discount = item['OldPrice']
            price_with_discount = item['Price']
            quantity_of_goods = item['Weight']
            marketplace = 'Auchan'

            if price_without_discount == 0:
                price_without_discount = price_with_discount
                price_with_discount = None

            if price_with_discount:
                price_with_discount = round(price_with_discount, 2)
            price_without_discount = round(price_without_discount, 2)

            insert_into_database(marketplace, product_url, product_article,
                                 product_name, price_without_discount,
                                 price_with_discount, quantity_of_goods,
                                 product_description)

async def main():
    
    tasks = []
    for num_page in range(1, 4):
        task = asyncio.create_task(get_page_info(f'https://api.retailrocket.ru/api/2.0/recommendation/popular/5ecce55697a525075c900196/?&stockId={num_page}&categoryIds=&categoryPaths=%D0%97%D0%BE%D0%BE%D1%82%D0%BE%D0%B2%D0%B0%D1%80%D1%8B&session=65882e1d3c1a03d818276ed6&pvid=571272754473881&isDebug=false&format=json'))
        tasks.append(task)

    await asyncio.gather(*tasks)

asyncio.run(main())

