from datetime import datetime

from pydantic import EmailStr, Field
from typing import Optional
from sqlalchemy import insert

from DB.databaseConnection import session
from DB.models import instructors


def register_instructor(
        email: EmailStr,
        password: Optional[str] = Field(default="12345", min_length=5, max_length=25),
        surname: Optional[str] = Field(max_length=50),
        name: Optional[str] = Field(max_length=50),
        patronymic: Optional[str] = Field(max_length=50),
        date_of_birth: Optional[datetime] = Field(default=datetime.utcnow),
        passport_data: Optional[str] = Field(default="0000000000", max_length=10),
        citizenship: Optional[str] = Field(default="Россия", max_length=30),
        marital_status: Optional[str] = Field(max_length=50),
        registration_address: Optional[str] = Field(max_length=50),
        residence_address: Optional[str] = Field(max_length=50),
        nationality: Optional[str] = Field(max_length=50),
        phone_number: Optional[str] = Field(max_length=15),
        education: Optional[str] = Field(max_length=50),
        work_experience: Optional[int] = Field(lt=100)
) -> None:
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
    :param work_experience: Стаж работы
    :return:
    """

    # Создание словаря и передача в него данных
    new_instructor = {"Почта": email,
                      "Пароль": password,
                      "Фамилия": surname,
                      "Имя": name,
                      "Отчество": patronymic,
                      "Дата рождения": date_of_birth,
                      "Паспортные данные": passport_data,
                      "Гражданство": citizenship,
                      "Семейное положение": marital_status,
                      "Место прописки": registration_address,
                      "Место проживания": residence_address,
                      "Национальность": nationality,
                      "Номер телефона": phone_number,
                      "Образование": education,
                      "Стаж работы": work_experience
                      }

    # запрос на добавление в базу данных, распаковка созданного словаря
    try:
        stmt = insert(instructors).values(**new_instructor)
        session.execute(stmt)
        session.commit()
        session.close()
    except Exception as e:
        print(e)
