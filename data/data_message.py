"""Этот модуль содержит сообщения для тестов API."""


class RegistrationUserMessage:
    """Этот класс содержит сообщения, связанные с регистрацией пользователя."""
    MESSAGE_REGISTER_EXISTING_USER = 'User already exists'
    MESSAGE_REGISTRATION_WITHOUT_FILLING_IN_THE_FIELD = 'Email, password and name are required fields'


class LoginUserMessage:
    """Этот класс содержит сообщения, связанные с входом пользователя в систему."""
    MESSAGE_USER_PASSWORD_OR_EMAIL_INCORRECT = 'email or password are incorrect'
    MESSAGE_USER_NOT_AUTH = 'You should be authorised'


class CreateOrdersMessage:
    """Этот класс содержит сообщения, связанные с созданием заказов."""
    MESSAGE_CREATE_ORDERS_INCORRECT_HASH_INGREDIENT = 'One or more ids provided are incorrect'
    MESSAGE_CREATE_ORDERS_NOT_INGREDIENT = 'Ingredient ids must be provided'
