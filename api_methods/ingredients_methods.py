import requests
import allure


class IngredientsMethods:
    def __init__(self, url):
        self.url = url

    @allure.step('Получить список доступных ингредиентов')
    def get_ingredients(self):
        response = requests.get(f"{self.url}")
        return response