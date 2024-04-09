from PyQt6 import QtCore
from PyQt6.QtWidgets import QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QCheckBox, QMessageBox, \
    QTabWidget, QComboBox, QHBoxLayout, QTableWidget, QTableWidgetItem

from Logic.Cosmonauts.Auth.loginCosmonaut import login_cosmonaut
from Logic.Cosmonauts.Auth.registerCosmonaut import register_cosmonaut
from Logic.Cosmonauts.Supervisions.get_info import get_info_about_supervision
from Logic.Errors.Errors import UserIsExist, MyValidationError
from Logic.Instructors.Auth.loginInstructor import login_instructor
from Logic.Instructors.Auth.registerInstructor import register_instructor
from Logic.Instructors.Supervisions.global_search import global_search_users_by_lastname, add_supervision
from Logic.Instructors.Supervisions.personal_search import delete_from_supervision, instructor_search_users_by_lastname
from Logic.Instructors.Trainings.addInputData import add_input_data, get_elements_by_ID_instructor
from Logic.Instructors.Trainings.add_training import get_last_input_data, add_training, get_input_data_by_ID
from UI.AuthData import AuthData
from UI.RegistrationValidation import RegistrationData, validate_data
from style import BUTTON_STYLE

from config import START_LOGIN_X, START_LOGIN_Y, LOGIN_X, LOGIN_Y, START_MAIN_X, START_MAIN_Y, MAIN_X, MAIN_Y


class LoginWindow(QMainWindow):
    """
    Класс, отвечающий за окно авторизации
    """

    def __init__(self, current_user):
        super().__init__()

        # region Настройка виджетов окна авторизации
        self.setWindowTitle("Авторизация")
        self.setGeometry(START_LOGIN_X, START_LOGIN_Y, LOGIN_X, LOGIN_Y)
        self.current_user = current_user

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()

        self.window_label = QLabel("Авторизация")
        self.window_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.window_label)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Почта")
        self.email_input.setText("user@mail.com")  # по умолчанию
        layout.addWidget(self.email_input)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setText("qwerty123")  # по умолчанию
        layout.addWidget(self.password_input)

        self.role_checkbox = QCheckBox("Инструктор")
        layout.addWidget(self.role_checkbox)

        self.login_button = QPushButton("Авторизация")
        self.login_button.setStyleSheet(BUTTON_STYLE)
        self.login_button.clicked.connect(self.login_button_clicked)
        layout.addWidget(self.login_button)

        self.registration_button = QPushButton("Зарегистрироваться")
        layout.addWidget(self.registration_button)

        # Установим обработчик для кнопки регистрации
        self.registration_button.clicked.connect(self.open_registration_window)

        self.central_widget.setLayout(layout)

        # endregion

    def open_registration_window(self, current_user):
        """
        Функция открытия окна регистрации
        :param current_user:
        :return:
        """
        self.registration_window = RegistrationWindow(current_user)
        self.registration_window.show()
        self.close()

    def open_main_window(self, current_user):
        """Функция открытия главного окна"""
        self.main_window = MainWindow(current_user)
        self.main_window.show()
        self.close()

    def login_button_clicked(self):
        """
        Функция обработчик для кнопки авторизации
        :return:
        """
        # Получение данных из полей ввода
        data = AuthData(
            email=self.email_input.text(),
            password=self.password_input.text()
        )

        # region Инструктор
        if self.role_checkbox.isChecked():
            try:
                data = data.dict()  # Преобразование данных обратно в словарь для использования в регистрации
                current_user = login_instructor(**data)
                # QMessageBox.information(self, "Успех", "Авторизация прошла успешно!")
                self.open_main_window(current_user)

            except UserIsExist as e:
                QMessageBox.warning(self, "Ошибка", str(e))

            except Exception as e:
                QMessageBox.critical(self, "Critical Error", str(e))
                print(f"Ошибка при авторизации инструктора: {str(e)}")
        # endregion

        # region Космонавт
        else:

            try:
                data = data.dict()  # Преобразование данных обратно в словарь для использования в регистрации
                current_user = login_cosmonaut(**data)  # получение данных о текущем пользователе
                # QMessageBox.information(self, "Успех", "Авторизация прошла успешно!")
                self.open_main_window(current_user)

            except UserIsExist as e:
                QMessageBox.warning(self, "Ошибка", str(e))

            except Exception as e:
                QMessageBox.critical(self, "Critical Error", str(e))
                print(f"Ошибка при авторизации космонавта: {str(e)}")
        # endregion


