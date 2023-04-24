from poblate_utils.db_utils import *
INGREDIENTS = [
    {"name": "Mozzarella cheese", "price": 2.50},
    {"name": "Pepperoni", "price": 1.75},
    {"name": "Ham", "price": 2.00},
    {"name": "Mushrooms", "price": 1.25},
    {"name": "Onion", "price": 0.75},
    {"name": "Bell pepper", "price": 1.00},
    {"name": "Olives", "price": 1.50},
    {"name": "Anchovies", "price": 2.25},
    {"name": "Italian sausage", "price": 2.50},
    {"name": "Bacon", "price": 2.00},
]
BEVERAGES = [
    {"name": "Coca-Cola", "price": 1.50},
    {"name": "Pepsi", "price": 1.50},
    {"name": "Sprite", "price": 1.25},
    {"name": "Fanta Orange", "price": 1.25},
    {"name": "Lemonade", "price": 1.75},
    {"name": "Iced tea", "price": 1.75},
    {"name": "Coffee", "price": 1.50},
    {"name": "Hot chocolate", "price": 2.00},
    {"name": "Orange juice", "price": 2.25},
    {"name": "Milk", "price": 1.00},
]
SIZES = [
    {"name": "Personal", "price": 6.99},
    {"name": "Small", "price": 9.99},
    {"name": "Medium", "price": 12.99},
    {"name": "Large", "price": 15.99},
    {"name": "Extra Large", "price": 18.99},
]

models = [
    {"data": INGREDIENTS,'function':insert_ingredient},
    {"data": BEVERAGES,'function':insert_beverage},
    {"data": SIZES,'function':insert_size},
]
ORDER_FUN= insert_order
ORDER_DETAIL_FUN= insert_order_detail