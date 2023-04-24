import sqlite3

from constants import (
    models,
    ORDER_FUN,
    BEVERAGE_DETAIL_FUN,
    INGREDIENT_DETAIL_FUN,
    INGREDIENTS,
    BEVERAGES,
    SIZES,
)
from poblate_utils.utils import (
    generate_random_list_of_names,
    create_ramdon_order,
    create_models,
    create_orders,
)

conn = sqlite3.connect("../pizza.sqlite")
cursor = conn.cursor()
results = []
# check if database is empty
cursor.execute("SELECT * FROM size")
results.append(len(cursor.fetchall()))
cursor.execute("SELECT * FROM beverage")
results.append(len(cursor.fetchall()))
cursor.execute("SELECT * FROM ingredient")
results.append(len(cursor.fetchall()))


if sum(results) == 0:
    for model in models:
        create_models(cursor, model["data"], model["function"])
        fake_names = generate_random_list_of_names()
        for i in range(1, 200):
            order_data, ingredient_detail, beverage_detail = create_ramdon_order(
                fake_names, INGREDIENTS, BEVERAGES, SIZES
            )
            create_orders(
                cursor,
                order_data,
                ingredient_detail,
                beverage_detail,
                ORDER_FUN,
                INGREDIENT_DETAIL_FUN,
                BEVERAGE_DETAIL_FUN,
            )
    print("database poblated correctly")
else:
    print("The database needs to be empty to poblate correctly")


conn.commit()
conn.close()
