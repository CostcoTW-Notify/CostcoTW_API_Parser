from typing import Optional
from app.models.product import Product


class NotifyMessageHelper:

    @staticmethod
    def build_new_onsale_item_notify_message(product: Product) -> str:

        if product['onSaleInfo'] is None or product['price'] is None:
            raise Exception('received not onsale item')

        price = int(product['price'])
        basePrice = int(product['onSaleInfo']['basePrice'])
        discountPrice = int(product['onSaleInfo']['discountPrice'])

        message = "\n"
        message += "每日新特價商品情報 :\n\n"
        message += f"商品編號 : #{product['code']}\n"
        message += f"{product['zhName']}\n"
        message += f"特價: ${price} (${basePrice} - ${discountPrice})\n\n"
        message += f"https://www.costco.com.tw{product['url']}\n"

        return message

    @staticmethod
    def build_new_best_buy_item_notify_message(product: Product) -> str:

        if product['price'] is None:
            raise Exception('Received priceless item')

        message = "\n"
        message += "每日最佳價格商品情報 :\n\n"
        message += f"商品編號 : #{product['code']}\n"
        message += f"{product['zhName']}\n"
        message += f"特價 : ${int(product['price'])}\n\n"
        message += f"https://www.costco.com.tw{product['url']}\n"

        return message

    @staticmethod
    def build_product_in_stock_notify_message(product: Product) -> str:

        if product['stockStatus']['inStock'] is False:
            raise Exception('Received out of stock item')

        stock_count = product['stockStatus']['stockLevel']
        if stock_count is None:
            stock_count = "充足"

        message = "\n"
        message += "庫存追蹤商品通知 :\n\n"
        message += f"商品編號 #{product['code']}\n"
        message += f"{product['zhName']}\n"
        if product['price'] is None:
            message += f"售價: 請登入 Costco 查看\n"
        else:
            message += f"售價: ${int(product['price'])}\n"
        message += f"已重新上架,目前庫存數量: {stock_count}\n\n"
        message += f"https://www.costco.com.tw{product['url']}\n"

        return message
