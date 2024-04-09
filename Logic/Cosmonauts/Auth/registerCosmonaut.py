from sqlalchemy import insert, select

from DB.databaseConnection import session
from DB.models import cosmonauts, instructors

from Logic.Errors.Errors import UserIsExist

from globals import current_user


def register_cosmonaut(
        email: str,
        password: str,
        surname: str,
        name: str,
        patronymic: str,
        date_of_birth: str,
        passport_data: str,
        citizenship: str,
        marital_status: str,
        registration_address: str,
        residence_address: str,
        nationality: str,
        phone_number: str,
        education: str
):
    """
    Функция для добавления данных о космонавте в базу данных
    :param email: Почта
    :param password: Пароль
    :param surname: Фамилия
    :param name: Имя
    :param patronymic: Отчество
    :param date_of_birth: Дата рождения
    :param passport_data: Паспортные данные
    :param citizenship: Гражданство
    :param marital_status: Семейное положение
    :param registration_address: Место прописки
    :param residence_address: Место проживания
    :param nationality: Национальность
    :param phone_number: Номер мобильного телефона
    :param education: Образование
    :return:
    """

    # Создание словаря и передача в него данных
    new_cosmonaut = {"email": email,
                     "password": password,
                     "surname": surname,
                     "name": name,
                     "patronymic": patronymic,
                     "date_of_birth": date_of_birth,
                     "passport_data": passport_data,
                     "citizenship": citizenship,
                     "marital_status": marital_status,
                     "registration_address": registration_address,
                     "residence_address": residence_address,
                     "nationality": nationality,
                     "phone_number": phone_number,
                     "education": education
                     }

    global current_user

    # запрос на добавление в базу данных, распаковка созданного словаря
    try:
        # проверяем, что почта не используется среди космонавтов
        query = select(cosmonauts).where(cosmonauts.c.email == email)
        result = session.execute(query)
        cosmonaut = result.first()

        if cosmonaut:
            raise UserIsExist("Пользователь с такой почтой уже существует!")

        # проверяем, что почта не используется среди инструкторов
        query = select(instructors).where(instructors.c.email == email)
        result = session.execute(query)
        instructor = result.first()

        if instructor:
            raise UserIsExist("Пользователь с такой почтой уже существует!")

        stmt = insert(cosmonauts).values(**new_cosmonaut)
        session.execute(stmt)
        session.commit()

        current_user = new_cosmonaut

        return current_user

    except Exception as e:
        # Обработка возможных ошибок
        session.rollback()  # Откатываем транзакцию
        raise e
    finally:
        session.close()  # Закрываем сессию
