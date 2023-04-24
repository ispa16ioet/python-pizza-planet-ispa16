from typing import Tuple
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

from ..repositories.managers import (
    IngredientManager,
    OrderManager,
    SizeManager,
    BeverageManager,
)


class OrderState(object):
    def __init__(self, context):
        self.context = context

    def updateState(self):
        try:
            self.order_detail = self.manager.update(
                _id=self.id, new_values={"state": self.name}
            )
            self.order_error = None
        except (SQLAlchemyError, RuntimeError) as ex:
            self.order_detail = None
            self.order_error = str(ex)


class Default(OrderState):
    name = "Default"
    manager = OrderManager
    order_detail = ""
    order_error = ""

    def get_orders(self, method):
        try:
            self.order_detail = method()
            self.order_error = None
        except (SQLAlchemyError, RuntimeError) as ex:
            self.order_detail = None
            self.order_error = str(ex)

    def get_all_orders(self):
        self.get_orders(self.manager.get_all)

    def get_order_by_id(self, _id):
        self.get_orders(lambda: self.manager.get_by_id(_id))


class CreateOrder(OrderState):
    order_detail = ""
    order_error = ""
    name = "OrderRealized"
    manager = OrderManager
    __required_info = (
        "client_name",
        "client_dni",
        "client_address",
        "client_phone",
        "size_id",
    )

    @staticmethod
    def check_required_keys(keys: Tuple[str, ...], element: dict[str, any]) -> bool:
        """Check if all the required keys are present in the given dictionary."""
        return all(element.get(key) for key in keys)

    @staticmethod
    def calculate_order_price(
        size_price: float, ingredients: list, beverages: list
    ) -> float:
        price = (
            sum(ingredient.price for ingredient in ingredients)
            + size_price
            + sum(beverage.price for beverage in beverages)
        )
        return round(price, 2)

    def create(self, order: dict):
        """Create and save order object on database."""
        current_order = order.copy()
        if not self.check_required_keys(self.__required_info, current_order):
            return "Invalid order payload", None

        if not current_order.get("state"):
            current_order["state"] = self.name

        if current_order.get("date"):
            current_order["date"] = datetime.strptime(
                current_order["date"], "%Y-%m-%d %H:%M:%S.%f"
            )

        size_id = current_order.get("size_id")
        size = SizeManager.get_by_id(size_id)

        if not size:
            return "Invalid size for Order", None

        ingredient_ids = current_order.pop("ingredients", [])
        beverage_ids = current_order.pop("beverages", [])
        try:
            ingredients = IngredientManager.get_by_id_list(ingredient_ids)
            beverages = BeverageManager.get_by_id_list(beverage_ids)
            price = self.calculate_order_price(
                size.get("price"), ingredients, beverages
            )
            order_with_price = {**current_order, "total_price": price}
            self.order_detail = self.manager.create(
                order_data=order_with_price,
                ingredients=ingredients,
                beverages=beverages,
            )
            self.order_error = None
        except (SQLAlchemyError, RuntimeError) as ex:
            self.order_detail = None
            self.order_error = str(ex)


class OnPreparing(OrderState):
    def __init__(self, order_detail):
        self.order_detail = order_detail.order_detail
        self.manager = OrderManager
        self.name = "OnPreparing"
        self.order_detail["state"] = self.name
        self.id = order_detail.order_detail["_id"]
        self.updateState()


class Sended(OrderState):
    def __init__(self, order_detail):
        self.order_detail = order_detail.order_detail
        self.manager = OrderManager
        self.name = "Sended"
        self.order_detail["state"] = self.name
        self.id = order_detail.order_detail["_id"]
        self.updateState()


class Finish(OrderState):
    def __init__(self, order_detail):
        self.order_detail = order_detail.order_detail
        self.manager = OrderManager
        self.name = "Finish"
        self.order_detail["state"] = self.name
        self.id = order_detail.order_detail["_id"]
        self.updateState()
