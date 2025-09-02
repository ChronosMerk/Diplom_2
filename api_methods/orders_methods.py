import requests
import allure

class OrdersMethods:
    def __init__(self, url):
        self.url = url

    @allure.step('Создание заказа')
    def create_orders(self, payload, token=None):
        headers = {"Authorization": f"{token}"}
        response = requests.post(self.url, json=payload, headers=headers)
        return response
