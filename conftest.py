import pytest
import helpers
from data.data import URLS
from api_methods.user_methods import UserMethods
from api_methods.orders_methods import OrdersMethods
from api_methods.ingredients_methods import IngredientsMethods

@pytest.fixture
def user_methods():
    user_url = f'{URLS.BASE}/auth'
    user_methods = UserMethods(user_url)
    return user_methods

@pytest.fixture
def orders_methods():
    orders = f'{URLS.BASE}/orders'
    orders_methods = OrdersMethods(orders)
    return orders_methods

@pytest.fixture(scope="session")
def ingredients_methods() -> IngredientsMethods:
    ingredients = f'{URLS.BASE}/ingredients'
    ingredients_methods = IngredientsMethods(ingredients)
    return ingredients_methods

@pytest.fixture
def create_user(user_methods):
    users_to_delete = []

    def _create_user(email=None, password=None, name=None):
        payload = helpers.register_new_user()
        if email:    payload["email"] = email
        if password: payload["password"] = password
        if name:     payload["name"] = name

        resp = user_methods.registration_user(payload)
        users_to_delete.append({"email": payload["email"], "password": payload["password"]})

        return {"response": resp, "payload": payload}

    yield _create_user

    for creds in users_to_delete:
        login_resp = user_methods.auth_user({"email": creds["email"], "password": creds["password"]})
        if login_resp.status_code == 200:
            token = login_resp.json()["accessToken"]
            user_methods.delete_user(token)

@pytest.fixture
def auth_user(create_user, user_methods):
    user = create_user()["payload"]
    login = user_methods.auth_user(user)
    return login
