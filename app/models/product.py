from typing import Optional, TypedDict
from datetime import datetime


class OnSaleInfo(TypedDict):
    # 原價
    basePrice: int
    # 減價金額
    discountPrice: int


class StockStatus(TypedDict):
    # 是否在庫
    inStock: bool
    # 庫存數量
    stockLevel: Optional['int']


class DecalInfo(TypedDict):
    altText: str
    position: int
    url: str


class KeyValuePair(TypedDict):
    key: str
    value: DecalInfo


class Product(TypedDict):
    # 商品編號
    code: str
    # 中文名稱
    zhName: str
    # 英文名稱
    engName: str
    # 出貨類型 eg. Costco Food or Costco Frozen
    deliveryName: Optional['str']
    # 售價
    price: Optional['int']
    # 特價資訊
    onSaleInfo: Optional['OnSaleInfo']
    # 庫存資訊
    stockStatus: StockStatus
    # 商品連結
    url: str
    # 是否為需登入才可查看價格的商品
    hidePriceValue: bool
    # Note
    decalData: Optional['list[KeyValuePair]']
    # 快照時間
    snapshotTime: datetime
