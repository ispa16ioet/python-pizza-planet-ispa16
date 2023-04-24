from typing import Tuple, List
from sqlalchemy.exc import SQLAlchemyError

from ..repositories.managers import ReportManager
from ..repositories.models import Ingredient, IngredientDetail, Order


class ReportController:
    @staticmethod
    def get_most_common_ingredient() -> Tuple[List[Ingredient], str]:
        try:
            most_common_ingredient = ReportManager.get_most_common_ingredient(
                model=IngredientDetail
            )
            return most_common_ingredient
        except (SQLAlchemyError, RuntimeError) as ex:
            return str(ex)

    @staticmethod
    def get_less_common_ingredient() -> Tuple[List[Ingredient], str]:
        try:
            less_common_ingredient = ReportManager.get_less_common_ingredient(
                model=IngredientDetail
            )
            return less_common_ingredient
        except (SQLAlchemyError, RuntimeError) as ex:
            return str(ex)

    @staticmethod
    def get_months_with_more_revenue() -> Tuple[List[Order], str]:
        try:
            months_with_more_revenue = ReportManager.get_months_with_more_revenue(
                model=Order
            )
            return months_with_more_revenue
        except (SQLAlchemyError, RuntimeError) as ex:
            return str(ex)

    @staticmethod
    def get_best_clients() -> Tuple[List[Order], str]:
        try:
            best_clients = ReportManager.get_best_clients(model=Order)
            return best_clients
        except (SQLAlchemyError, RuntimeError) as ex:
            return str(ex)

    @staticmethod
    def get_worst_clients() -> Tuple[List[Order], str]:
        try:
            worst_clients = ReportManager.get_worst_clients(model=Order)
            return worst_clients
        except (SQLAlchemyError, RuntimeError) as ex:
            return str(ex)
