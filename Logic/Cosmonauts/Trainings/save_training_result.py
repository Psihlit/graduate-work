from sqlalchemy import select, insert

from DB.databaseConnection import session
from DB.models import supervisions, results


def save_training_result(result_data, current_time, maximum_time, current_user, current_train):

    id_cosmonauts = current_user['id']
    id_training = current_train[0]

    results_list, comments = [], []
    mistake_count = 0
    if int(current_time[3:5]) >= int(maximum_time):
        comments.append("Вы не уложились в сроки норматива!")
        results_list.append(2)
    else:
        for i in range(1, 4):
            if f"ЦВ{i}: Прокрутка выполнена НЕ безопасно" in result_data:
                mistake_count += 1
                comments.append(
                    f"Прокрутка крыльчатки ЦВ{i} выполнена не безопасно - вентилятор не был отключен для безопасных действий.")
            if f"ЦВ{i}: Замена выполнена НЕ безопасно" in result_data:
                mistake_count += 1
                comments.append(
                    f"Замена вентилятора ЦВ{i} выполнена не безопасно - вентилятор не был отключен для безопасных действий.")
            if f"ЦВ{i}: Перед повторным запуском НЕ прошло 30 секунд" in result_data:
                mistake_count += 1
                comments.append(
                    f"Перед повторным запуском ЦВ{i} не прошло минимально допустимое время - 30 секунд.")
        if mistake_count <= 1:
            results_list.append(5)
        if 1 < mistake_count <= 3:
            results_list.append(4)
        if 3 < mistake_count <= 5:
            results_list.append(3)
        if 5 < mistake_count:
            results_list.append(2)

    if len(comments) > 0:
        result_comments = " ".join(comments)
    else:
        result_comments = "-"

    print(result_comments)
    print(results_list)

    try:
        # Создаем запрос
        query = select(supervisions.c.ID_instructor).where(supervisions.c.ID_cosmonaut == id_cosmonauts)

        # Выполняем запрос
        result = session.execute(query).fetchone()

        if result:
            id_instructor = result[0]
        else:
            return None
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

    # Создание словаря и передача в него данных
    new_result = {"ID_cosmonaut": id_cosmonauts,
                  "ID_instructor": id_instructor,
                  "ID_training": id_training,
                  "results": results_list[0],
                  "comments": result_comments
                  }

    try:
        stmt = insert(results).values(**new_result)
        session.execute(stmt)
        session.commit()

        return "Запись сохранена"

    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
