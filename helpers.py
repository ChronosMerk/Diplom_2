import random
import string

# метод регистрации нового курьера возвращает список из логина и пароля
def register_new_user():
    # метод генерирует строку, состоящую только из букв нижнего регистра, в качестве параметра передаём длину строки
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    login = generate_random_string(8)
    domain = generate_random_string(5)
    email = f'{login}@{domain}.com'

    password = generate_random_string(10)
    name = generate_random_string(10)

    # собираем тело запроса
    payload = {
        "email": email,
        "password": password,
        "name": name
    }
    return payload