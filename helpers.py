"""Этот модуль предоставляет вспомогательные функции для тестов API."""
import random
import string


def register_new_user():
    """
    Генерирует нового пользователя со случайными данными.

    Эта функция создает нового пользователя со случайным адресом электронной почты, паролем и именем.
    Данные возвращаются в виде словаря (payload), который можно использовать в запросах к API.

    Возвращает:
        dict: Словарь, содержащий данные нового пользователя с ключами "email", "password" и "name".
    """

    def generate_random_string(length):
        """
        Генерирует случайную строку заданной длины.

        Аргументы:
            length (int): Длина генерируемой строки.

        Возвращает:
            str: Случайная строка из строчных букв.
        """
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    # Генерируем случайные данные для нового пользователя
    login = generate_random_string(8)
    domain = generate_random_string(5)
    email = f'{login}@{domain}.com'

    password = generate_random_string(10)
    name = generate_random_string(10)

    # Собираем тело запроса
    payload = {
        "email": email,
        "password": password,
        "name": name
    }
    return payload