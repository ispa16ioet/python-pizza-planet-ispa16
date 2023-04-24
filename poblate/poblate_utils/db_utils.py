from typing import Any, Dict, Tuple

def insert_order(cursor: Any, order: Dict[str, Any]) -> None:
    cursor.execute("""
        INSERT INTO `order` (`client_name`, `client_dni`, `client_address`, `client_phone`, `date`, `total_price`, `size_id`, `state`)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
     """, (order['client_name'], order['client_dni'], order['client_address'],
                 order['client_phone'], order['date'], order['total'], order['size_id'], order['state']))


def insert_order_detail(cursor: Any, order_detail: int, order_id: int) -> None:
    cursor.execute("""
        INSERT INTO `order_detail` (`order_id`, `beverage_id`, `beverage_price`,`ingredient_id`, `ingredient_price`)
        VALUES (?, ?, ?, ?, ?)
    """, (order_id, order_detail['beverage_id'], order_detail['beverage_price'], order_detail['ingredient_id'], order_detail['ingredient_price']))


def insert_size(cursor: Any, size: Dict) -> None:
    cursor.execute('''
        INSERT INTO size ( name, price)
        VALUES ( ?, ?)
    ''', (size['name'], size['price']))



def insert_ingredient(cursor: Any, ingredient: Dict) -> None:
    cursor.execute('''
        INSERT INTO `ingredient` ( name, price)
        VALUES ( ?, ?)
    ''', (ingredient['name'], ingredient['price']))


def insert_beverage(cursor: Any, beverage: Dict) -> None:
    cursor.execute('''
        INSERT INTO beverage ( name, price)
        VALUES ( ?, ?)
    ''', (beverage['name'], beverage['price']))
