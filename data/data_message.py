class RegistrationUserMessage:
    MESSAGE_REGISTER_EXISTING_USER = 'User already exists'
    MESSAGE_REGISTRATION_WITHOUT_FILLING_IN_THE_FIELD = 'Email, password and name are required fields'

class LoginUserMessage:
    MESSAGE_USER_PASSWORD_OR_EMAIL_INCORRECT = 'email or password are incorrect'
    MESSAGE_USER_NOT_AUTH = 'You should be authorised'

class CreateOrdersMessage:
    MESSAGE_CREATE_ORDERS_INCORRECT_HASH_INGREDIENT = 'One or more ids provided are incorrect'
    MESSAGE_CREATE_ORDERS_NOT_INGREDIENT = 'Ingredient ids must be provided'