class RegistrationWindow(QMainWindow):
    """
    Класс, отвечающий за окно регистрации
    """

    # region Настройка виджетов окна регистрации
    def __init__(self, current_user):
        super().__init__()

        self.setWindowTitle("Регистрация")
        self.setGeometry(START_LOGIN_X, START_LOGIN_Y, LOGIN_X, LOGIN_Y)
        self.current_user = current_user

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()

        self.window_label = QLabel("Регистрация")
        self.window_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.window_label)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Почта")
        layout.addWidget(self.email_input)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Пароль")
        layout.addWidget(self.password_input)

        self.surname_input = QLineEdit()
        self.surname_input.setPlaceholderText("Фамилия")
        layout.addWidget(self.surname_input)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Имя")
        layout.addWidget(self.name_input)

        self.patronymic_input = QLineEdit()
        self.patronymic_input.setPlaceholderText("Отчество")
        layout.addWidget(self.patronymic_input)

        # Выбрать календарик
        self.date_of_birth_input = QLineEdit()
        self.date_of_birth_input.setPlaceholderText("Дата рождения")
        layout.addWidget(self.date_of_birth_input)

        self.passport_data_input = QLineEdit()
        self.passport_data_input.setPlaceholderText("Паспортные данные")
        layout.addWidget(self.passport_data_input)

        self.citizenship_input = QLineEdit()
        self.citizenship_input.setPlaceholderText("Гражданство")
        layout.addWidget(self.citizenship_input)

        # Выбрать выпадающее окошко
        self.marital_status_input = QLineEdit()
        self.marital_status_input.setPlaceholderText("Семейное положение")
        layout.addWidget(self.marital_status_input)

        self.registration_address_input = QLineEdit()
        self.registration_address_input.setPlaceholderText("Место прописки")
        layout.addWidget(self.registration_address_input)

        self.residence_address_input = QLineEdit()
        self.residence_address_input.setPlaceholderText("Место проживания")
        layout.addWidget(self.residence_address_input)

        self.nationality_input = QLineEdit()
        self.nationality_input.setPlaceholderText("Национальность")
        layout.addWidget(self.nationality_input)

        self.phone_number_input = QLineEdit()
        self.phone_number_input.setPlaceholderText("Номер телефона")
        layout.addWidget(self.phone_number_input)

        self.education_input = QLineEdit()
        self.education_input.setPlaceholderText("Образование")
        layout.addWidget(self.education_input)

        self.role_checkbox = QCheckBox("Инструктор")
        self.role_checkbox.stateChanged.connect(self.toggle_role_checkbox)
        layout.addWidget(self.role_checkbox)

        self.work_experience_input = QLineEdit()
        self.work_experience_input.setPlaceholderText("Стаж работы")
        self.work_experience_input.setVisible(False)
        layout.addWidget(self.work_experience_input)

        self.registration_button = QPushButton("Зарегистрироваться")
        self.registration_button.clicked.connect(self.register_button_clicked)
        layout.addWidget(self.registration_button)

        self.back_to_login_button = QPushButton("Уже зарегистрированы?")
        layout.addWidget(self.back_to_login_button)

        # Установим обработчик для кнопки возврата к авторизации
        self.back_to_login_button.clicked.connect(self.open_login_window)

        self.central_widget.setLayout(layout)

    # endregion

    def open_login_window(self, current_user):
        """
        Функция для открытия окна авторизации
        :param current_user:
        :return:
        """
        self.login_window = LoginWindow(current_user)
        self.login_window.show()
        self.close()

    def open_main_window(self, current_user):
        """
        Функция для перехода на главную страницу
        :param current_user:
        :return:
        """
        self.main_window = MainWindow(current_user)
        self.main_window.show()
        self.close()

    def toggle_role_checkbox(self, state):
        """
        Функция для проверки, в каком положении находится checkBox
        :param state:
        :return:
        """
        if state == 2:  # 2 соответствует состоянию "нажат"
            self.work_experience_input.setVisible(True)
        else:
            self.work_experience_input.setVisible(False)

    def register_button_clicked(self):
        """Функция-обработчик для нажатия кнопки регистрации"""

        # region Получение данных и верификация
        try:
            # Получение данных из полей ввода
            data = RegistrationData(
                email=self.email_input.text(),
                password=self.password_input.text(),
                surname=self.surname_input.text(),
                name=self.name_input.text(),
                patronymic=self.patronymic_input.text(),
                date_of_birth=self.date_of_birth_input.text(),
                passport_data=self.passport_data_input.text(),
                citizenship=self.citizenship_input.text(),
                marital_status=self.marital_status_input.text(),
                registration_address=self.registration_address_input.text(),
                residence_address=self.residence_address_input.text(),
                nationality=self.nationality_input.text(),
                phone_number=self.phone_number_input.text(),
                education=self.education_input.text(),
                work_experience=int(
                    self.work_experience_input.text()) if self.work_experience_input.isVisible() else 0
            )

            errors = validate_data(data)
            if len(errors) > 0:
                message = '\n'.join(errors)
                raise MyValidationError(message)

        except MyValidationError as e:
            QMessageBox.warning(self, "Ошибка заполнения данных!", str(e))
            return

        # endregion

        # region Инструктор
        if self.role_checkbox.isChecked():
            try:
                # Отображение сообщения об ошибке, если данные не прошли валидацию
                data = data.dict()  # Преобразование данных обратно в словарь для использования в регистрации
                current_user = register_instructor(**data)
                QMessageBox.information(self, "Успех", "Регистрация прошла успешно!")
                self.open_main_window(current_user)

            except UserIsExist as e:
                QMessageBox.warning(self, "Ошибка", str(e))

            except Exception as e:
                QMessageBox.critical(self, "Critical Error", str(e))
                print(f"Ошибка при добавлении регистрации инструктора: {str(e)}")
        # endregion

        # region Космонавт
        else:

            try:
                # Отображение сообщения об ошибке, если данные не прошли валидацию
                data = data.dict()  # Преобразование данных обратно в словарь для использования в регистрации
                del data['work_experience']
                current_user = register_cosmonaut(**data)
                # QMessageBox.information(self, "Успех", "Регистрация прошла успешно!")
                self.open_main_window(current_user)

            except UserIsExist as e:
                QMessageBox.warning(self, "Ошибка", str(e))

            except Exception as e:
                QMessageBox.critical(self, "Critical Error", str(e))
                print(f"Ошибка при регистрации космонавта: {str(e)}, {e}")
        # endregion


