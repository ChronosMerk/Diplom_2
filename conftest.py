"""Этот модуль содержит фикстуры для тестов API."""
import pytest
import helpers
from data.data import URLS
from api_methods.user_methods import UserMethods
from api_methods.orders_methods import OrdersMethods
from api_methods.ingredients_methods import IngredientsMethods


@pytest.fixture
def user_methods():
    """
    Фикстура для создания экземпляра класса UserMethods.

    Возвращает:
        UserMethods: Экземпляр класса UserMethods.
    """
    user_url = f'{URLS.BASE}/auth'
    user_methods = UserMethods(user_url)
    return user_methods


@pytest.fixture
def orders_methods():
    """
    Фикстура для создания экземпляра класса OrdersMethods.

    Возвращает:
        OrdersMethods: Экземпляр класса OrdersMethods.
    """
    orders = f'{URLS.BASE}/orders'
    orders_methods = OrdersMethods(orders)
    return orders_methods


@pytest.fixture(scope="session")
def ingredients_methods() -> IngredientsMethods:
    """
    Фикстура для создания экземпляра класса IngredientsMethods с областью видимости "session".

    Возвращает:
        IngredientsMethods: Экземпляр класса IngredientsMethods.
    """
    ingredients = f'{URLS.BASE}/ingredients'
    ingredients_methods = IngredientsMethods(ingredients)
    return ingredients_methods


@pytest.fixture
def create_user(user_methods):
    """
    Фикстура для создания и последующего удаления пользователя.

    Эта фикстура создает пользователя с помощью API, а после выполнения теста
    удаляет его, чтобы не оставлять тестовые данные в системе.

    Аргументы:
        user_methods (UserMethods): Экземпляр класса UserMethods.

    Возвращает:
        function: Внутренняя функция для создания пользователя.
    """
    users_to_delete = []

    def _create_user(email=None, password=None, name=None):
        """
        Внутренняя функция для создания пользователя.

        Аргументы:
            email (str, optional): Email пользователя. По умолчанию None.
            password (str, optional): Пароль пользователя. По умолчанию None.
            name (str, optional): Имя пользователя. По умолчанию None.

        Возвращает:
            dict: Словарь с ответом от API и данными пользователя.
        """
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
    """
    Фикстура для создания и авторизации пользователя.

    Аргументы:
        create_user (function): Фикстура для создания пользователя.
        user_methods (UserMethods): Экземпляр класса UserMethods.

    Возвращает:
        requests.Response: Ответ от API на запрос авторизации.
    """
    user = create_user()["payload"]
    login = user_methods.auth_user(user)
    return login
