from typing import Optional
from app.models import Product
import httpx


def _convert_products(products: list):
    return [Product.parse(p) for p in products]


async def _fetch_from_costco_tw(category: Optional['str'] = None) -> list[Product]:
    costco_url = 'https://www.costco.com.tw/rest/v2/taiwan/products/search'
    params = {
        'pageSize': '100',
        'currentPage': 0,
        'sort': 'price-asc',
        'lang': 'zh_TW',
        'curr': 'TWD'
    }

    if category is not None:
        # params['category'] = 'hot-buys'
        params['category'] = category

    products: list[Product] = []
    curr_page = 0
    max_page = float('inf')
    error_count = 0
    error_code = 0
    error_msg = ''

    async with httpx.AsyncClient() as client:
        client.timeout = httpx.Timeout(10)
        while curr_page < max_page:
            if error_count > 2:
                raise Exception({
                    'error_code': error_code,
                    'error_msg': error_msg
                })

            params['currentPage'] = curr_page

            headers = client.headers
            headers['User-Agent'] += " CostcoTW-Notify/0.1"
            headers['Accept'] = 'application/json'
            client.headers = headers

            try:
                response = await client.get(costco_url, params=params, headers=headers)
            except Exception as err:
                error_count += 1
                error_code = -1
                error_msg = str(err)
                continue

            if (response.status_code != 200):
                error_count += 1
                error_code = response.status_code
                error_msg = response.text
                continue

            json = response.json()
            curr_page += 1

            products = products + _convert_products(json['products'])

            if (max_page == float('inf')):
                max_page = json['pagination']['totalPages']

            error_count = 0

            print(f'fetch {curr_page}/{max_page} ...')

    return products


async def fetch_all_products() -> list[Product]:

    all_products = await _fetch_from_costco_tw()

    return all_products


async def fetch_category_products(category: str) -> list[Product]:

    products_in_category = await _fetch_from_costco_tw(category)

    return products_in_category
