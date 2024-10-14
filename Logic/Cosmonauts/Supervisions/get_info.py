from sqlalchemy import select, join

from DB.databaseConnection import session
from DB.models import instructors, cosmonauts, supervisions


def get_info_about_supervision(email):
    try:
        # Строим запрос с использованием оператора JOIN
        query = select(instructors).select_from(
            join(cosmonauts, supervisions, cosmonauts.c.ID == supervisions.c.ID_cosmonaut).
            join(instructors, supervisions.c.ID_instructor == instructors.c.ID)
            ).where(cosmonauts.c.email == email)

        # Выполняем запрос и получаем результат
        search_results = session.execute(query).fetchone()

        result_list = [search_results[1], search_results[3], search_results[4], search_results[5]]

        return result_list

    except TypeError as e:
        raise e

    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
