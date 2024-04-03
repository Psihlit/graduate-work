import re

import pydantic_core
from PyQt6 import QtCore
from PyQt6.QtWidgets import QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QCheckBox, QMessageBox
from pydantic import ValidationError

from Logic.Cosmonauts.registerCosmonaut import register_cosmonaut
from Logic.Errors.Errors import UserIsExist, MyValidationError
from Logic.Instructors.registerInstructor import register_instructor
from UI.RegistrationValidation import RegistrationData, validate_data
from style import BUTTON_STYLE


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Авторизация")
        self.setGeometry(100, 100, 300, 200)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()

        self.window_label = QLabel("Авторизация")
        self.window_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.window_label)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Почта")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Пароль")
        layout.addWidget(self.password_input)

        self.role_checkbox = QCheckBox("Инструктор")
        layout.addWidget(self.role_checkbox)

        self.login_button = QPushButton("Авторизация")
        self.login_button.setStyleSheet(BUTTON_STYLE)
        layout.addWidget(self.login_button)

        self.registration_button = QPushButton("Зарегистрироваться")
        layout.addWidget(self.registration_button)

        # Установим обработчик для кнопки регистрации
        self.registration_button.clicked.connect(self.open_registration_window)

        self.central_widget.setLayout(layout)

    def open_registration_window(self):
        self.registration_window = RegistrationWindow()
        self.registration_window.show()
        self.close()


class RegistrationWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Регистрация")
        self.setGeometry(100, 100, 300, 200)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()

        # Создание меток для отображения ошибок
        self.error_labels = {
            "email": QLabel(""),
            "password": QLabel(""),
            "surname": QLabel(""),
            "name": QLabel(""),
            "patronymic": QLabel(""),
            "passport_data": QLabel(""),
            "citizenship": QLabel(""),
            "registration_address": QLabel(""),
            "residence_address": QLabel(""),
            "nationality": QLabel(""),
            "phone_number": QLabel(""),
            "education": QLabel(""),
            "work_experience": QLabel("")
        }

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

    def open_login_window(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

    def toggle_role_checkbox(self, state):
        if state == 2:  # 2 соответствует состоянию "нажат"
            self.work_experience_input.setVisible(True)
        else:
            self.work_experience_input.setVisible(False)

    def register_button_clicked(self):
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

        if self.role_checkbox.isChecked():
            try:
                # Отображение сообщения об ошибке, если данные не прошли валидацию
                data = data.dict()  # Преобразование данных обратно в словарь для использования в регистрации
                register_instructor(**data)
                QMessageBox.information(self, "Успех", "Регистрация прошла успешно!")

            except UserIsExist as e:
                QMessageBox.warning(self, "Ошибка", str(e))
        else:

            try:
                # Отображение сообщения об ошибке, если данные не прошли валидацию
                data = data.dict()  # Преобразование данных обратно в словарь для использования в регистрации
                del data['work_experience']
                register_cosmonaut(**data)
                QMessageBox.information(self, "Успех", "Регистрация прошла успешно!")

            except UserIsExist as e:
                QMessageBox.warning(self, "Ошибка", str(e))

            except Exception as e:
                QMessageBox.critical(self, "Critical Error", str(e))
                print(str(e))

