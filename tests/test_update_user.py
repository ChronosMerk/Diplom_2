import allure
import pytest
from data.data_message import LoginUserMessage

@allure.title('Обновление поле email и name')
class TestUpdateUser:
    @allure.title('Позитивный тест на изменение данных')
    @pytest.mark.parametrize('input_value', ['email', 'name'])
    def test_update_user_success(self,input_value, auth_user, user_methods):
        allure.dynamic.description(f'Обновление поля {input_value} и получение статус кода 200')
        token = auth_user.json()["accessToken"]
        payload = auth_user.json()['user']
        low = 'Test' + payload[input_value]
        payload[input_value] = low.lower()

        response = user_methods.update_user(payload, token)

        assert response.status_code == 200
        assert response.json()['user'][input_value] == payload[input_value]

    @allure.title('Не авторизованный пользователь пытается обновить данные')
    @allure.description('Если не передать токен в запрос, будет ошибка "You should be authorised" и код ошибки 401')
    def test_update_user_not_token(self, auth_user, user_methods):
        payload = auth_user.json()['user']

        response = user_methods.update_user(payload)

        assert response.status_code == 401
        assert response.json()['message'] == LoginUserMessage.MESSAGE_USER_NOT_AUTH


