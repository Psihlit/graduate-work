import random
import time

import numpy as np
from PyQt6 import QtCore
from PyQt6.QtCore import Qt, QPointF, QTimer, QTime
from PyQt6.QtGui import QIntValidator, QPixmap
from PyQt6.QtWidgets import QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QCheckBox, QMessageBox, \
    QTabWidget, QComboBox, QHBoxLayout, QTableWidget, QTableWidgetItem, QCalendarWidget, QHeaderView, \
    QGraphicsScene, QGraphicsView, QGraphicsPixmapItem, QMenu

from Logic.Cosmonauts.Auth.loginCosmonaut import login_cosmonaut
from Logic.Cosmonauts.Auth.registerCosmonaut import register_cosmonaut
from Logic.Cosmonauts.Supervisions.get_info import get_info_about_supervision
from Logic.Cosmonauts.Trainings.get_training_data import get_training_data
from Logic.Cosmonauts.Trainings.get_trainings import get_trainings
from Logic.Cosmonauts.Trainings.save_training_result import save_training_result
from Logic.Errors.Errors import UserIsExist, MyValidationError
from Logic.Instructors.Auth.loginInstructor import login_instructor
from Logic.Instructors.Auth.registerInstructor import register_instructor
from Logic.Instructors.Supervisions.global_search import global_search_users_by_lastname, add_supervision
from Logic.Instructors.Supervisions.personal_search import delete_from_supervision, instructor_search_users_by_lastname
from Logic.Instructors.Trainings.addInputData import add_input_data, get_elements_by_ID_instructor
from Logic.Instructors.Trainings.add_training import get_last_input_data, add_training, get_input_data_by_ID

