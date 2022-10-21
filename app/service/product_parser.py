from typing import Optional
from models import Product
import httpx

headers = {
    'user-agent': 'CostcoTW-Notify 0.1',
    'accept': 'application/json'
}


async def _fetch_from_costco_tw(category: Optional['str'] = None) -> list:
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

    products = []
    curr_page = 0
    max_page = float('inf')
    error_count = 0

    async with httpx.AsyncClient() as client:
        client.timeout = httpx.Timeout(10)
        while curr_page < max_page:
            if error_count > 2:
                raise Exception('Cannot access CostcoTW API...')

            params['currentPage'] = curr_page
            response: httpx.Response

            try:
                response = await client.get(costco_url, params=params, headers=headers)
            except:
                error_count += 1
                continue

            if (response.status_code != 200):
                error_count += 1
                continue

            json = response.json()
            curr_page += 1

            products = products + json['products']

            if (max_page == float('inf')):
                max_page = json['pagination']['totalPages']

            error_count = 0

            print(f'fetch {curr_page}/{max_page} ...')

    return products


async def fetch_all_products() -> list:

    all_products = await _fetch_from_costco_tw()

    prods = [Product.parse(p) for p in all_products]

    return prods
