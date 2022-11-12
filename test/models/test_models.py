import json
import pytest
from app.models.mongo.product import Product
from json import loads


@pytest.fixture()
def get_single_product_json():
    text = ''
    with open('test/models/products.json', 'r', encoding='utf-8') as file:
        text = file.read()
    json = loads(text)
    return json


def test_Product_parse(get_single_product_json):

    product = Product.parse(get_single_product_json)

    assert product.code == '217455'
    assert product.zhName == 'Ariel 抗菌抗臭洗衣精補充包 1260公克 X 6入'
    assert product.price == 719
    assert product.onSaleInfo is not None
    assert product.onSaleInfo.basePrice == 899


def test_Product_to_dict(get_single_product_json):

    product = Product.parse(get_single_product_json)
    prod_dict = product.to_dict()

    assert prod_dict['code'] == '217455'
    assert prod_dict['zhName'] == 'Ariel 抗菌抗臭洗衣精補充包 1260公克 X 6入'
    assert prod_dict['price'] == 719
    assert prod_dict['onSaleInfo'] is not None
    assert prod_dict['onSaleInfo']['basePrice'] == 899
