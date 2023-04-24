from enum import Enum
from typing import Any, Callable, Dict, Tuple, Union

from flask import jsonify

from app.controllers.report import ReportController
from ..order.order_state import OnPreparing, Sended, Finish


class OrderState(Enum):
    ORDER_REALIZED = "OrderRealized"
    ON_PREPARING = "OnPreparing"
    SENDED = "Sended"
    FINISH = "Finish"


def entity_controller_action(
    action: Callable[..., Union[Dict[str, Any], Tuple[Dict[str, Any], str]]],
    parm: Any = None,
) -> Tuple[str, int]:
    """Run the given action on an entity and return the result as a JSON response."""
    if parm:
        entity_data, error = action(parm)
    else:
        entity_data, error = action()

    response = entity_data if not error else {"error": error}
    status_code = 200 if not error else 400
    return jsonify(response), status_code


def state_control_action(new_order: Any) -> Tuple[str, int]:
    """Get the state of the given order and return it as a JSON response."""
    response = (
        new_order.order_detail
        if not new_order.order_error
        else {"error": new_order.order_error}
    )

    status_code = 200 if not new_order.order_error else 400
    return jsonify(response), status_code


def change_order_state(new_order: Any) -> None:
    """Change the state of the given order based on its current state."""
    current_state = OrderState(new_order.order_detail["state"])
    if current_state == OrderState.ORDER_REALIZED:
        new_order.set_state(OnPreparing(new_order))
    elif current_state == OrderState.ON_PREPARING:
        new_order.set_state(Sended(new_order))
    elif current_state == OrderState.SENDED:
        new_order.set_state(Finish(new_order))


def generate_report() -> Tuple[str, int]:
    most_common_ingredients = ReportController.get_most_common_ingredient()
    less_common_ingredient = ReportController.get_less_common_ingredient()
    months_with_more_revenue = ReportController.get_months_with_more_revenue()
    best_clients = ReportController.get_best_clients()
    worst_clients = ReportController.get_worst_clients()

    report = [
        {
            "report_name": "Most Common Ingredients",
            "report_id": "most_common_ingredients",
            "description": " most common ingredients used in the current year",
            "data": most_common_ingredients,
            "symbol": "",
        },
        {
            "report_name": "Less Common Ingredient",
            "report_id": "less_common_ingredient",
            "description": " less common ingredients used in the current year",
            "data": less_common_ingredient,
            "symbol": "",
        },
        {
            "report_name": "Months With More Revenue",
            "report_id": "months_with_more_revenue",
            "description": " months with more revenue in the current year",
            "data": months_with_more_revenue,
            "symbol": "$",
        },
        {
            "report_name": "Best Clients",
            "report_id": "best_clients",
            "description": " clients that had waste the most in the current year",
            "data": best_clients,
            "symbol": "$",
        },
        {
            "report_name": "Worst Clients",
            "report_id": "worst_clients",
            "description": " clients that had waste the less in the current year",
            "data": worst_clients,
            "symbol": "$",
        },
    ]
    status_code = 200 if report else 400
    return jsonify(report), status_code
