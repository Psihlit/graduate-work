class UserIsExist(Exception):
    """Класс для ошибки - пользователь уже существует"""

    def __init__(self, message):
        super().__init__(message)
        self.message = message


class MyValidationError(Exception):
    """Класс для ошибки - ошибка валидации данных"""

    def __init__(self, message):
        super().__init__(message)
        self.message = message
