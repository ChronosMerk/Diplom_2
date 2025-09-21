"""Этот модуль предоставляет класс для взаимодействия с API пользователя."""
import requests
import allure


class UserMethods:
    """Класс для представления методов взаимодействия с API пользователя."""

    def __init__(self, url):
        """
        Инициализирует класс UserMethods.

        Аргументы:
            url (str): Базовый URL для API пользователя.
        """
        self.url = url

    @allure.step('Отправка запроса на регистрацию')
    def registration_user(self, payload):
        """
        Регистрирует нового пользователя.

        Аргументы:
            payload (dict): Данные пользователя.

        Возвращает:
            requests.Response: Ответ от API.
        """
        response = requests.post(f'{self.url}/register', json=payload)
        return response

    @allure.step('Отправка запроса на авторизацию пользователя')
    def auth_user(self, payload):
        """
        Авторизует пользователя.

        Аргументы:
            payload (dict): Данные для входа.

        Возвращает:
            requests.Response: Ответ от API.
        """
        response = requests.post(f'{self.url}/login', json=payload)
        return response

    @allure.step('Отправка запроса на изменение данных пользователя')
    def update_user(self, payload, token=None):
        """
        Обновляет данные пользователя.

        Аргументы:
            payload (dict): Новые данные пользователя.
            token (str, optional): Токен авторизации. По умолчанию None.

        Возвращает:
            requests.Response: Ответ от API.
        """
        headers = {"Authorization": f"{token}"}
        response = requests.patch(f'{self.url}/user', json=payload, headers=headers)
        return response

    @allure.step('Отправка запроса на удаление пользователя')
    def delete_user(self, token):
        """
        Удаляет пользователя.

        Аргументы:
            token (str): Токен авторизации.

        Возвращает:
            requests.Response: Ответ от API.
        """
        headers = {"Authorization": f"{token}"}
        response = requests.delete(f'{self.url}/user', headers=headers)
        return response



