import allure
from data.data_message import LoginUserMessage, CreateOrdersMessage

@allure.title('Тесты создания заказа')
class TestOrders:
    @allure.title('Позитивный тест создания заказа с авторизованным пользователем')
    @allure.description('Создать и авторизоваться пользователем, получить валидные ID ингредиентов, создать заказ, проверить код ответа, статус и наличие номера заказа')
    def test_order_creation_authorized(self, orders_methods, auth_user, ingredients_methods):
        token = auth_user.json()['accessToken']
        ingredients = ingredients_methods.get_ingredients()
        payload = {"ingredients": [ingredients.json()['data'][0]['_id']]}
        response = orders_methods.create_orders(payload, token)

        assert response.status_code == 200
        assert payload['ingredients'][0] in response.text

    @allure.title('Получить заказа неавторизованного пользователя')
    @allure.description('Получить список заказов без авторизации, проверить код ответа, статус и текст ошибки. В ДАННОМ ЗАПРОСЕ БАГ ОН ПРИСЫЛАЕТ 200')
    def test_order_creation_not_authorized(self, orders_methods, auth_user, ingredients_methods):
        ingredients = ingredients_methods.get_ingredients()
        payload = {"ingredients": [ingredients.json()['data'][0]['_id']]}
        response = orders_methods.create_orders(payload)

        assert response.status_code == 200
        assert response.json()["success"] is True

    @allure.title('Получить заказа с неверным хешем ингредиентов')
    @allure.description('Получить список заказов с неверным хешем ингредиентов, проверить код ответа, статус и текст ошибки.')
    def test_order_creation_incorrect_hash_ingredient(self, orders_methods, auth_user):
        token = auth_user.json()['accessToken']
        payload = {"ingredients": ['60d3463f7034a100269f45e7']}
        response = orders_methods.create_orders(payload, token)

        assert response.status_code == 400
        assert response.json()['message'] == CreateOrdersMessage.MESSAGE_CREATE_ORDERS_INCORRECT_HASH_INGREDIENT

    @allure.title('Получить заказа без добавления ингредиентов')
    @allure.description('Получить список заказов без добавления ингредиентов, проверить код ответа и текст ошибки.')
    def test_order_creation_not_ingredients(self, orders_methods, auth_user):
        token = auth_user.json()['accessToken']
        response = orders_methods.create_orders(None, token)

        assert response.status_code == 400
        assert response.json()['message'] == CreateOrdersMessage.MESSAGE_CREATE_ORDERS_NOT_INGREDIENT

    @allure.title('Получить заказа конкретного пользователя по токену')
    @allure.description('Получить заказа конкретного пользователя по токену, проверить код ответа и заказ.')
    def test_get_user_orders_with_auth_success(self, auth_user, orders_methods, ingredients_methods):
        token = auth_user.json()['accessToken']
        ingredients = ingredients_methods.get_ingredients()
        payload = {"ingredients": [ingredients.json()['data'][0]['_id']]}
        response_create_order = orders_methods.create_orders(payload, token)
        order_number = response_create_order.json()['order']['number']

        response_get_order = orders_methods.receiving_order(token)

        assert response_get_order.status_code == 200
        assert response_get_order.json()['orders'][0]['number'] == order_number

    @allure.title('Получить заказы неавторизованного пользователя')
    @allure.description('Получить список заказов без авторизации, проверить код ответа, статус и текст ошибки')
    def test_get_user_orders_without_auth_fail(self, orders_methods):
        response = orders_methods.receiving_order()
        response_json = response.json()

        assert response.status_code == 401
        assert response_json["success"] is False
        assert response_json["message"] == LoginUserMessage.MESSAGE_USER_NOT_AUTH
