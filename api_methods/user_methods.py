import requests
import allure

class UserMethods:
    def __init__(self, url):
        self.url = url

    @allure.step('Отправка запроса на регистрацию')
    def registration_user(self, payload):
        response = requests.post(f'{self.url}/register', json=payload)
        return response

    @allure.step('Отправка запроса на авторизацию пользователя')
    def auth_user(self, payload):
        response = requests.post(f'{self.url}/login', json=payload)
        return response

    @allure.step('Отправка запроса на Изменение данных пользователя')
    def update_user(self, payload, token=None):
        headers = {"Authorization": f"{token}"}
        response = requests.patch(f'{self.url}/user', json=payload, headers=headers)
        return response

    @allure.step('Отправка запроса на удаление пользователя')
    def delete_user(self, token):
        headers = {"Authorization": f"{token}"}
        response = requests.delete(f'{self.url}/user', headers=headers)
        return response



