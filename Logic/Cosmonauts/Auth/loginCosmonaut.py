from sqlalchemy import select

from DB.databaseConnection import session
from DB.models import cosmonauts

from Logic.Errors.Errors import UserIsNotExist, PasswordError

from globals import current_user


def login_cosmonaut(
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
        "education"
    ]

    global current_user

    try:
        # проверяем, что почта не используется среди космонавтов
        query = select(cosmonauts).where(cosmonauts.c.email == email)
        result = session.execute(query)
        cosmonaut = result.first()

        if not cosmonaut:
            raise UserIsNotExist("Пользователь с такой почтой не существует!")

        if cosmonaut[2] != password:
            raise PasswordError("Неверная почта или пароль!")

        current_user = dict(zip(keys, cosmonaut))

        return current_user

    except Exception as e:
        raise e
