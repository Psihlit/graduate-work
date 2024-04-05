from sqlalchemy import select

from DB.databaseConnection import session
from DB.models import instructors

from Logic.Errors.Errors import UserIsNotExist, PasswordError

from globals import current_user


def login_instructor(
        email: str,
        password: str
):
    """
    Функция для добавления данных о космонавте в базу данных
    :param email: Почта
    :param password: Пароль
    :return:
    """

    keys = [
        "id",
        "email",
        "password",
        "surname",
        "name",
        "patronymic",
        "date_of_birth",
        "passport_data",
        "citizenship",
        "marital_status",
        "registration_address",
        "residence_address",
        "nationality",
        "phone_number",
        "education",
        "work_experience"
    ]

    global current_user

    try:
        # проверяем, что почта не используется среди космонавтов
        query = select(instructors).where(instructors.c.email == email)
        result = session.execute(query)
        instructor = result.first()

        if not instructor:
            raise UserIsNotExist("Пользователь с такой почтой не существует!")

        if instructor[2] != password:
            raise PasswordError("Неверная почта или пароль!")

        current_user = dict(zip(keys, instructor))

        return current_user

    except Exception as e:
        raise e
