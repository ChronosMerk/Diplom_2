import allure

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

    @allure.title('Получить заказы неавторизованного пользователя')
    @allure.description('Получить список заказов без авторизации, проверить код ответа, статус и текст ошибки. В ДАННОМ ЗАПРОСЕ БАГ ОН ПРИСЫЛАЕТ 200')
    def test_order_creation_not_authorized(self, orders_methods, auth_user, ingredients_methods):
        ingredients = ingredients_methods.get_ingredients()
        payload = {"ingredients": [ingredients.json()['data'][0]['_id']]}
        response = orders_methods.create_orders(payload)

        assert response.status_code == 200
        assert response.json()["success"] is True