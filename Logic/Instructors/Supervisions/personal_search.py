from sqlalchemy import delete

from DB.databaseConnection import session
from DB.models import cosmonauts, supervisions


def instructor_search_users_by_lastname(instructor_id: int, surname: str):
    try:
        if surname:  # Если указан текст фамилии, выполняем поиск с частичным совпадением
            search_results = session.query(cosmonauts).join(
                supervisions, supervisions.c.ID_cosmonaut == cosmonauts.c.ID
            ).filter(
                supervisions.c.ID_instructor == instructor_id,
                cosmonauts.c.surname.like(f'%{surname}%')
            ).all()
        else:  # Если фамилия не указана, возвращаем всех космонавтов под кураторством указанного инструктора
            search_results = session.query(cosmonauts).join(
                supervisions, supervisions.c.ID_cosmonaut == cosmonauts.c.ID
            ).filter(
                supervisions.c.ID_instructor == instructor_id
            ).all()

        result_list = []
        for element in search_results:
            element_list = [element.ID, element.surname, element.name, element.patronymic, element.email]
            result_list.append(element_list)

        return result_list

    except Exception as e:
        # Обработка возможных ошибок
        session.rollback()  # Откатываем транзакцию
        raise e
    finally:
        session.close()  # Закрываем сессию


def delete_from_supervision(cosmonaut_id: int, instructor_id: int):
    try:
        stmt = delete(supervisions).where(
            (supervisions.c.ID_cosmonaut == cosmonaut_id) & (supervisions.c.ID_instructor == instructor_id))
        session.execute(stmt)
        session.commit()

    except Exception as e:
        # Обработка возможных ошибок
        session.rollback()  # Откатываем транзакцию
        raise e
    finally:
        session.close()  # Закрываем сессию
