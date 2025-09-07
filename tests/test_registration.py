import allure
import pytest
import helpers
from data.data_message import RegistrationUserMessage

@allure.title('Тестирование регистрации уникального пользователя')
class TestRegistration:
    #создать уникального пользователя;
    #создать пользователя, который уже зарегистрирован;
    #создать пользователя и не заполнить одно из обязательных полей.
    @allure.title('Позитивная регистрация пользователя')
    @allure.description('Генерация данных для пользователя, отправка на регистрацию, получение 200 кода и успешное создание user')
    def test_registration_user_success(self, create_user):
        user = create_user()
        response = user["response"]
        payload = user["payload"]

        assert response.status_code == 200
        assert response.json()['user']['email'] == payload['email']
        assert 'Bearer' in response.json()['accessToken']

    @allure.title('Проверка на регистрацию уже существующего пользователя')
    @allure.description('Генерация данных для пользователя, отправка на регистрацию, получение 200 кода, после создание с такими же данными, получение кода 403 и message User already exists')
    def test_register_existing_user(self, create_user):
        first = create_user()
        second = create_user(**first["payload"])
        resp = second["response"]

        assert resp.status_code == 403
        assert resp.json()['message'] == RegistrationUserMessage.MESSAGE_REGISTER_EXISTING_USER

    @allure.description('Создание пользователя без заполнения полей и получение ответа "Email, password and name are required fields" и статус код 403')
    @pytest.mark.parametrize('input_value',['email','password','name'])
    def test_register_user_missing_required_field(self, input_value, user_methods):
        allure.dynamic.title(f'Проверка, что без поля {input_value} нельзя зарегистрировать')
        payload = helpers.register_new_user()
        payload[input_value] = ''

        response = user_methods.registration_user(payload)

        assert response.status_code == 403
        assert response.json()['message'] == RegistrationUserMessage.MESSAGE_REGISTRATION_WITHOUT_FILLING_IN_THE_FIELD