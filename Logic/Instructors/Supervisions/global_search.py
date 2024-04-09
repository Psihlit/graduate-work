from sqlalchemy import insert

from DB.databaseConnection import session
from DB.models import cosmonauts, supervisions


def global_search_users_by_lastname(surname: str):
    # Формирование запроса на основе введенного текста фамилии
    if surname:  # Если указан текст фамилии, выполняем поиск с частичным совпадением
        search_results = session.query(cosmonauts).filter(
            ~cosmonauts.c.ID.in_(session.query(supervisions.c.ID_cosmonaut)),
            cosmonauts.c.surname.like(f'%{surname}%')
        ).all()
    else:  # Если фамилия не указана, возвращаем всех космонавтов без кураторства
        search_results = session.query(cosmonauts).filter(
            ~cosmonauts.c.ID.in_(session.query(supervisions.c.ID_cosmonaut))
        ).all()

    result_list = []
    for element in search_results:
        element_list = [element.ID, element.surname, element.name, element.patronymic, element.email]
        result_list.append(element_list)

    return result_list


def add_supervision(cosmonaut_id: int, instructor_id: int):
    supervisions_data = {
        "ID_cosmonaut": cosmonaut_id,
        "ID_instructor": instructor_id
    }
    try:
        stmt = insert(supervisions).values(**supervisions_data)
        session.execute(stmt)
        session.commit()

    except Exception as e:
        # Обработка возможных ошибок
        session.rollback()  # Откатываем транзакцию
        raise e
    finally:
        session.close()  # Закрываем сессию
