from PyQt6 import QtCore
from PyQt6.QtWidgets import QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QCheckBox, QMessageBox, \
    QTabWidget

from Logic.Cosmonauts.loginCosmonaut import login_cosmonaut
from Logic.Cosmonauts.registerCosmonaut import register_cosmonaut
from Logic.Errors.Errors import UserIsExist, MyValidationError
from Logic.Instructors.loginInstructor import login_instructor
from Logic.Instructors.registerInstructor import register_instructor
from UI.AuthData import AuthData
from UI.RegistrationValidation import RegistrationData, validate_data
from style import BUTTON_STYLE

from config import START_LOGIN_X, START_LOGIN_Y, LOGIN_X, LOGIN_Y, START_MAIN_X, START_MAIN_Y, MAIN_X, MAIN_Y

from globals import current_user


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
        layout.addWidget(self.email_input)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Пароль")
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
                QMessageBox.information(self, "Успех", "Авторизация прошла успешно!")
                self.open_main_window(current_user)

            except UserIsExist as e:
                QMessageBox.warning(self, "Ошибка", str(e))

            except Exception as e:
                QMessageBox.critical(self, "Critical Error", str(e))
                print(str(e))
        # endregion

        # region Космонавт
        else:

            try:
                data = data.dict()  # Преобразование данных обратно в словарь для использования в регистрации
                current_user = login_cosmonaut(**data)  # получение данных о текущем пользователе
                QMessageBox.information(self, "Успех", "Авторизация прошла успешно!")
                self.open_main_window(current_user)

            except UserIsExist as e:
                QMessageBox.warning(self, "Ошибка", str(e))

            except Exception as e:
                QMessageBox.critical(self, "Critical Error", str(e))
                print(str(e))
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
                print(str(e))
        # endregion

        # region Космонавт
        else:

            try:
                # Отображение сообщения об ошибке, если данные не прошли валидацию
                data = data.dict()  # Преобразование данных обратно в словарь для использования в регистрации
                del data['work_experience']
                current_user = register_cosmonaut(**data)
                QMessageBox.information(self, "Успех", "Регистрация прошла успешно!")
                self.open_main_window(current_user)

            except UserIsExist as e:
                QMessageBox.warning(self, "Ошибка", str(e))

            except Exception as e:
                QMessageBox.critical(self, "Critical Error", str(e))
                print(str(e))
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

        self.tab_widget.addTab(self.training_tab, "Выбор тренировки")
        self.tab_widget.addTab(self.personal_page_tab, "Личная страница")

        # region Выбор тренировки
        # Вкладка "Выбор тренировки"
        training_layout = QVBoxLayout()
        self.training_tab.setLayout(training_layout)
        training_layout.addWidget(QPushButton("Кнопка на вкладке 'Выбор тренировки'"))
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
        print(len(self.current_user))
        for field in fields:
            label = QLabel(field + ":")
            personal_layout.addWidget(label)
            # Проверяем наличие данных о пользователе и выводим их
            if self.current_user:
                label_value = QLabel(str(self.current_user.get(dict_keys[i], "")))
                personal_layout.addWidget(label_value)
                i += 1

        # Добавление поля "Стаж работы", если длина списка current_user равна 16
        if len(self.current_user) == 16:
            work_experience_label = QLabel("Стаж работы:")
            personal_layout.addWidget(work_experience_label)
            if self.current_user:
                work_experience_value = QLabel(str(self.current_user.get("work_experience", "")))
                personal_layout.addWidget(work_experience_value)

        personal_layout.addWidget(QPushButton("Кнопка на вкладке 'Личная страница'"))
        # endregion

        # Создаем кнопку "Выйти из учетной записи"
        logout_button = QPushButton("Выйти из учетной записи")
        logout_button.clicked.connect(self.logout)
        self.tab_widget.addTab(logout_button, " ")
    # endregion

    def logout(self):
        """Функция для деавторизации пользователя"""
        current_user = None
        self.login_window = LoginWindow(current_user)
        self.login_window.show()
        self.close()
        print("Выход из учетной записи")