from typing import Optional
from datetime import datetime


class OnSaleInfo:
    def __init__(self, basePrice: int, discountPrice: int) -> None:
        # 原價
        self.basePrice = basePrice
        # 減價金額
        self.discountPrice = discountPrice


class StockStatus:
    def __init__(self, inStock: bool) -> None:
        # 是否在庫
        self.inStock = inStock
        # 庫存水位
        self.stockLevel: Optional['int'] = None


class Product:

    def __init__(self,
                 code: str,
                 zhName: str,
                 engName: str,
                 stockStatus: StockStatus,
                 url: str) -> None:
        # 商品編號
        self.code = code
        # 中文名稱
        self.zhName = zhName
        # 英文名稱
        self.engName = engName
        # 出貨類型 eg. Costco Food or Costco Frozen
        self.deliveryName: Optional['str'] = None
        # 售價
        self.price: Optional['int'] = None
        # 特價資訊
        self.onSaleInfo: Optional['OnSaleInfo'] = None
        # 庫存資訊
        self.stockStatus = stockStatus
        # 商品連結
        self.url: str = url
        # 是否為需登入才可查看價格的商品
        self.hidePriceValue: bool = False
        # Note
        self.decalData: Optional['dict'] = None
        # 快照時間
        self.snapshotTime = datetime.utcnow()

    @property
    def now_on_sale(self):
        return self.onSaleInfo is not None

    @property
    def is_best_price(self):
        return self.price is not None and ((self.price - 7) % 10 == 0)

    @property
    def is_deal(self):
        return self._is_key_word_in_decal('decal_Toogood')

    @property
    def is_warehouse_only2(self):
        return self._is_key_word_in_decal('decal_WHS2')

    @property
    def is_warehouse_only(self):
        if self.decalData is not None:
            for x in self.decalData:
                if '賣場獨家' in x['value']['altText']:
                    return True
        return False

    @property
    def is_online_only(self):
        if self.decalData is not None:
            for x in self.decalData:
                if '網路獨家' in x['value']['altText']:
                    return True
        return False

    def _is_key_word_in_decal(self, keyword: str):
        if self.decalData is None:
            return False
        for x in self.decalData:
            if keyword in x['value']['url']:
                return True
        return False

    @classmethod
    def parse(cls, json: dict):

        code = json['code']
        name = json['name']
        englishName = json['englishName']
        stock_info = StockStatus(
            True if json['stock']['stockLevelStatus'] == 'inStock' else False)
        stock_info.stockLevel = json['stock']['stockLevel'] if 'stockLevel' in json['stock'] else None
        url = json['url']
        decalData = json['decalData'] if 'decalData' in json else None
        deliveryName = json['deliveryName'] if 'deliveryName' in json else None
        price = json['price']['value'] if 'price' in json else None

        prod = cls(
            code=code,
            zhName=name,
            engName=englishName,
            stockStatus=stock_info,
            url=url
        )
        prod.decalData = decalData
        prod.price = price
        prod.deliveryName = deliveryName
        if 'discountPrice' in json:
            prod.onSaleInfo = OnSaleInfo(
                json['basePrice']['value'], json['discountPrice']['value'])

        return prod

    def __repr__(self) -> str:
        return f'[{self.code}] {self.zhName} : {self.price}'

    def to_dict(self) -> dict:
        prod_dict = self.__dict__
        prod_dict['onSaleInfo'] = self.onSaleInfo.__dict__ if self.onSaleInfo is not None else None
        prod_dict['stockStatus'] = self.stockStatus.__dict__

        return prod_dict
