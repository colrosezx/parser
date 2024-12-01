from curl_cffi import requests
import json
import time
import asyncio
import aiohttp
from database import insert_into_database


async def fetch_requests(session, url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                    return await response.json()

    except aiohttp.ClientError as e:
        print(f"Error: {e}")
        return
    
    except json.JSONDecodeError as e:
        print(f"Ошибка декодирования JSON: {e}")
        return
    

async def get_info_about_cards(url):
    async with aiohttp.ClientSession() as session:
        json_data = await fetch_requests(session, url)
    
        for product in json_data['data']['products']:
                product_name = product['name']
                product_article = product['id']
                product_url = f'https://www.wildberries.ru/catalog/{product_article}/detail.aspx'
                price_with_discount = product['sizes'][0]['price']['total'] / 100
                price_without_discount = product['sizes'][0]['price']['basic'] / 100
                quantity_of_goods = product['totalQuantity']
                marketplace = 'Wildberries'

                insert_into_database(marketplace, product_url,
                                     product_article, product_name,
                                     price_without_discount, price_with_discount,
                                     quantity_of_goods, None)

async def main():
    num_pages = 3
    tasks = []

    for num_page in range(1, num_pages + 1):
        task = asyncio.create_task(get_info_about_cards(f'https://catalog.wb.ru/catalog/electronic22/v2/catalog?ab_testing=false&appType=1&curr=rub&dest=-5818883&page={num_page}&sort=popular&spp=30&subject=515'))
        tasks.append(task)
    
    await asyncio.gather(*tasks)


start_time = time.time()
asyncio.run(main())
end_time = time.time()

print(end_time-start_time)