from UI.RegistrationValidation import RegistrationData, validate_data
from style import *

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
        self.central_widget.setStyleSheet(Q_WIDGET_STYLE)
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()

        self.window_label = QLabel("Авторизация")
        self.window_label.setStyleSheet(BIG_LABEL_STYLE)
        self.window_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.window_label)

        # region Ввод почты
        self.email_layout = QHBoxLayout()

        self.email_label = QLabel("Почта:")
        self.email_label.setStyleSheet(MIDDLE_LABEL_STYLE)
        self.email_input = QLineEdit()
        self.email_input.setStyleSheet(LINEEDIT_STYLE)
        self.email_input.setPlaceholderText("Введите вашу почту")
        self.email_input.setText("user@mail.com")  # по умолчанию

        self.email_layout.addWidget(self.email_label)
        self.email_layout.addWidget(self.email_input)

        layout.addLayout(self.email_layout)
        # endregion

        # region Ввод пароля
        self.password_layout = QHBoxLayout()

        self.password_label = QLabel("Пароль:")
        self.password_label.setStyleSheet(MIDDLE_LABEL_STYLE)
        self.password_input = QLineEdit()
        self.password_input.setStyleSheet(LINEEDIT_STYLE)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Введите ваш пароль")
        self.password_input.setText("qwerty123")  # по умолчанию
        self.password_input.setToolTip("Содержит минимум 1 букву и 1 цифру")

        self.password_layout.addWidget(self.password_label)
        self.password_layout.addWidget(self.password_input)

        layout.addLayout(self.password_layout)
        # endregion

        # region Выбор роли
        self.role_checkbox = QCheckBox("Инструктор")
        self.role_checkbox.setStyleSheet(CHECKBOX_STYLE)

        layout.addWidget(self.role_checkbox)
        # endregion

        # region Кнопки
        self.login_button = QPushButton("Авторизация")
        self.login_button.setStyleSheet(BUTTON_STYLE)
        self.login_button.clicked.connect(self.login_button_clicked)
        layout.addWidget(self.login_button)

        self.registration_button = QPushButton("Зарегистрироваться")
        self.registration_button.setStyleSheet(BUTTON_STYLE)
        self.registration_button.clicked.connect(self.open_registration_window)
        layout.addWidget(self.registration_button)
        # endregion

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
        data = {"email": self.email_input.text(),
                "password": self.password_input.text()
                }

        # region Инструктор
        if self.role_checkbox.isChecked():
            try:
                current_user = login_instructor(**data)
                # QMessageBox.information(self, "Успех", "Авторизация прошла успешно!")
                self.open_main_window(current_user)

            except UserIsExist as e:
                instructor_error_message = QMessageBox()
                instructor_error_message.setStyleSheet(MESSAGEBOX_STYLE)
                instructor_error_message.warning(self, "Ошибка", str(e))

            except Exception as e:
                instructor_critical_error_message = QMessageBox()
                instructor_critical_error_message.setStyleSheet(MESSAGEBOX_STYLE)
                instructor_critical_error_message.critical(self, "Critical Error", str(e))
                print(f"Ошибка при авторизации инструктора: {str(e)}")
        # endregion

        # region Космонавт
        else:

            try:
                current_user = login_cosmonaut(**data)  # получение данных о текущем пользователе
                # QMessageBox.information(self, "Успех", "Авторизация прошла успешно!")
                self.open_main_window(current_user)

            except UserIsExist as e:
                cosmonaut_error_message = QMessageBox()
                cosmonaut_error_message.setStyleSheet(MESSAGEBOX_STYLE)
                cosmonaut_error_message.warning(self, "Ошибка", str(e))

            except Exception as e:
                cosmonaut_critical_error_message = QMessageBox()
                cosmonaut_critical_error_message.setStyleSheet(MESSAGEBOX_STYLE)
                cosmonaut_critical_error_message.critical(self, "Critical Error", str(e))
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
        self.central_widget.setStyleSheet(Q_WIDGET_STYLE)
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()

        self.window_label = QLabel("Регистрация")
        self.window_label.setStyleSheet(BIG_LABEL_STYLE)
        self.window_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.window_label)

        # region Ввод почты
        email_layout = QHBoxLayout()

        self.email_label = QLabel("Почта:")
        self.email_label.setStyleSheet(MIDDLE_LABEL_STYLE)
        self.email_input = QLineEdit()
        self.email_input.setStyleSheet(LINEEDIT_STYLE)
        self.email_input.setPlaceholderText("Введите вашу почту")

        email_layout.addWidget(self.email_label)
        email_layout.addWidget(self.email_input)

        layout.addLayout(email_layout)
        # endregion

        # region Ввод пароля
        password_layout = QHBoxLayout()

        self.password_label = QLabel("Пароль:")
        self.password_label.setStyleSheet(MIDDLE_LABEL_STYLE)
        self.password_input = QLineEdit()
        self.password_input.setStyleSheet(LINEEDIT_STYLE)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Введите ваш пароль")
        self.password_input.setToolTip(
            "Пароль должен содержать хотя бы 1 букву и 1 символ, минимальная длина 5 символов")

        password_layout.addWidget(self.password_label)
        password_layout.addWidget(self.password_input)

        layout.addLayout(password_layout)
        # endregion

        # region Ввод фамилии
        surname_layout = QHBoxLayout()

        self.surname_label = QLabel("Фамилия:")
        self.surname_label.setStyleSheet(MIDDLE_LABEL_STYLE)
        self.surname_input = QLineEdit()
        self.surname_input.setStyleSheet(LINEEDIT_STYLE)
        self.surname_input.setPlaceholderText("Введите вашу фамилию")

        surname_layout.addWidget(self.surname_label)
        surname_layout.addWidget(self.surname_input)

        layout.addLayout(surname_layout)
        # endregion

        # region Ввод имени
        name_layout = QHBoxLayout()

        self.name_label = QLabel("Имя:")
        self.name_label.setStyleSheet(MIDDLE_LABEL_STYLE)
        self.name_input = QLineEdit()
        self.name_input.setStyleSheet(LINEEDIT_STYLE)
        self.name_input.setPlaceholderText("Введите ваше имя")

        name_layout.addWidget(self.name_label)
        name_layout.addWidget(self.name_input)

        layout.addLayout(name_layout)
        # endregion

        # region Ввод отчества
        patronymic_layout = QHBoxLayout()

        self.patronymic_label = QLabel("Отчество:")
        self.patronymic_label.setStyleSheet(MIDDLE_LABEL_STYLE)
        self.patronymic_input = QLineEdit()
        self.patronymic_input.setStyleSheet(LINEEDIT_STYLE)
        self.patronymic_input.setPlaceholderText("Введите ваше отчество (если имеется)")

        patronymic_layout.addWidget(self.patronymic_label)
        patronymic_layout.addWidget(self.patronymic_input)

        layout.addLayout(patronymic_layout)
        # endregion

        # region "Дата рождения"
        date_of_birth_layout = QHBoxLayout()

        self.date_of_birth_label = QLabel("Дата рождения:")
        self.date_of_birth_label.setStyleSheet(MIDDLE_LABEL_STYLE)
        self.show_calendar_button = QPushButton("Выбрать дату")
        self.show_calendar_button.setStyleSheet(BUTTON_STYLE)
        self.show_calendar_button.clicked.connect(self.show_calendar_button_clicked)
        self.date_of_birth_calendar = QCalendarWidget()
        self.date_of_birth_calendar.setStyleSheet(CALENDAR_WIDGET_STYLE)
        self.date_of_birth_calendar.hide()

        date_of_birth_layout.addWidget(self.date_of_birth_label)
        date_of_birth_layout.addWidget(self.show_calendar_button)

        layout.addLayout(date_of_birth_layout)
        layout.addWidget(self.date_of_birth_calendar)
        # endregion

        # region Ввод паспортных данных
        passport_data_layout = QHBoxLayout()

        self.passport_data_label = QLabel("Паспортные данные:")
        self.passport_data_label.setStyleSheet(MIDDLE_LABEL_STYLE)
        self.passport_data_input = QLineEdit()
        self.passport_data_input.setStyleSheet(LINEEDIT_STYLE)
        self.passport_data_input.setValidator(QIntValidator())  # для ввода только цифр
        self.passport_data_input.setMaxLength(10)  # ограничение на 10 символов
        self.passport_data_input.setToolTip("Введите серию и номер паспорта без пробелов")
        self.passport_data_input.setPlaceholderText("Введите ваши паспортные данные")

        passport_data_layout.addWidget(self.passport_data_label)
        passport_data_layout.addWidget(self.passport_data_input)

        layout.addLayout(passport_data_layout)
        # endregion

        # region Ввод гражданства
        citizenship_layout = QHBoxLayout()

        self.citizenship_label = QLabel("Гражданство:")
        self.citizenship_label.setStyleSheet(MIDDLE_LABEL_STYLE)
        self.citizenship_input = QLineEdit()
        self.citizenship_input.setStyleSheet(LINEEDIT_STYLE)
        self.citizenship_input.setPlaceholderText("Введите ваше гражданство")

        citizenship_layout.addWidget(self.citizenship_label)
        citizenship_layout.addWidget(self.citizenship_input)

        layout.addLayout(citizenship_layout)
        # endregion

        # region Ввод семейного положения
        marital_status_layout = QHBoxLayout()

        self.marital_status_label = QLabel("Семейное положение:")
        self.marital_status_label.setStyleSheet(MIDDLE_LABEL_STYLE)
        self.marital_status_combo = QComboBox()
        self.marital_status_combo.setStyleSheet(COMBOBOX_STYLE)
        self.marital_status_combo.addItems(["Замужем/Женат", "Не замужем/Не женат", "В разводе", "Другое"])

        marital_status_layout.addWidget(self.marital_status_label)
        marital_status_layout.addWidget(self.marital_status_combo)

        layout.addLayout(marital_status_layout)
        # endregion

        # РАЗОБРАТЬСЯ С ЭТИМ ВИДЖЕТОМ
        # ПРОБЛЕМА ИЗ_ЗА ComboBox СКОРЕЙ ВСЕГО
        # region Ввод места прописки
        registration_address_layout = QHBoxLayout()

        self.registration_address_label = QLabel("Место прописки:")
        self.registration_address_label.setStyleSheet(MIDDLE_LABEL_STYLE)
        self.registration_address_input = QLineEdit()
        self.registration_address_input.setStyleSheet(LINEEDIT_STYLE)
        # self.registration_address_input.setMinimumWidth(150)
        self.registration_address_input.setPlaceholderText("Введите ваше место прописки")

        registration_address_layout.addWidget(self.registration_address_label)
        registration_address_layout.addWidget(self.registration_address_input)

        layout.addLayout(registration_address_layout)
        # endregion

        # region Ввод места проживания
        residence_address_layout = QHBoxLayout()

        self.residence_address_label = QLabel("Место проживания:")
        self.residence_address_label.setStyleSheet(MIDDLE_LABEL_STYLE)
        self.residence_address_input = QLineEdit()
        self.residence_address_input.setStyleSheet(LINEEDIT_STYLE)
        self.residence_address_input.setPlaceholderText("Введите ваше место проживания")

        residence_address_layout.addWidget(self.residence_address_label)
        residence_address_layout.addWidget(self.residence_address_input)

        layout.addLayout(residence_address_layout)
        # endregion

        # region Ввод национальности
        nationality_layout = QHBoxLayout()

        self.nationality_label = QLabel("Национальность:")
        self.nationality_label.setStyleSheet(MIDDLE_LABEL_STYLE)
        self.nationality_input = QLineEdit()
        self.nationality_input.setStyleSheet(LINEEDIT_STYLE)
        self.nationality_input.setPlaceholderText("Введите вашу национальность")

        nationality_layout.addWidget(self.nationality_label)
        nationality_layout.addWidget(self.nationality_input)

        layout.addLayout(nationality_layout)
        # endregion

        # region Ввод номер телефона
        phone_number_layout = QHBoxLayout()

        self.phone_number_label = QLabel("Номер телефона:")
        self.phone_number_label.setStyleSheet(MIDDLE_LABEL_STYLE)
        self.phone_number_input = QLineEdit()
        self.phone_number_input.setStyleSheet(LINEEDIT_STYLE)
        self.phone_number_input.setPlaceholderText("Введите ваш номер телефона")
        self.phone_number_input.setToolTip("Формат номера: '+X(XXX)XXX-XX-XX'")

        phone_number_layout.addWidget(self.phone_number_label)
        phone_number_layout.addWidget(self.phone_number_input)

        layout.addLayout(phone_number_layout)
        # endregion

        # region Ввод образования
        education_layout = QHBoxLayout()

        self.education_label = QLabel("Образование:")
        self.education_label.setStyleSheet(MIDDLE_LABEL_STYLE)
        self.education_input = QLineEdit()
        self.education_input.setStyleSheet(LINEEDIT_STYLE)
        self.education_input.setPlaceholderText("Введите ваше образование")

        education_layout.addWidget(self.education_label)
        education_layout.addWidget(self.education_input)

        layout.addLayout(education_layout)
        # endregion

        self.role_checkbox = QCheckBox("Инструктор")
        self.role_checkbox.setStyleSheet(CHECKBOX_STYLE)
        self.role_checkbox.stateChanged.connect(self.toggle_role_checkbox)
        layout.addWidget(self.role_checkbox)

        # region Ввод стажа работы
        work_experience_layout = QHBoxLayout()

        self.work_experience_label = QLabel("Стаж работы:")
        self.work_experience_label.setVisible(False)
        self.work_experience_label.setStyleSheet(MIDDLE_LABEL_STYLE)
        self.work_experience_input = QLineEdit()
        self.work_experience_input.setStyleSheet(LINEEDIT_STYLE)
        self.work_experience_input.setValidator(QIntValidator())
        self.work_experience_input.setPlaceholderText("Введите ваш стаж работы")
        self.work_experience_input.setVisible(False)

        work_experience_layout.addWidget(self.work_experience_label)
        work_experience_layout.addWidget(self.work_experience_input)

        layout.addLayout(work_experience_layout)
        # endregion

        # region Кнопки
        self.registration_button = QPushButton("Зарегистрироваться")
        self.registration_button.setStyleSheet(BUTTON_STYLE)
        self.registration_button.clicked.connect(self.register_button_clicked)
        layout.addWidget(self.registration_button)

        self.back_to_login_button = QPushButton("Уже зарегистрированы?")
        self.back_to_login_button.setStyleSheet(BUTTON_STYLE)
        self.back_to_login_button.clicked.connect(self.open_login_window)
        layout.addWidget(self.back_to_login_button)
        # endregion

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
            self.work_experience_label.setVisible(True)
        else:
            self.work_experience_input.setVisible(False)
            self.work_experience_label.setVisible(False)

    def show_calendar_button_clicked(self):
        self.show_calendar_button.hide()
        self.date_of_birth_calendar.show()  # Показываем календарь при нажатии на кнопку

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
                date_of_birth=self.date_of_birth_calendar.selectedDate().toString("dd.MM.yyyy"),
                passport_data=self.passport_data_input.text(),
                citizenship=self.citizenship_input.text(),
                marital_status=self.marital_status_combo.currentText(),
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
            input_message = QMessageBox()
            input_message.setStyleSheet(MESSAGEBOX_STYLE)
            input_message.warning(self, "Ошибка заполнения данных!", str(e))
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
                instructor_error_message = QMessageBox()
                instructor_error_message.setStyleSheet(MESSAGEBOX_STYLE)
                instructor_error_message.warning(self, "Ошибка", str(e))

            except Exception as e:
                instructor_critical_error_message = QMessageBox()
                instructor_critical_error_message.setStyleSheet(MESSAGEBOX_STYLE)
                instructor_critical_error_message.critical(self, "Critical Error", str(e))
                print(f"Ошибка при авторизации инструктора: {str(e)}")
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
                cosmonaut_error_message = QMessageBox()
                cosmonaut_error_message.setStyleSheet(MESSAGEBOX_STYLE)
                cosmonaut_error_message.warning(self, "Ошибка", str(e))

            except Exception as e:
                cosmonaut_critical_error_message = QMessageBox()
                cosmonaut_critical_error_message.setStyleSheet(MESSAGEBOX_STYLE)
                cosmonaut_critical_error_message.critical(self, "Critical Error", str(e))
                print(f"Ошибка при авторизации космонавта: {str(e)}")
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
        self.tab_widget.setStyleSheet(TAB_WIDGET_STYLE)
        self.setCentralWidget(self.tab_widget)

        # Создаем вкладки и добавляем их в виджет вкладок
        self.training_tab = QWidget()
        self.training_tab.setStyleSheet(Q_WIDGET_STYLE)
        self.personal_page_tab = QWidget()
        self.personal_page_tab.setStyleSheet(Q_WIDGET_STYLE)
        self.supervision_tab = QTabWidget()
        self.supervision_tab.setStyleSheet(Q_WIDGET_STYLE)

        self.tab_widget.addTab(self.training_tab, "Выбор тренировки")
        self.tab_widget.addTab(self.personal_page_tab, "Личная страница")
        self.tab_widget.addTab(self.supervision_tab, "Кураторство")

        # region Выбор тренировки
        # Вкладка "Выбор тренировки"
        training_layout = QVBoxLayout()
        self.training_tab.setLayout(training_layout)

        self.training_table = QTableWidget()
        self.training_table.setStyleSheet(TABLE_WIDGET_STYLE)
        # Горизонтальное растягивание ячеек
        self.training_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        # # Вертикальное растягивание ячеек
        # self.global_search_results_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Вертикальное растягивание ячеек
        self.training_table.verticalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents)

        self.training_table.setColumnCount(4)
        self.training_table.setHorizontalHeaderLabels(["Название тренировки", "Описание", "Продолжительность, мин", ""])
        training_layout.addWidget(self.training_table, stretch=1)
        self.fill_possible_training_table()
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
            temp_layout = QHBoxLayout()

            label = QLabel(field + ":")
            label.setStyleSheet(MIDDLE_LABEL_STYLE)
            temp_layout.addWidget(label)
            # Проверяем наличие данных о пользователе и выводим их
            if self.current_user:
                label_value = QLabel(str(self.current_user.get(dict_keys[i], "")))
                label_value.setStyleSheet(MIDDLE_LABEL_STYLE)
                temp_layout.addWidget(label_value)
                i += 1
                personal_layout.addLayout(temp_layout)

        # Добавление поля "Стаж работы", если длина списка current_user равна 16
        if self.is_instructor():
            temp_layout = QHBoxLayout()

            work_experience_label = QLabel("Стаж работы:")
            work_experience_label.setStyleSheet(MIDDLE_LABEL_STYLE)
            temp_layout.addWidget(work_experience_label)
            if self.current_user:
                work_experience_value = QLabel(str(self.current_user.get("work_experience", "")))
                work_experience_value.setStyleSheet(MIDDLE_LABEL_STYLE)
                temp_layout.addWidget(work_experience_value)
                personal_layout.addLayout(temp_layout)

        logout_button = QPushButton("Выйти из учетной записи")
        logout_button.setStyleSheet(BUTTON_STYLE)
        personal_layout.addWidget(logout_button)
        logout_button.clicked.connect(self.logout)
        # endregion

        # region Кураторство

        # для инструктора
        if self.is_instructor():
            # region Поиск
            # Вкладка "Поиск"
            self.global_search_tab = QWidget()
            self.global_search_tab.setStyleSheet(Q_WIDGET_STYLE)
            self.global_search_layout = QVBoxLayout()
            self.global_search_tab.setLayout(self.global_search_layout)

            self.global_horizontal_layout = QHBoxLayout()

            # Добавляем виджеты в горизонтальный контейнер
            self.global_horizontal_layout.addWidget(QLabel("Поле поиска:").setStyleSheet(MIDDLE_LABEL_STYLE))
            self.global_search_edit = QLineEdit()
            self.global_search_edit.setStyleSheet(LINEEDIT_STYLE)
            self.global_horizontal_layout.addWidget(self.global_search_edit)

            self.global_search_button = QPushButton("Поиск")
            self.global_search_button.setStyleSheet(BUTTON_STYLE)
            self.global_horizontal_layout.addWidget(self.global_search_button)
            self.global_search_button.clicked.connect(self.global_search_button_clicked)

            # Добавляем кнопку "Очистить"
            self.global_clear_button = QPushButton("Очистить")
            self.global_clear_button.setStyleSheet(BUTTON_STYLE)
            self.global_horizontal_layout.addWidget(self.global_clear_button)
            self.global_clear_button.clicked.connect(self.global_clear_search_field)

            # Устанавливаем созданный горизонтальный контейнер в качестве макета для виджета self.search_tab
            self.global_search_layout.addLayout(self.global_horizontal_layout, stretch=1)

            self.global_search_results_table = QTableWidget()
            self.global_search_results_table.setStyleSheet(TABLE_WIDGET_STYLE)
            # Горизонтальное растягивание ячеек
            self.global_search_results_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            # # Вертикальное растягивание ячеек
            # self.global_search_results_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

            # Вертикальное растягивание ячеек
            self.global_search_results_table.verticalHeader().setSectionResizeMode(
                QHeaderView.ResizeMode.ResizeToContents)

            self.global_search_results_table.setColumnCount(5)
            self.global_search_results_table.setHorizontalHeaderLabels(["Фамилия", "Имя", "Отчество", "Почта", ""])
            self.global_search_layout.addWidget(self.global_search_results_table, stretch=1)
            self.global_fill_possible_supervision_table()

            self.supervision_tab.addTab(self.global_search_tab, "Поиск")
            self.supervision_tab.currentChanged.connect(self.global_update_search_tab)

            # endregion

            # region Мое кураторство

            # Вкладка "Мое кураторство"
            self.instructor_supervision_tab = QWidget()
            self.instructor_supervision_tab.setStyleSheet(Q_WIDGET_STYLE)
            self.instructor_supervision_layout = QVBoxLayout()
            self.instructor_supervision_tab.setLayout(self.instructor_supervision_layout)

            # Создаем горизонтальный контейнер для строки с полем ввода и кнопками
            self.instructor_horizontal_layout = QHBoxLayout()

            # Добавляем виджеты в горизонтальный контейнер
            self.instructor_horizontal_layout.addWidget(QLabel("Поле поиска:").setStyleSheet(MIDDLE_LABEL_STYLE))
            self.instructor_search_edit = QLineEdit()
            self.instructor_search_edit.setStyleSheet(LINEEDIT_STYLE)
            self.instructor_horizontal_layout.addWidget(self.instructor_search_edit)

            self.instructor_search_button = QPushButton("Поиск")
            self.instructor_search_button.setStyleSheet(BUTTON_STYLE)
            self.instructor_horizontal_layout.addWidget(self.instructor_search_button)
            self.instructor_search_button.clicked.connect(self.instructor_search_button_clicked)

            # Добавляем кнопку "Очистить"
            self.instructor_clear_button = QPushButton("Очистить")
            self.instructor_clear_button.setStyleSheet(BUTTON_STYLE)
            self.instructor_horizontal_layout.addWidget(self.instructor_clear_button)
            self.instructor_clear_button.clicked.connect(self.instructor_clear_search_field)

            # Устанавливаем созданный горизонтальный контейнер в качестве макета для виджета self.search_tab
            self.instructor_supervision_layout.addLayout(self.instructor_horizontal_layout)

            # Добавление таблицы с данными кураторства
            self.instructor_search_results_table = QTableWidget()
            self.instructor_search_results_table.setStyleSheet(TABLE_WIDGET_STYLE)
            # Горизонтальное растягивание ячеек
            self.instructor_search_results_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

            # # Вертикальное растягивание ячеек
            # self.instructor_search_results_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

            # Вертикальное растягивание ячеек
            self.instructor_search_results_table.verticalHeader().setSectionResizeMode(
                QHeaderView.ResizeMode.ResizeToContents)

            self.instructor_search_results_table.setColumnCount(5)  # Установите количество столбцов
            self.instructor_search_results_table.setHorizontalHeaderLabels(["Фамилия", "Имя", "Отчество", "Почта", ""])
            self.instructor_supervision_layout.addWidget(self.instructor_search_results_table, stretch=1)
            self.instructor_fill_possible_supervision_table()

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
                        temp_layout = QHBoxLayout()

                        label = QLabel(field + ":")
                        label.setStyleSheet(MIDDLE_LABEL_STYLE)
                        temp_layout.addWidget(label)
                        label_value = QLabel(str(instructor_info[i]))
                        label_value.setStyleSheet(MIDDLE_LABEL_STYLE)
                        temp_layout.addWidget(label_value)

                        self.cosmonaut_supervision_layout.addLayout(temp_layout)
                        i += 1
            # endregion

            # region Кураторства нет
            except TypeError as e:
                label = QLabel("У вас отсутствует куратор")
                label.setStyleSheet(MIDDLE_LABEL_STYLE)
                self.cosmonaut_supervision_layout.addWidget(label)
            # endregion

        # endregion

        # region Добавление тренировки (только Инструктор)
        if self.is_instructor():
            self.create_training_tab = QWidget()
            self.create_training_tab.setStyleSheet(Q_WIDGET_STYLE)
            self.tab_widget.addTab(self.create_training_tab, "Добавление тренировки")

            # Добавляем виджеты на вкладку "Создание тренировки"
            self.create_training_layout = QVBoxLayout()
            self.create_training_tab.setLayout(self.create_training_layout)

            # region Название тренировки
            self.training_name_label = QLabel("Название тренировки:")
            self.training_name_label.setStyleSheet(MIDDLE_LABEL_STYLE)
            self.create_training_layout.addWidget(self.training_name_label)
            self.training_name_input = QLineEdit()
            self.training_name_input.setStyleSheet(LINEEDIT_STYLE)
            self.create_training_layout.addWidget(self.training_name_input)
            # endregion

            # region Описание тренировки
            self.training_description_label = QLabel("Описание тренировки:")
            self.training_description_label.setStyleSheet(MIDDLE_LABEL_STYLE)
            self.create_training_layout.addWidget(self.training_description_label)
            self.training_description_input = QLineEdit()
            self.training_description_input.setStyleSheet(LINEEDIT_STYLE)
            self.create_training_layout.addWidget(self.training_description_input)
            # endregion

            # region Продолжительность
            self.training_duration_label = QLabel("Продолжительность:")
            self.training_duration_label.setStyleSheet(MIDDLE_LABEL_STYLE)
            self.create_training_layout.addWidget(self.training_duration_label)
            self.training_duration_input = QLineEdit()
            self.training_duration_input.setStyleSheet(LINEEDIT_STYLE)
            self.create_training_layout.addWidget(self.training_duration_input)
            # endregion

            # region Добавление входных данных

            self.input_data_label = QLabel("Входные данные:")
            self.input_data_label.setStyleSheet(BIG_LABEL_STYLE)
            self.create_training_layout.addWidget(self.input_data_label)

            # region Выпадающее окно с выбором данных из БД
            self.input_data_combobox = QComboBox()
            self.input_data_combobox.setStyleSheet(COMBOBOX_STYLE)
            self.update_input_data_combobox()
            # Добавьте элементы из базы данных сюда
            self.create_training_layout.addWidget(self.input_data_combobox)
            # endregion

            # Обработчик события изменения значения в выпадающем списке
            self.input_data_combobox.currentIndexChanged.connect(self.update_fields)

            self.parameter_a_label = QLabel("Параметр А:")
            self.parameter_a_label.setStyleSheet(MIDDLE_LABEL_STYLE)
            self.create_training_layout.addWidget(self.parameter_a_label)
            self.parameter_a_input = QLineEdit()
            self.parameter_a_input.setStyleSheet(LINEEDIT_STYLE)
            self.create_training_layout.addWidget(self.parameter_a_input)

            self.parameter_b_label = QLabel("Параметр Б:")
            self.parameter_b_label.setStyleSheet(MIDDLE_LABEL_STYLE)
            self.create_training_layout.addWidget(self.parameter_b_label)
            self.parameter_b_input = QLineEdit()
            self.parameter_b_input.setStyleSheet(LINEEDIT_STYLE)
            self.create_training_layout.addWidget(self.parameter_b_input)

            self.parameter_c_label = QLabel("Параметр В:")
            self.parameter_c_label.setStyleSheet(MIDDLE_LABEL_STYLE)
            self.create_training_layout.addWidget(self.parameter_c_label)
            self.parameter_c_input = QLineEdit()
            self.parameter_c_input.setStyleSheet(LINEEDIT_STYLE)
            self.create_training_layout.addWidget(self.parameter_c_input)

            # endregion

            # region Кнопка
            self.save_button = QPushButton("Сохранить")
            self.save_button.setStyleSheet(BUTTON_STYLE)
            self.save_button.clicked.connect(self.save_training)
            self.create_training_layout.addWidget(self.save_button)
            # endregion
        # endregion

    # endregion

    def is_instructor(self):
        if len(self.current_user) == 16:
            return True
        return False

    # region Функции для "Выбор тренировки"

    def fill_possible_training_table(self):
        """
        Заполнение таблицы ВСЕМИ возможными вариантами
        :return:
        """
        try:
            self.training_table.clearContents()  # Очищаем таблицу перед заполнением
            trainings = get_trainings()  # Получаем все тренировки
            self.filling_training_table(trainings)
        except Exception as e:
            QMessageBox.critical(self, "Critical Error", str(e))
            print(f"Ошибка при заполнении таблицы возможного кураторства: {str(e)}")

    def filling_training_table(self, trainings):
        """
        Функция заполнения таблицы всех возможных отношений кураторов
        :param trainings:
        :return:
        """
        try:
            # Очистка содержимого таблицы
            self.training_table.clearContents()
            self.training_table.setRowCount(0)

            # Заполнение таблицы данными
            for row_index, row_data in enumerate(trainings):
                self.training_table.insertRow(row_index)
                for col_index, col_data in enumerate(row_data[1:]):  # Пропускаем первый элемент (ID)
                    item = QTableWidgetItem(str(col_data))
                    self.training_table.setItem(row_index, col_index, item)

                # Создаем кнопку "Добавить" и добавляем ее в последний столбец каждой строки
                start_button = QPushButton("Запуск")
                start_button.setStyleSheet(BUTTON_STYLE)
                start_button.clicked.connect(lambda checked, row=row_data: self.start_training(row))
                self.training_table.setCellWidget(row_index, 3, start_button)

        except Exception as e:
            QMessageBox.critical(self, "Critical Error", str(e))
            print(f"Ошибка при запуске тренировки: {str(e)}")

    def start_training(self, training_data):
        # Подготовка данных из базы данных

        # self.second_window = TrainingWindow(training_data, self.current_user)
        self.second_window = TrainingWindow(training_data, self.current_user)
        # self.second_window = Ui_Train_window()
        self.second_window.show()
        self.close()

    # endregion

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
                add_button.setStyleSheet(BUTTON_STYLE)
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
                add_button.setStyleSheet(BUTTON_STYLE)
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


