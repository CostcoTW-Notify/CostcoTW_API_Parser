from typing import Optional
from datetime import datetime
from app.models.mongo.product import Product, KeyValuePair, DecalInfo, OnSaleInfo, StockStatus


class ProductHelper:

    @staticmethod
    def parse(json: dict):

        dInfo: list[KeyValuePair] = []
        if 'decalData' in json:
            for j in json['decalData']:
                key = j['key']
                value = j['value']
                altText = value['altText']
                position = value['position']
                url = value['url']
                info = DecalInfo(altText=altText, position=position, url=url)
                kv = KeyValuePair(key=key, value=info)
                dInfo.append(kv)

        deliveryName = json['deliveryName'] if 'deliveryName' in json else None
        price = json['price']['value'] if 'price' in json else None

        price = price
        deliveryName = deliveryName
        onSaleInfo: Optional[OnSaleInfo] = None
        if 'discountPrice' in json:
            onSaleInfo = OnSaleInfo(
                basePrice=json['basePrice']['value'], discountPrice=json['discountPrice']['value'])

        product = Product(
            code=json['code'],
            zhName=json['name'],
            engName=json['englishName'],
            stockStatus=StockStatus(
                inStock=True if json['stock']['stockLevelStatus'] == 'inStock' else False,
                stockLevel=json['stock']['stockLevel'] if 'stockLevel' in json['stock'] else None
            ),
            decalData=dInfo,
            url=json['url'],
            deliveryName=deliveryName,
            price=price,
            onSaleInfo=onSaleInfo,
            hidePriceValue=False,
            snapshotTime=datetime.utcnow()
        )

        return product
