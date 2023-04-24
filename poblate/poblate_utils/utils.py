from faker import Faker
import random
import datetime

fake = Faker()

def generate_random_date():
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    microsecond = random.randint(0, 999999)

    # Get the current year
    current_year = datetime.date.today().year

    # Construct the datetime object with the current year, random month, day, hour, minute, second, and microsecond
    random_datetime = datetime.datetime(
        current_year, month, day, hour, minute, second, microsecond
    )

    # Format the datetime as needed
    random_datetime_string = random_datetime.strftime("%Y-%m-%d %H:%M:%S.%f")
    return random_datetime_string




def create_models(cursor , data, fun):
    for element in data:
        fun( cursor,element)

def create_orders(cursor , order_data,beverage_detail, ingredient_detail, order_fun, order_detail_fun):

    order_fun( cursor,order_data)
    order_id = cursor.lastrowid
    for beverage in beverage_detail:
        order_detail_fun( cursor,beverage,order_id)
    for ingredient in ingredient_detail:
        order_detail_fun( cursor,ingredient,order_id)

def generate_random_list_of_ids(limit):
    length = random.randint(1, limit)
    id_set = set()
    while len(id_set) < length:
        id_set.add(fake.random_int(min=1, max=limit))
    random_list = list(id_set)
    return random_list


def generate_random_list_of_names():
    names = [fake.name() for _ in range(350)]
    return names


def create_ramdon_order(fake_names,INGREDIENTS,BEVERAGES,SIZES):
    name = fake_names[fake.random_int(min=0, max=349)]
    dni = fake.random_int(min=10000000, max=99999999)
    phone_number = fake.phone_number()
    address = fake.address()
    size_id = fake.random_int(min=1, max=5)
    date = generate_random_date()

    # Generate a random list of ingredients, beverages
    ingredients = generate_random_list_of_ids(10)
    beverages = generate_random_list_of_ids(10)
    total = calculate_total_prize(size_id,ingredients,beverages,INGREDIENTS,BEVERAGES,SIZES)
    order_data = {
        "client_name": name,
        "client_dni": dni,
        "state": "finish",
        "client_address": address,
        "client_phone": phone_number,
        "size_id": size_id,
        "date": date,
        "total":total
    }

    ingredient_detail = [{'ingredient_id':ingredient,'ingredient_price':INGREDIENTS[ingredient-1]['price'],'beverage_id':None,'beverage_price':None} for ingredient in ingredients]
    beverage_detail = [{'ingredient_id':None,'ingredient_price':None,'beverage_id':beverage,'beverage_price':BEVERAGES[beverage-1]['price']} for beverage in beverages]
    return order_data,ingredient_detail,beverage_detail

def calculate_total_prize(size_id, ingredients, beverages,INGREDIENTS,BEVERAGES,SIZES):
    total_size_price = SIZES[size_id-1]['price']
    total_ingredients_price = sum(INGREDIENTS[ingredient-1]['price'] for ingredient in ingredients)
    total_beverages_price = sum(BEVERAGES[beverage-1]['price'] for beverage in beverages)
    return round((total_size_price + total_ingredients_price + total_beverages_price),2)