class TrainingWindow(QMainWindow):
    def __init__(self, data, current_user):
        width = 620
        height = 648
        super().__init__()
        self.setWindowTitle("Training Window")
        self.setFixedSize(width, height)
        self.current_user = current_user
        self.data = data

        self.train_data = get_training_data(self.data[0])
        start_fan_speed = int(self.train_data[2])
        start_temp = int(self.train_data[3])
        end_temp = int(self.train_data[4])

        global fans
        fans = [1, 2, 3]
        # Выбираем случайный порядок вентиляторов для поломок
        random.shuffle(fans)
        self.first_flag = True
        self.end_flag = False
        self.end_flag_is_changed = False

        self.test_time1 = 1
        self.test_time1 = 2
        self.test_repair = 1.0

        # region флаги для работы алгоритма
        self.cv1_down_flag = False
        self.cv1_rounded_flag = False
        self.cv1_changed_flag = False
        self.cv1_broken = False

        self.cv2_down_flag = False
        self.cv2_rounded_flag = False
        self.cv2_changed_flag = False
        self.cv2_broken = False

        self.cv3_down_flag = False
        self.cv3_rounded_flag = False
        self.cv3_changed_flag = False
        self.cv3_broken = False

        self.result = []
        # endregion

        # Создаем QGraphicsScene
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, width, height)

        # Создаем QGraphicsView и устанавливаем нашу сцену
        self.view = QGraphicsView(self.scene)
        self.setCentralWidget(self.view)

        # Убираем полосы прокрутки
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Добавляем фоновое изображение
        image = "Images/Общий вид/Стартовая страница.png"
        self.background_image = QGraphicsPixmapItem(QPixmap(image))

        self.scene.addItem(self.background_image)
        self.background_image.setPos(0, 34)

        # region Верхние кнопки
        return_button = QPushButton("Завершить тренировку")
        return_button.setFixedWidth(int(width / 2 - 20))
        return_button.setStyleSheet(BUTTON_STYLE)
        return_button.clicked.connect(self.back_to_menu)

        return_button_item = self.scene.addWidget(return_button)
        return_button_item.setPos(10, 0)

        start_button = QPushButton("Начать")
        start_button.setFixedWidth(int(width / 2 - 20))
        start_button.setStyleSheet(BUTTON_STYLE)
        start_button.clicked.connect(self.start_simulation)

        start_button_item = self.scene.addWidget(start_button)
        start_button_item.setPos(width / 2 + 10, 0)
        # endregion

        # region Центральные вентиляторы
        self.cv1_label = QLabel("ЦВ1")
        self.cv1_label.setStyleSheet(TRANSPARENT_LABEL)

        self.cv1_label_item = self.scene.addWidget(self.cv1_label)
        self.cv1_label_item.setPos(138, 252)

        self.cv2_label = QLabel("ЦВ2")
        self.cv2_label.setStyleSheet(TRANSPARENT_LABEL)

        self.cv2_label_item = self.scene.addWidget(self.cv2_label)
        self.cv2_label_item.setPos(498, 538)

        self.cv3_label = QLabel("ЦВ3")
        self.cv3_label.setStyleSheet(TRANSPARENT_LABEL)

        self.cv3_label_item = self.scene.addWidget(self.cv3_label)
        self.cv3_label_item.setPos(110, 601)
        # endregion

        # region Вентиляторы
        self.v1_label = QLabel("В1")
        self.v1_label.setStyleSheet(TRANSPARENT_LABEL)

        self.v1_label_item = self.scene.addWidget(self.v1_label)
        self.v1_label_item.setPos(560, 195)

        self.v2_label = QLabel("В2")
        self.v2_label.setStyleSheet(TRANSPARENT_LABEL)

        self.v2_label_item = self.scene.addWidget(self.v2_label)
        self.v2_label_item.setPos(560, 224)
        # endregion

        # region СКПФ
        self.scpf1_label = QLabel("СКПФ1")
        self.scpf1_label.setStyleSheet(TRANSPARENT_LABEL)

        self.scpf1_label_item = self.scene.addWidget(self.scpf1_label)
        self.scpf1_label_item.setPos(418, 154)

        self.scpf2_label = QLabel("СКПФ2")
        self.scpf2_label.setStyleSheet(TRANSPARENT_LABEL)

        self.scpf2_label_item = self.scene.addWidget(self.scpf2_label)
        self.scpf2_label_item.setPos(418, 231)
        # endregion

        # region Служебная температура
        self.ser_temp_inp = QLabel(f"{start_temp} °C")
        self.ser_temp_inp.setStyleSheet(INFO_LABEL)

        self.ser_temp_inp_item = self.scene.addWidget(self.ser_temp_inp)
        self.ser_temp_inp_item.setPos(42, 178)

        self.ser_temp_out = QLabel(f"{end_temp} °C")
        self.ser_temp_out.setStyleSheet(INFO_LABEL)

        self.ser_temp_out_item = self.scene.addWidget(self.ser_temp_out)
        self.ser_temp_out_item.setPos(330, 110)
        # endregion

        # region АГЖ температура
        self.ag_temp_inp = QLabel(f"{start_temp} °C")
        self.ag_temp_inp.setStyleSheet(INFO_LABEL)

        self.ag_temp_inp_item = self.scene.addWidget(self.ag_temp_inp)
        self.ag_temp_inp_item.setPos(364, 186)

        self.ag_temp_out = QLabel(f"{end_temp} °C")
        self.ag_temp_out.setStyleSheet(INFO_LABEL)

        self.ag_temp_out_item = self.scene.addWidget(self.ag_temp_out)
        self.ag_temp_out_item.setPos(588, 150)
        # endregion

        # region Значения центральных вентиляторов
        self.cv1_data = QLabel(f"{start_fan_speed}")
        self.cv1_data.setStyleSheet(INFO_LABEL)

        self.cv1_data_item = self.scene.addWidget(self.cv1_data)
        self.cv1_data_item.setPos(186, 214)

        self.cv2_data = QLabel(f"{start_fan_speed}")
        self.cv2_data.setStyleSheet(INFO_LABEL)

        self.cv2_data_item = self.scene.addWidget(self.cv2_data)
        self.cv2_data_item.setPos(499, 513)

        self.cv3_data = QLabel(f"{start_fan_speed}")
        self.cv3_data.setStyleSheet(INFO_LABEL)

        self.cv3_data_item = self.scene.addWidget(self.cv3_data)
        self.cv3_data_item.setPos(142, 526)
        # endregion

        # region Значения вентиляторов
        self.v1_data = QLabel("1300")
        self.v1_data.setStyleSheet(INFO_LABEL)

        self.v1_data_item = self.scene.addWidget(self.v1_data)
        self.v1_data_item.setPos(502, 143)

        self.v2_data = QLabel("1200")
        self.v2_data.setStyleSheet(INFO_LABEL)

        self.v2_data_item = self.scene.addWidget(self.v2_data)
        self.v2_data_item.setPos(502, 274)
        # endregion

        # Поля для отображения значений

        # region Таймер
        # Создаем QLabel для отображения времени
        self.timer_label = QLabel("Время:")
        self.timer_label.setStyleSheet(TRANSPARENT_LABEL)
        self.timer_item = self.scene.addWidget(self.timer_label)
        self.timer_item.setPos(430, 37)

        self.time_label = QLabel("00:00:00")
        self.time_label.setStyleSheet(TRANSPARENT_LABEL)
        self.time_item = self.scene.addWidget(self.time_label)
        self.time_item.setPos(501, 37)

        # Таймер для обновления времени
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.time_elapsed = QTime(0, 0, 0)

        # Переменная для хранения времени в секундах
        self.elapsed_seconds = 0
        # endregion

        self.fan1_working = True
        self.fan2_working = True
        self.fan3_working = True

    def update_ui(self):
        self.ser_temp_inp.adjustSize()
        self.ser_temp_out.adjustSize()
        self.ag_temp_inp.adjustSize()
        self.ag_temp_out.adjustSize()
        self.cv1_data.adjustSize()
        self.cv2_data.adjustSize()
        self.cv3_data.adjustSize()
        self.v1_data.adjustSize()
        self.v2_data.adjustSize()

    def start_simulation(self):
        self.timer.start(1000)  # Запускаем таймер, чтобы обновлять значения каждую секунду

    def update_time(self):

        # Конец тренировки
        if self.end_flag == True:
            if self.end_flag_is_changed:
                return
            self.end_flag_is_changed = True
            QMessageBox.information(self, "Конец", "Тренировка завершена!")
            current_time = self.time_label.text()
            maximum_time = self.data[3]
            save_training_result(self.result, current_time, maximum_time, self.current_user, self.data)
            self.back_to_menu()
            return

        # Увеличиваем время в секундах
        self.elapsed_seconds += 1
        # Обновляем значение времени на метке
        hours = self.elapsed_seconds // 3600
        minutes = (self.elapsed_seconds % 3600) // 60
        seconds = self.elapsed_seconds % 60
        self.time_label.setText(f"{hours:02d}:{minutes:02d}:{seconds:02d}")

        # Выводим текущее время в секундах в консоль
        # print("Время в секундах:", self.elapsed_seconds)
        first_time = 5
        second_time = 20

        if self.first_flag and self.fan1_working and self.fan2_working and self.fan3_working:
            fans = [1, 2, 3]
            random.shuffle(fans)
            self.number_of_broken_fan = fans.pop()
            self.break_time = random.randint(self.elapsed_seconds + self.test_time1,
                                             self.elapsed_seconds + self.test_time1)
            self.first_flag = False

        self.simulations()
        self.update_ui()

    def simulations(self):

        if len(self.result) > 0 and self.result.count("Продолжать эксплуатацию модуля") == 3:
            if self.end_flag_is_changed:
                return
            self.end_flag = True

        if self.elapsed_seconds == self.break_time:

            if self.number_of_broken_fan == 1:
                # image_path = "Images/Общий вид/ЦВ1 поломка.png"
                # self.background_image.setPixmap(QPixmap(image_path))
                self.fan1_working = self.change_view(self.fan1_working, "Images/Общий вид/ЦВ1 поломка.png")

            if self.number_of_broken_fan == 2:
                # image_path = "Images/Общий вид/ЦВ2 поломка.png"
                # self.background_image.setPixmap(QPixmap(image_path))
                self.fan2_working = self.change_view(self.fan2_working, "Images/Общий вид/ЦВ2 поломка.png")

            if self.number_of_broken_fan == 3:
                # image_path = "Images/Общий вид/ЦВ3 поломка.png"
                # self.background_image.setPixmap(QPixmap(image_path))
                self.fan3_working = self.change_view(self.fan3_working, "Images/Общий вид/ЦВ3 поломка.png")

            self.first_flag = True

        if not self.fan1_working:
            temps = self.simulate_fan_breakage(self.cv1_data.text(), self.ser_temp_inp.text())
            self.cv1_data.setText(str(temps[0]))
            self.ser_temp_inp.setText(f"{str(round(temps[1], 2))} °C")
        else:
            temps = self.simulate_fan_repair(self.cv1_data.text(), self.ser_temp_inp.text(), 25)
            self.cv1_data.setText(str(temps[0]))
            self.ser_temp_inp.setText(f"{str(round(temps[1], 2))} °C")

        if not self.fan2_working:
            temps = self.simulate_fan_breakage(self.cv2_data.text(), self.ag_temp_inp.text())
            self.cv2_data.setText(str(temps[0]))
            self.ag_temp_inp.setText(f"{str(round(temps[1], 2))} °C")
        else:
            temps = self.simulate_fan_repair(self.cv2_data.text(), self.ag_temp_inp.text(), 25)
            self.cv2_data.setText(str(temps[0]))
            self.ag_temp_inp.setText(f"{str(round(temps[1], 2))} °C")

        if not self.fan3_working:
            temps = self.simulate_fan_breakage(self.cv3_data.text(), self.ser_temp_out.text())
            self.cv3_data.setText(str(temps[0]))
            self.ser_temp_out.setText(f"{str(round(temps[1], 2))} °C")
        else:
            temps = self.simulate_fan_repair(self.cv3_data.text(), self.ser_temp_out.text(), 25)
            self.cv3_data.setText(str(temps[0]))
            self.ser_temp_out.setText(f"{str(round(temps[1], 2))} °C")

    def change_view(self, fan_state, image_path):
        fan_state = not fan_state
        self.background_image.setPixmap(QPixmap(image_path))
        return fan_state

    def simulate_fan_breakage(self, fan_speed, temperature):
        temp1 = fan_speed.split()
        temp2 = temperature.split()

        fan_speed = int(temp1[0])
        current_temperature = float(temp2[0])

        if fan_speed > 0:
            fan_speed -= 25
            if fan_speed < 0:
                fan_speed = 0
        else:
            # Если скорость вращения равна 0, увеличиваем температуру на 0.01 каждые 4-6 секунд
            if self.elapsed_seconds % 6 == 0 or self.elapsed_seconds % 4 == 0:
                current_temperature += 0.01

        # Исходные данные
        temperature_increase_rate = 0.001  # процентное увеличение температуры за секунду

        # Рассчитываем новую температуру, учитывая увеличение температуры
        current_temperature *= (1 + temperature_increase_rate / 100)

        # Учитываем влияние вентиляции
        current_temperature += fan_speed * 0.00001  # добавляем к температуре воздействие вентиляции

        # Возвращаем новую температуру
        return fan_speed, current_temperature

    def simulate_fan_repair(self, fan_speed, temperature, temperature_shield):

        temp1 = fan_speed.split()
        temp2 = temperature.split()

        fan_speed = int(temp1[0])
        current_temperature = float(temp2[0])

        if fan_speed < 1500:
            fan_speed += 150
            if fan_speed > 1500:
                fan_speed = 1500
        else:
            # Если скорость вращения равна 0, увеличиваем температуру на 0.01 каждые 4-6 секунд
            if self.elapsed_seconds % 6 == 0 or self.elapsed_seconds % 4 == 0:
                current_temperature -= 0.01

        if current_temperature < temperature_shield:
            current_temperature = temperature_shield
            return fan_speed, current_temperature

        # Исходные данные
        temperature_increase_rate = 0.001  # процентное увеличение температуры за секунду

        # Рассчитываем новую температуру, учитывая увеличение температуры
        current_temperature *= (1 - temperature_increase_rate / 100)

        # Учитываем влияние вентиляции
        current_temperature -= fan_speed * 0.00001  # добавляем к температуре воздействие вентиляции

        # Возвращаем новую температуру
        return fan_speed, current_temperature

    def contextMenuEvent(self, event):
        # Определяем точки и действия для всех вентиляторов
        fan_data = {
            1: {
                'point': [(QPointF(128, 192), QPointF(184, 244))],
                'actions': ["Отключить вентилятор",
                            "Включить вентилятор",
                            "Прокрутить крыльчатку со стороны электродвигателя",
                            "Заменить вентилятор"]
            },
            2: {
                'point': [(QPointF(442, 486), QPointF(498, 547))],
                'actions': ["Отключить вентилятор",
                            "Включить вентилятор",
                            "Прокрутить крыльчатку со стороны электродвигателя",
                            "Заменить вентилятор"]
            },
            3: {
                'point': [(QPointF(103, 545), QPointF(157, 598))],
                'actions': ["Отключить вентилятор",
                            "Включить вентилятор",
                            "Прокрутить крыльчатку со стороны электродвигателя",
                            "Заменить вентилятор"]
            }
        }

        # Проверяем, содержится ли позиция курсора в одном из прямоугольников каждого вентилятора
        for fan_id, fan_info in fan_data.items():
            for (point_A, point_B) in fan_info['point']:
                if point_A.x() <= event.pos().x() <= point_B.x() and point_A.y() <= event.pos().y() <= point_B.y():
                    menu = QMenu(self)

                    # Добавляем действия в меню
                    for action_text in fan_info['actions']:
                        menu.addAction(action_text)

                    # Выполняем выбранное действие из контекстного меню
                    action = menu.exec(event.globalPos())

                    # Обработка выбранного действия
                    if action:
                        print(f"Выбрано действие: {action.text()}")
                        fan_down_flag = getattr(self, f"cv{fan_id}_down_flag")
                        fan_rounded_flag = getattr(self, f"cv{fan_id}_rounded_flag")
                        fan_changed_flag = getattr(self, f"cv{fan_id}_changed_flag")

                        if fan_down_flag:
                            self.handle_down_state(fan_id, action)
                        elif fan_rounded_flag:
                            self.handle_rounded_state(fan_id, action)
                        elif fan_changed_flag:
                            self.handle_changed_state(fan_id, action)
                        else:
                            self.handle_default_state(fan_id, action)

                    event.accept()
                    print(self.result)
                    return

        event.ignore()  # Пропустить обработку события, если курсор не находится в заданной области

    def handle_down_state(self, fan_id, action):
        if action.text() == "Включить вентилятор":
            self.current_time = time.time()
            elapsed_time = self.current_time - self.start_time
            setattr(self, f"cv{fan_id}_down_flag", False)
            minimum_elapsed_time = 30

            if elapsed_time >= minimum_elapsed_time:
                self.result.append(f"ЦВ{fan_id}: Перед повторным запуском прошло 30 секунд")

                if random.random() <= 0.4:
                    fan_working = self.change_view(getattr(self, f"fan{fan_id}_working"),
                                                   f"Images/Общий вид/Стартовая страница.png")
                    setattr(self, f"fan{fan_id}_working", fan_working)
                    self.result.append(f"ЦВ{fan_id}: Включился")
                    self.result.append("Продолжать эксплуатацию модуля")

                else:
                    self.result.append(f"ЦВ{fan_id}: Не включился")

            else:
                self.result.append(f"ЦВ{fan_id}: Перед повторным запуском НЕ прошло 30 секунд")
                setattr(self, f"cv{fan_id}_down_flag", False)

        elif action.text() == "Прокрутить крыльчатку со стороны электродвигателя":
            self.result.append(f"ЦВ{fan_id}: Прокрутка выполнена безопасно")
            setattr(self, f"cv{fan_id}_rounded_flag", True)
            setattr(self, f"cv{fan_id}_down_flag", False)

        elif action.text() == "Заменить вентилятор":
            self.result.append(f"ЦВ{fan_id}: Замена выполнена безопасно")
            setattr(self, f"cv{fan_id}_changed_flag", True)
            setattr(self, f"cv{fan_id}_down_flag", False)

        elif action.text() == "Отключить вентилятор" and getattr(self, f"cv{fan_id}_broken"):
            setattr(self, f"cv{fan_id}_broken", False)
            self.result.append(f"ЦВ{fan_id}: Отключен до по указанию Земли")

    def handle_rounded_state(self, fan_id, action):
        if action.text() == "Включить вентилятор":
            setattr(self, f"cv{fan_id}_rounded_flag", False)

            if random.random() <= 0.2:
                fan_working = self.change_view(getattr(self, f"fan{fan_id}_working"),
                                               f"Images/Общий вид/Стартовая страница.png")
                setattr(self, f"fan{fan_id}_working", fan_working)
                self.result.append(f"ЦВ{fan_id}: Включился после прокрутки крыльчатки")
                self.result.append("Продолжать эксплуатацию модуля")

            else:
                self.result.append(f"ЦВ{fan_id}: НЕ включился после прокрутки крыльчатки")

    def handle_changed_state(self, fan_id, action):
        if action.text() == "Включить вентилятор":
            setattr(self, f"cv{fan_id}_changed_flag", False)

            if random.random() <= 0.5:
                fan_working = self.change_view(getattr(self, f"fan{fan_id}_working"),
                                               f"Images/Общий вид/Стартовая страница.png")
                setattr(self, f"fan{fan_id}_working", fan_working)
                self.result.append(f"ЦВ{fan_id}: Включился после замены вентилятора")
                self.result.append("Продолжать эксплуатацию модуля")

            else:
                self.result.append(f"ЦВ{fan_id}: НЕ включился после замены вентилятора")
                self.result.append(f"ЦВ{fan_id}: Отказ")
                self.result.append("Продолжать эксплуатацию модуля")
                setattr(self, f"cv{fan_id}_broken", True)

    def handle_default_state(self, fan_id, action):
        if action.text() == "Включить вентилятор":
            repair_chance = 0.2
            if random.random() <= repair_chance:
                fan_working = self.change_view(getattr(self, f"fan{fan_id}_working"),
                                               f"Images/Общий вид/Стартовая страница.png")
                setattr(self, f"fan{fan_id}_working", fan_working)
                self.result.append(f"ЦВ{fan_id}: Включился")
                self.result.append("Продолжать эксплуатацию модуля")

            else:
                self.result.append(f"ЦВ{fan_id}: Не включился")

        elif action.text() == "Отключить вентилятор":
            setattr(self, f"cv{fan_id}_down_flag", True)
            self.start_time = time.time()
            self.result.append(f"ЦВ{fan_id}: Отключен")

        elif action.text() == "Прокрутить крыльчатку со стороны электродвигателя":
            self.result.append(f"ЦВ{fan_id}: Прокрутка выполнена НЕ безопасно")
            setattr(self, f"cv{fan_id}_rounded_flag", True)

        elif action.text() == "Заменить вентилятор":
            self.result.append(f"ЦВ{fan_id}: Замена выполнена НЕ безопасно")
            setattr(self, f"cv{fan_id}_changed_flag", True)

    def back_to_menu(self):
        self.main_window = MainWindow(self.current_user)
        self.main_window.show()
        self.close()

    def mousePressEvent(self, event):
        # Проверяем, что клик был выполнен внутри окна
        if event.button() == Qt.MouseButton.LeftButton and self.rect().contains(event.pos()):
            # Получаем координаты клика относительно главного окна
            click_pos = event.pos()
            # Выводим координаты в консоль
            print(f"Координаты клика: {click_pos.x()}, {click_pos.y()}")