class MainWindow(QMainWindow):
    # region Настройка виджетов главного окна
    def __init__(self, current_user):
        super().__init__()
        self.setWindowTitle("Главное окно")
        self.setGeometry(START_MAIN_X, START_MAIN_Y, MAIN_X, MAIN_Y)
        self.current_user = current_user

        # Создаем виджет вкладок
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        # Создаем вкладки и добавляем их в виджет вкладок
        self.training_tab = QWidget()
        self.personal_page_tab = QWidget()
        self.supervision_tab = QTabWidget()

        self.tab_widget.addTab(self.training_tab, "Выбор тренировки")
        self.tab_widget.addTab(self.personal_page_tab, "Личная страница")
        self.tab_widget.addTab(self.supervision_tab, "Кураторство")

        # region Выбор тренировки
        # Вкладка "Выбор тренировки"
        training_layout = QVBoxLayout()
        self.training_tab.setLayout(training_layout)
        # endregion

        # region Личная страница
        # Вкладка "Личная страница"
        personal_layout = QVBoxLayout()
        self.personal_page_tab.setLayout(personal_layout)

        # Добавление полей из регистрации космонавта
        fields = ["Почта", "Фамилия", "Имя", "Отчество", "Дата рождения",
                  "Паспортные данные", "Гражданство", "Семейный статус", "Место прописки",
                  "Место проживания", "Национальность", "Номер телефона",
                  "Образование"]

        dict_keys = ["email", "surname", "name", "patronymic", "date_of_birth", "passport_data",
                     "citizenship", "marital_status", "registration_address", "residence_address", "nationality",
                     "phone_number", "education"]

        i = 0
        for field in fields:
            label = QLabel(field + ":")
            personal_layout.addWidget(label)
            # Проверяем наличие данных о пользователе и выводим их
            if self.current_user:
                label_value = QLabel(str(self.current_user.get(dict_keys[i], "")))
                personal_layout.addWidget(label_value)
                i += 1

        # Добавление поля "Стаж работы", если длина списка current_user равна 16
        if self.is_instructor():
            work_experience_label = QLabel("Стаж работы:")
            personal_layout.addWidget(work_experience_label)
            if self.current_user:
                work_experience_value = QLabel(str(self.current_user.get("work_experience", "")))
                personal_layout.addWidget(work_experience_value)

        logout_button = QPushButton("Выйти из учетной записи")
        personal_layout.addWidget(logout_button)
        logout_button.clicked.connect(self.logout)
        # endregion

        # region Кураторство

        # для инструктора
        if self.is_instructor():
            # region Поиск
            # Вкладка "Поиск"
            self.global_search_tab = QWidget()
            self.global_search_layout = QVBoxLayout()
            self.global_search_tab.setLayout(self.global_search_layout)

            self.global_horizontal_layout = QHBoxLayout()

            # Добавляем виджеты в горизонтальный контейнер
            self.global_horizontal_layout.addWidget(QLabel("Поле поиска:"))
            self.global_search_edit = QLineEdit()
            self.global_horizontal_layout.addWidget(self.global_search_edit)

            self.global_search_button = QPushButton("Поиск")
            self.global_horizontal_layout.addWidget(self.global_search_button)
            self.global_search_button.clicked.connect(self.global_search_button_clicked)

            # Добавляем кнопку "Очистить"
            self.global_clear_button = QPushButton("Очистить")
            self.global_horizontal_layout.addWidget(self.global_clear_button)
            self.global_clear_button.clicked.connect(self.global_clear_search_field)

            # Устанавливаем созданный горизонтальный контейнер в качестве макета для виджета self.search_tab
            self.global_search_layout.addLayout(self.global_horizontal_layout)

            self.global_search_results_table = QTableWidget()
            self.global_search_results_table.setColumnCount(5)
            self.global_search_results_table.setHorizontalHeaderLabels(["Фамилия", "Имя", "Отчество", "Почта", ""])
            self.global_search_layout.addWidget(self.global_search_results_table)
            self.global_fill_possible_supervision_table()

            self.supervision_tab.addTab(self.global_search_tab, "Поиск")
            self.supervision_tab.currentChanged.connect(self.global_update_search_tab)

            # endregion

            # region Мое кураторство

            # Вкладка "Мое кураторство"
            self.instructor_supervision_tab = QWidget()
            self.instructor_supervision_layout = QVBoxLayout()
            self.instructor_supervision_tab.setLayout(self.instructor_supervision_layout)

            # Создаем горизонтальный контейнер для строки с полем ввода и кнопками
            self.instructor_horizontal_layout = QHBoxLayout()

            # Добавляем виджеты в горизонтальный контейнер
            self.instructor_horizontal_layout.addWidget(QLabel("Поле поиска:"))
            self.instructor_search_edit = QLineEdit()
            self.instructor_horizontal_layout.addWidget(self.instructor_search_edit)

            self.instructor_search_button = QPushButton("Поиск")
            self.instructor_horizontal_layout.addWidget(self.instructor_search_button)
            self.instructor_search_button.clicked.connect(self.instructor_search_button_clicked)

            # Добавляем кнопку "Очистить"
            self.instructor_clear_button = QPushButton("Очистить")
            self.instructor_horizontal_layout.addWidget(self.instructor_clear_button)
            self.instructor_clear_button.clicked.connect(self.instructor_clear_search_field)

            # Устанавливаем созданный горизонтальный контейнер в качестве макета для виджета self.search_tab
            self.instructor_supervision_layout.addLayout(self.instructor_horizontal_layout)

            # Добавление таблицы с данными кураторства
            self.instructor_search_results_table = QTableWidget()
            self.instructor_search_results_table.setColumnCount(5)  # Установите количество столбцов
            self.instructor_search_results_table.setHorizontalHeaderLabels(["Фамилия", "Имя", "Отчество", "Почта", ""])
            self.instructor_supervision_layout.addWidget(self.instructor_search_results_table)
            self.instructor_fill_possible_supervision_table()

            # Добавление кнопки "Удалить" к таблице
            self.instructor_delete_button = QPushButton("Удалить")
            self.instructor_supervision_layout.addWidget(self.instructor_delete_button)
            self.instructor_delete_button.clicked.connect(
                self.delete_from_supervision)  # Подключение обработчика нажатия кнопки "Удалить"

            # Добавляем вкладку "Мое кураторство" в виджет вкладок
            self.supervision_tab.addTab(self.instructor_supervision_tab, "Мое кураторство")
            self.supervision_tab.currentChanged.connect(self.update_instructor_supervision_tab)

            # endregion

        # для космонавта
        else:
            # region Кураторство есть
            try:
                self.cosmonaut_supervision_layout = QVBoxLayout()
                self.supervision_tab.setLayout(self.cosmonaut_supervision_layout)

                cosmonaut_supervision_fields = ["Почта", "Фамилия", "Имя", "Отчество"]

                instructor_info = get_info_about_supervision(self.current_user.get("email", ""))

                if len(instructor_info) > 0:
                    i = 0
                    for field in cosmonaut_supervision_fields:
                        label = QLabel(field + ":")
                        self.cosmonaut_supervision_layout.addWidget(label)
                        label_value = QLabel(str(instructor_info[i]))
                        self.cosmonaut_supervision_layout.addWidget(label_value)
                        i += 1
            # endregion

            # region Кураторства нет
            except TypeError as e:
                label = QLabel("У вас отсутствует куратор")
                self.cosmonaut_supervision_layout.addWidget(label)
            # endregion

        # endregion

        # region Добавление тренировки (только Инструктор)
        if self.is_instructor():
            self.create_training_tab = QWidget()
            self.tab_widget.addTab(self.create_training_tab, "Добавление тренировки")

            # Добавляем виджеты на вкладку "Создание тренировки"
            self.create_training_layout = QVBoxLayout()
            self.create_training_tab.setLayout(self.create_training_layout)

            self.training_name_label = QLabel("Название тренировки:")
            self.create_training_layout.addWidget(self.training_name_label)
            self.training_name_input = QLineEdit()
            self.create_training_layout.addWidget(self.training_name_input)

            self.training_description_label = QLabel("Описание тренировки:")
            self.create_training_layout.addWidget(self.training_description_label)
            self.training_description_input = QLineEdit()
            self.create_training_layout.addWidget(self.training_description_input)

            self.training_duration_label = QLabel("Продолжительность:")
            self.create_training_layout.addWidget(self.training_duration_label)
            self.training_duration_input = QLineEdit()
            self.create_training_layout.addWidget(self.training_duration_input)

            # region Добавление входных данных

            self.input_data_label = QLabel("Входные данные:")
            self.create_training_layout.addWidget(self.input_data_label)

            # Выпадающее окно с выбором данных из БД
            self.input_data_combobox = QComboBox()
            self.update_input_data_combobox()
            # Добавьте элементы из базы данных сюда
            self.create_training_layout.addWidget(self.input_data_combobox)

            # Обработчик события изменения значения в выпадающем списке
            self.input_data_combobox.currentIndexChanged.connect(self.update_fields)

            self.parameter_a_label = QLabel("Параметр А:")
            self.create_training_layout.addWidget(self.parameter_a_label)
            self.parameter_a_input = QLineEdit()
            self.create_training_layout.addWidget(self.parameter_a_input)

            self.parameter_b_label = QLabel("Параметр Б:")
            self.create_training_layout.addWidget(self.parameter_b_label)
            self.parameter_b_input = QLineEdit()
            self.create_training_layout.addWidget(self.parameter_b_input)

            self.parameter_c_label = QLabel("Параметр В:")
            self.create_training_layout.addWidget(self.parameter_c_label)
            self.parameter_c_input = QLineEdit()
            self.create_training_layout.addWidget(self.parameter_c_input)

            # endregion

            # Добавляем кнопку "Сохранить"
            self.save_button = QPushButton("Сохранить")
            self.save_button.clicked.connect(self.save_training)
            self.create_training_layout.addWidget(self.save_button)

        # endregion

    # endregion

    def is_instructor(self):
        if len(self.current_user) == 16:
            return True
        return False

    # region Функции для "Кураторство" -> "Поиск"
    def global_clear_search_field(self):
        """
        Очищает поле поиска, формирует таблицу заново
        :return:
        """
        try:
            self.global_search_edit.clear()
            self.global_fill_possible_supervision_table()
        except Exception as e:
            QMessageBox.critical(self, "Critical Error", str(e))
            print(f"Ошибка при очистке поиска: {str(e)}")

    def global_fill_possible_supervision_table(self):
        """
        Заполнение таблицы ВСЕМИ возможными вариантами
        :return:
        """
        try:
            self.global_search_results_table.clearContents()  # Очищаем таблицу перед заполнением
            search_results = global_search_users_by_lastname("")  # Получаем всех пользователей
            self.global_filling_table(search_results)
        except Exception as e:
            QMessageBox.critical(self, "Critical Error", str(e))
            print(f"Ошибка при заполнении таблицы возможного кураторства: {str(e)}")

    def global_filling_table(self, search_results):
        """
        Функция заполнения таблицы всех возможных отношений кураторов
        :param search_results:
        :return:
        """
        try:
            # Очистка содержимого таблицы
            self.global_search_results_table.clearContents()
            self.global_search_results_table.setRowCount(0)

            # Заполнение таблицы данными
            for row_index, row_data in enumerate(search_results):
                self.global_search_results_table.insertRow(row_index)
                for col_index, col_data in enumerate(row_data[1:]):  # Пропускаем первый элемент (ID)
                    item = QTableWidgetItem(col_data)
                    self.global_search_results_table.setItem(row_index, col_index, item)

                # Создаем кнопку "Добавить" и добавляем ее в последний столбец каждой строки
                add_button = QPushButton("Добавить")
                add_button.clicked.connect(lambda checked, row=row_data: self.add_to_supervision(row))
                self.global_search_results_table.setCellWidget(row_index, 4, add_button)

        except Exception as e:
            QMessageBox.critical(self, "Critical Error", str(e))
            print(f"Ошибка при заполнении таблицы возможного кураторства: {str(e)}")

    def global_search_button_clicked(self):
        """
        Обработчик кнопки поиска
        :return:
        """
        try:
            self.global_search_results_table.clearContents()  # Очищаем таблицу при каждом новом поиске
            self.global_filling_table(global_search_users_by_lastname(self.global_search_edit.text()))
        except Exception as e:
            QMessageBox.critical(self, "Critical Error", str(e))
            print(f"Ошибка при поиске кураторства: {str(e)}")

    def add_to_supervision(self, user_data):
        """
        Обработчик кнопки добавления кураторства
        :param user_data:
        :return:
        """
        try:
            # Добавление пользователя в таблицу Кураторства
            cosmonaut_id = user_data[0]  # Получаем ID пользователя
            instructor_id = int(self.current_user.get("id", ""))  # Получаем ID инструктора
            add_supervision(cosmonaut_id, instructor_id)
            # После успешного добавления обновляем таблицу возможного кураторства
            self.global_fill_possible_supervision_table()
        except Exception as e:
            print(str(e))

    def global_update_search_tab(self, index):
        if index == self.supervision_tab.indexOf(self.global_search_tab):
            # Это обновление для вкладки "Поиск"
            self.global_fill_possible_supervision_table()

    # endregion

    # region Функции для "Кураторство" -> "Мое кураторство"

    def instructor_fill_possible_supervision_table(self):
        try:
            instructor_id = int(self.current_user.get("id", ""))
            self.instructor_search_results_table.clearContents()  # Очищаем таблицу перед заполнением
            search_results = instructor_search_users_by_lastname(instructor_id, "")  # Получаем всех пользователей
            self.instructor_filling_table(search_results)
        except Exception as e:
            QMessageBox.critical(self, "Critical Error", str(e))
            print(f"Ошибка при заполнении таблицы возможного кураторства: {str(e)}")

    def instructor_filling_table(self, search_results):
        try:
            # Очистка содержимого таблицы
            self.instructor_search_results_table.clearContents()
            self.instructor_search_results_table.setRowCount(0)

            # Заполнение таблицы данными
            for row_index, row_data in enumerate(search_results):
                self.instructor_search_results_table.insertRow(row_index)
                for col_index, col_data in enumerate(row_data[1:]):  # Пропускаем первый элемент (ID)
                    item = QTableWidgetItem(col_data)
                    self.instructor_search_results_table.setItem(row_index, col_index, item)

                # Создаем кнопку "Добавить" и добавляем ее в последний столбец каждой строки
                add_button = QPushButton("Удалить")
                add_button.clicked.connect(lambda checked, row=row_data: self.delete_from_supervision(row))
                self.instructor_search_results_table.setCellWidget(row_index, 4, add_button)

        except Exception as e:
            QMessageBox.critical(self, "Critical Error", str(e))
            print(f"Ошибка при заполнении таблицы возможного кураторства: {str(e)}")

    def delete_from_supervision(self, user_data):
        """
        Обработчик кнопки добавления кураторства
        :param user_data:
        :return:
        """
        try:
            # Добавление пользователя в таблицу Кураторства
            cosmonaut_id = user_data[0]  # Получаем ID пользователя
            instructor_id = int(self.current_user.get("id", ""))  # Получаем ID инструктора
            delete_from_supervision(cosmonaut_id, instructor_id)
            # После успешного добавления обновляем таблицу возможного кураторства
            self.instructor_fill_possible_supervision_table()
        except Exception as e:
            print(str(e))

    def instructor_search_button_clicked(self):
        """
        Обработчик кнопки поиска
        :return:
        """
        try:
            instructor_id = int(self.current_user.get("id", ""))
            self.instructor_search_results_table.clearContents()  # Очищаем таблицу при каждом новом поиске
            self.instructor_filling_table(
                instructor_search_users_by_lastname(instructor_id, self.instructor_search_edit.text()))
        except Exception as e:
            QMessageBox.critical(self, "Critical Error", str(e))
            print(f"Ошибка при поиске кураторства: {str(e)}")

    def instructor_clear_search_field(self):
        """
        Очищает поле поиска, формирует таблицу заново
        :return:
        """
        try:
            self.instructor_search_edit.clear()
            self.instructor_fill_possible_supervision_table()
        except Exception as e:
            QMessageBox.critical(self, "Critical Error", str(e))
            print(f"Ошибка при очистке поиска: {str(e)}")

    def update_instructor_supervision_tab(self, index):
        if index == self.supervision_tab.indexOf(self.instructor_supervision_tab):
            # Это обновление для вкладки "Мое кураторство"
            self.instructor_fill_possible_supervision_table()

    # endregion

    # region Функции для "Личная страница"
    def logout(self):
        """Функция для деавторизации пользователя"""
        current_user = None
        self.login_window = LoginWindow(current_user)
        self.login_window.show()
        self.close()
        print("Выход из учетной записи")

    # endregion

    # region Функции для "Добавление тренировки"

    def get_input_data(self):
        instructor_id = int(self.current_user.get("id", ""))
        input_data = get_elements_by_ID_instructor(instructor_id)
        # Создайте список элементов "Данные №N"
        input_data_items = [f"Данные № {element[0]}" for element in input_data]
        return input_data_items

    def update_fields(self, index):
        # Обработчик события изменения значения в выпадающем списке
        if index == 0:  # Выбран пункт "Новые данные"
            self.parameter_a_input.clear()
            self.parameter_b_input.clear()
            self.parameter_c_input.clear()
            self.parameter_a_input.setEnabled(True)
            self.parameter_b_input.setEnabled(True)
            self.parameter_c_input.setEnabled(True)
        else:
            # Получение данных из БД по выбранному id и заполнение полей
            text = self.input_data_combobox.currentText().split()
            if not text:
                return
            selected_id = int(text[-1])

            input_data = get_input_data_by_ID(selected_id)
            # Получите данные из БД по selected_id и заполните соответствующие поля
            # Здесь просто пример
            self.parameter_a_input.setText(input_data[2])  # param_a
            self.parameter_b_input.setText(input_data[3])  # param_b
            self.parameter_c_input.setText(input_data[4])  # param_c
            self.parameter_a_input.setEnabled(False)
            self.parameter_b_input.setEnabled(False)
            self.parameter_c_input.setEnabled(False)

    def update_input_data_combobox(self):
        self.input_data_combobox.clear()
        self.input_data_combobox.addItem("Новые данные")
        for element in self.get_input_data():
            self.input_data_combobox.addItem(element)

    def clear_all_widgets(self):
        self.training_name_input.clear()
        self.training_description_input.clear()
        self.training_duration_input.clear()
        self.parameter_a_input.clear()
        self.parameter_b_input.clear()
        self.parameter_c_input.clear()

    def save_training(self):
        # Обработчик нажатия на кнопку "Сохранить"
        training_name = self.training_name_input.text()
        training_description = self.training_description_input.text()
        training_duration = self.training_duration_input.text()
        parameter_a = self.parameter_a_input.text()
        parameter_b = self.parameter_b_input.text()
        parameter_c = self.parameter_c_input.text()

        if self.input_data_combobox.currentText() == "Новые данные":
            instructor_id = int(self.current_user.get("id", ""))

            input_data = {
                "ID_instructor": instructor_id,
                "param_A": parameter_a,
                "param_B": parameter_b,
                "param_C": parameter_c,
            }

            try:
                add_input_data(input_data)

            except Exception as e:
                QMessageBox.critical(self, "Critical Error", str(e))
                print(f"Ошибка при добавлении входных данных: {str(e)}")

        text = self.input_data_combobox.currentText().split()
        if text[-1] == "данные":
            input_data = get_last_input_data()
            ID_input_data = input_data[0]
        else:
            ID_input_data = int(text[-1])

        training_data = {
            "train_name": training_name,
            "description": training_description,
            "duration": training_duration,
            "ID_input_data": ID_input_data,
        }
        try:
            add_training(training_data)
            QMessageBox.information(self, "Успех", "Тренировка добавлена успешно!")
            self.update_input_data_combobox()
            self.clear_all_widgets()

        except Exception as e:
            QMessageBox.critical(self, "Critical Error", str(e))
            print(f"Ошибка при добавлении тренировки: {str(e)}")

    # endregion