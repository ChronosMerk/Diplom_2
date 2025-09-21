"""Этот модуль содержит тесты для создания и получения заказов."""
import allure
from data.data_message import LoginUserMessage, CreateOrdersMessage


@allure.title('Тесты создания и получения заказа')
class TestOrders:
    """Этот класс содержит тесты для создания и получения заказов."""

    @allure.title('Позитивный тест создания заказа с авторизованным пользователем')
    @allure.description('Создать и авторизоваться пользователем, получить валидные ID ингредиентов, создать заказ, проверить код ответа, статус и наличие номера заказа')
    def test_order_creation_authorized(self, orders_methods, auth_user, ingredients_methods):
        """
        Тестирует успешное создание заказа авторизованным пользователем.

        Шаги:
        1. Получает токен авторизации.
        2. Получает список ингредиентов.
        3. Создает заказ с одним ингредиентом.
        4. Проверяет, что код ответа равен 200.
        5. Проверяет, что в ответе содержится ID ингредиента.
        """
        token = auth_user.json()['accessToken']
        ingredients = ingredients_methods.get_ingredients()
        payload = {"ingredients": [ingredients.json()['data'][0]['_id']]}
        response = orders_methods.create_orders(payload, token)

        assert response.status_code == 200
        assert payload['ingredients'][0] in response.text

    @allure.title('Создание заказа неавторизованным пользователем')
    @allure.description('Создание заказа без авторизации. В данном запросе БАГ, он возвращает 200, а должен 401')
    def test_order_creation_not_authorized(self, orders_methods, ingredients_methods):
        """
        Тестирует создание заказа неавторизованным пользователем.

        Примечание:
            В этом тесте обнаружен баг. API возвращает код 200, хотя должен возвращать 401.

        Шаги:
        1. Получает список ингредиентов.
        2. Создает заказ с одним ингредиентом без токена авторизации.
        3. Проверяет, что код ответа равен 200 (ожидалось 401).
        4. Проверяет, что 'success' в ответе равно True.
        """
        ingredients = ingredients_methods.get_ingredients()
        payload = {"ingredients": [ingredients.json()['data'][0]['_id']]}
        response = orders_methods.create_orders(payload)

        assert response.status_code == 200
        assert response.json()["success"] is True

    @allure.title('Создание заказа с неверным хешем ингредиентов')
    @allure.description('Создание заказа с неверным хешем ингредиентов, проверка кода ответа и текста ошибки.')
    def test_order_creation_incorrect_hash_ingredient(self, orders_methods, auth_user):
        """
        Тестирует создание заказа с неверным хешем ингредиентов.

        Шаги:
        1. Получает токен авторизации.
        2. Создает заказ с неверным хешем ингредиента.
        3. Проверяет, что код ответа равен 400.
        4. Проверяет, что в ответе содержится правильное сообщение об ошибке.
        """
        token = auth_user.json()['accessToken']
        payload = {"ingredients": ['60d3463f7034a100269f45e7']}
        response = orders_methods.create_orders(payload, token)

        assert response.status_code == 400
        assert response.json()['message'] == CreateOrdersMessage.MESSAGE_CREATE_ORDERS_INCORRECT_HASH_INGREDIENT

    @allure.title('Создание заказа без добавления ингредиентов')
    @allure.description('Создание заказа без добавления ингредиентов, проверка кода ответа и текста ошибки.')
    def test_order_creation_not_ingredients(self, orders_methods, auth_user):
        """
        Тестирует создание заказа без добавления ингредиентов.

        Шаги:
        1. Получает токен авторизации.
        2. Создает заказ без ингредиентов.
        3. Проверяет, что код ответа равен 400.
        4. Проверяет, что в ответе содержится правильное сообщение об ошибке.
        """
        token = auth_user.json()['accessToken']
        response = orders_methods.create_orders(None, token)

        assert response.status_code == 400
        assert response.json()['message'] == CreateOrdersMessage.MESSAGE_CREATE_ORDERS_NOT_INGREDIENT

    @allure.title('Получение заказа конкретного пользователя по токену')
    @allure.description('Получение заказа конкретного пользователя по токену, проверка кода ответа и заказа.')
    def test_get_user_orders_with_auth_success(self, auth_user, orders_methods, ingredients_methods):
        """
        Тестирует успешное получение заказов конкретного пользователя.

        Шаги:
        1. Получает токен авторизации.
        2. Создает заказ.
        3. Получает номер заказа из ответа.
        4. Отправляет запрос на получение заказов пользователя.
        5. Проверяет, что код ответа равен 200.
        6. Проверяет, что номер созданного заказа присутствует в списке заказов.
        """
        token = auth_user.json()['accessToken']
        ingredients = ingredients_methods.get_ingredients()
        payload = {"ingredients": [ingredients.json()['data'][0]['_id']]}
        response_create_order = orders_methods.create_orders(payload, token)
        order_number = response_create_order.json()['order']['number']

        response_get_order = orders_methods.receiving_order(token)

        assert response_get_order.status_code == 200
        assert response_get_order.json()['orders'][0]['number'] == order_number

    @allure.title('Получение заказов неавторизованного пользователя')
    @allure.description('Получение списка заказов без авторизации, проверка кода ответа и текста ошибки')
    def test_get_user_orders_without_auth_fail(self, orders_methods):
        """
        Тестирует получение заказов неавторизованным пользователем.

        Шаги:
        1. Отправляет запрос на получение заказов без токена авторизации.
        2. Проверяет, что код ответа равен 401.
        3. Проверяет, что 'success' в ответе равно False.
        4. Проверяет, что в ответе содержится правильное сообщение об ошибке.
        """
        response = orders_methods.receiving_order()
        response_json = response.json()

        assert response.status_code == 401
        assert response_json["success"] is False
        assert response_json["message"] == LoginUserMessage.MESSAGE_USER_NOT_AUTH
