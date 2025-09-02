import allure
import pytest
from data.data import URLS, AuthorizationUser
from data.data_message import LoginUserMessage


@allure.title('Тестирование входа пользователя')
class TestLoginUser:
    #логин под существующим пользователем,
    #логин с неверным логином и паролем.
    @allure.title('Позитивный тест входа пользователя')
    @allure.description('Вход пользователя, получение статус кода 200, получение токена Bearer')
    def test_login_existing_user_success(self, user_methods):
        payload = AuthorizationUser.JSON_USER
        response = user_methods.auth_user(payload)

        assert response.status_code == 200
        assert response.json()['user']['email'] == payload['email']
        assert 'Bearer' in response.json()['accessToken']

    @allure.description('Вход пользователя с неправильным полями, получение статус кода 401')
    @pytest.mark.parametrize('input_value', ['email','password'])
    def test_user_login_wrong_login_password(self, input_value, user_methods):
        allure.dynamic.title(f'Вход пользователя с неправильным {input_value}')
        payload = AuthorizationUser.JSON_USER
        payload[input_value] = "AHUESF@mail.com"

        response = user_methods.auth_user(payload)

        assert response.status_code == 401
        assert response.json()['message'] == LoginUserMessage.MESSAGE_USER_PASSWORD_OR_EMAIL_INCORRECT