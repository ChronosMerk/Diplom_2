"""Этот модуль предоставляет класс для взаимодействия с API заказов."""
import requests
import allure


class OrdersMethods:
    """Класс для представления методов взаимодействия с API заказов."""

    def __init__(self, url):
        """
        Инициализирует класс OrdersMethods.

        Аргументы:
            url (str): Базовый URL для API заказов.
        """
        self.url = url

    @allure.step('Создание заказа')
    def create_orders(self, payload=None, token=None):
        """
        Создает новый заказ.

        Аргументы:
            payload (dict, optional): Данные заказа. По умолчанию None.
            token (str, optional): Токен авторизации. По умолчанию None.

        Возвращает:
            requests.Response: Ответ от API.
        """
        headers = {"Authorization": f"{token}"}
        response = requests.post(self.url, json=payload, headers=headers)
        return response

    @allure.step('Получение заказа пользователя')
    def receiving_order(self, token=None):
        """
        Получает заказ пользователя.

        Аргументы:
            token (str, optional): Токен авторизации. По умолчанию None.

        Возвращает:
            requests.Response: Ответ от API.
        """
        headers = {"Authorization": f"{token}"}
        response = requests.get(self.url, headers=headers)
        return response