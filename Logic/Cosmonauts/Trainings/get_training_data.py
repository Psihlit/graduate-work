from sqlalchemy import select

from DB.databaseConnection import session
from DB.models import input_data, trainings


def get_training_data(training_id):
    try:
        # Создаем запрос
        query = select(input_data).select_from(trainings.join(input_data)).where(trainings.c.ID == training_id)

        # Выполняем запрос
        result = session.execute(query).fetchone()

        return result
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()