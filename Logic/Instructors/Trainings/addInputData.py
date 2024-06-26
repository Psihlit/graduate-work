from sqlalchemy import insert, select

from DB.databaseConnection import session
from DB.models import input_data


def add_input_data(inputData):
    try:
        stmt = insert(input_data).values(**inputData)
        session.execute(stmt)
        session.commit()

    except Exception as e:
        # Обработка возможных ошибок
        session.rollback()  # Откатываем транзакцию
        raise e
    finally:
        session.close()  # Закрываем сессию


def get_elements_by_ID_instructor(ID_instructor):
    try:
        query = select(input_data).where(input_data.c.ID_instructor == ID_instructor)
        result = session.execute(query)
        data = result.all()

        return data

    except Exception as e:
        raise e
