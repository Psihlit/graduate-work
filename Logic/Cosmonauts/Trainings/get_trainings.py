from DB.databaseConnection import session
from DB.models import trainings


def get_trainings():
    search_results = session.query(trainings).all()

    result_list = []
    for element in search_results:
        element_list = [element.ID, element.train_name, element.description, element.duration]
        result_list.append(element_list)

    return result_list
