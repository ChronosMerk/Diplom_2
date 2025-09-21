"""Этот модуль содержит тесты для входа пользователя в систему."""
import allure
import pytest
from data.data import AuthorizationUser
from data.data_message import LoginUserMessage


@allure.title('Тестирование входа пользователя')
class TestLoginUser:
    """
    Этот класс содержит тесты для входа пользователя в систему.
    - Логин под существующим пользователем.
    - Логин с неверным логином и паролем.
    """
    @allure.title('Позитивный тест входа пользователя')
    @allure.description('Вход пользователя, получение статус кода 200, получение токена Bearer')
    def test_login_existing_user_success(self, user_methods):
        """
        Тестирует успешный вход существующего пользователя.

        Шаги:
        1. Отправляет запрос на авторизацию с корректными данными.
        2. Проверяет, что код ответа равен 200.
        3. Проверяет, что в ответе содержится email пользователя.
        4. Проверяет, что в ответе содержится токен доступа.
        """
        payload = AuthorizationUser.JSON_USER
        response = user_methods.auth_user(payload)

        assert response.status_code == 200
        assert response.json()['user']['email'] == payload['email']
        assert 'Bearer' in response.json()['accessToken']

    @allure.description('Вход пользователя с неправильным полями, получение статус кода 401')
    @pytest.mark.parametrize('input_value', ['email', 'password'])
    def test_user_login_wrong_login_password(self, input_value, user_methods):
        """
        Тестирует вход пользователя с неверным логином или паролем.

        Шаги:
        1. Изменяет email или пароль на неверный.
        2. Отправляет запрос на авторизацию.
        3. Проверяет, что код ответа равен 401.
        4. Проверяет, что в ответе содержится правильное сообщение об ошибке.
        """
        allure.dynamic.title(f'Вход пользователя с неправильным {input_value}')
        payload = AuthorizationUser.JSON_USER.copy()
        payload[input_value] = "AHUESF@mail.com"

        response = user_methods.auth_user(payload)

        assert response.status_code == 401
        assert response.json()['message'] == LoginUserMessage.MESSAGE_USER_PASSWORD_OR_EMAIL_INCORRECT