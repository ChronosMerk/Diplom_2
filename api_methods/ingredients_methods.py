"""Этот модуль предоставляет класс для взаимодействия с API ингредиентов."""
import requests
import allure


class IngredientsMethods:
    """Класс для представления методов взаимодействия с API ингредиентов."""

    def __init__(self, url):
        """
        Инициализирует класс IngredientsMethods.

        Аргументы:
            url (str): Базовый URL для API ингредиентов.
        """
        self.url = url

    @allure.step('Получить список доступных ингредиентов')
    def get_ingredients(self):
        """
        Получает список доступных ингредиентов.

        Возвращает:
            requests.Response: Ответ от API.
        """
        response = requests.get(f"{self.url}")
        return response