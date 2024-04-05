import re

from pydantic import BaseModel


# Определение модели данных для валидации
class RegistrationData(BaseModel):
    email: str
    password: str
    surname: str
    name: str
    patronymic: str
    date_of_birth: str
    passport_data: str
    citizenship: str
    marital_status: str
    registration_address: str
    residence_address: str
    nationality: str
    phone_number: str
    education: str
    work_experience: int


def validate_data(data: RegistrationData):
    errors = []

    if not check_email(data.email):
        errors.append("Почта не соответствует формату!")

    if not check_password(data.password):
        errors.append("Пароль не соответствует требованиям!")

    if not check_string_for_numbers(data.surname, 30):
        errors.append("Имя не соответствует требованиям!")

    if not check_string_for_numbers(data.name, 30):
        errors.append("Фамилия не соответствует требованиям!")

    if not check_patronymic(data.patronymic, 30):
        errors.append("Отчество не соответствует требованиям!")

    if not check_passport_data(data.passport_data, 10):
        errors.append("Паспортные данные не соответствует требованиям!")

    if not check_string_for_numbers(data.citizenship, 40):
        errors.append("Гражданство не соответствует требованиям!")

    if not check_string_for_numbers(data.registration_address, 100):
        errors.append("Место прописки не соответствует требованиям!")

    if not check_string_for_numbers(data.residence_address, 100):
        errors.append("Место проживания не соответствует требованиям!")

    if not check_string_for_numbers(data.nationality, 30):
        errors.append("Национальность не соответствует требованиям!")

    if not check_phone(data.phone_number):
        errors.append("Номер телефона не соответствует требованиям")

    if not check_string_for_numbers(data.education, 100):
        errors.append("Образование не соответствует требованиям!")

    if not check_integer(data.work_experience, 0, 100):
        errors.append("Стаж работы не соответствует требованиям")

    return errors


def check_integer(integer, minimum, maximum):
    if minimum <= integer <= maximum:
        return True


def check_password(password):
    # Проверка длины пароля
    if len(password) < 5:
        return False

    # Проверка наличия букв и цифр
    contains_letters = bool(re.search(r'[a-zA-Z]', password))
    contains_digits = bool(re.search(r'\d', password))

    # Пароль должен содержать и буквы, и цифры
    return contains_letters and contains_digits


def check_email(email):
    EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if re.match(EMAIL_REGEX, email):
        return True


def check_phone(phone_number):
    PHONE_REGEX = r'\+7\(\d{3}\)\d{3}-\d{2}-\d{2}'
    if re.match(PHONE_REGEX, phone_number):
        return True


def check_string_for_numbers(input_string, max_chars):
    # Проверка длины строки
    if len(input_string) > max_chars:
        # Проверка наличия цифр в строке
        if any(char.isdigit() for char in input_string):
            return False
    return True


def check_passport_data(passport_data, max_chars):
    # Проверка длины строки
    if len(passport_data) > max_chars:
        return False
    # Проверка наличия букв в строке
    if any(char.isalpha() for char in passport_data):
        return False
    return True


def check_patronymic(patronymic, max_chars):
    # Проверка длины строки
    if 0 < len(patronymic) <= max_chars:
        # Проверка наличия цифр в строке
        if any(char.isdigit() for char in patronymic):
            return False
    return True
