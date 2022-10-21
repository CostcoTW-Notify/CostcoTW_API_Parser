from app.models.product import Product
from json import loads


def test_Product_parse():
    text = ''
    with open('test/products.json', 'r', encoding='utf-8') as file:
        text = file.read()

    json = loads(text)

    product = Product.parse(json)

    assert product.code == '217455'
    assert product.zhName == 'Ariel 抗菌抗臭洗衣精補充包 1260公克 X 6入'
    assert product.price == 719
    assert product.onSaleInfo is not None
    assert product.onSaleInfo.basePrice == 899
    pass
