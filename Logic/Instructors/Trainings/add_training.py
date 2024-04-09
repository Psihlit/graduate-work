from sqlalchemy import select, desc, insert

from DB.databaseConnection import session
from DB.models import input_data, trainings


def get_input_data_by_ID(ID):
    try:
        query = select(input_data).where(input_data.c.ID == ID)
        record = session.execute(query)
        result = record.first()

        return result

    except Exception as e:
        raise e


def get_last_input_data():
    try:
        query = select(input_data).order_by(desc(input_data.c.ID))
        last_record = session.execute(query)
        result = last_record.first()

        return result

    except Exception as e:
        raise e


def add_training(training_data):
    try:
        stmt = insert(trainings).values(**training_data)
        session.execute(stmt)
        session.commit()

    except Exception as e:
        # Обработка возможных ошибок
        session.rollback()  # Откатываем транзакцию
        raise e
    finally:
        session.close()  # Закрываем сессию
