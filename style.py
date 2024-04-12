from PyQt6.QtGui import QFont

# Шрифт для всего приложения
FONT = QFont("Arial", 12)

# Цвета
PRIMARY_COLOR = "#2c3e50"  # Основной цвет (темно-синий)
SECONDARY_COLOR = "#3498db"  # Вторичный цвет (голубой)
LIGHT_TEXT_COLOR = "#ffffff"  # Цвет текста (белый)
DARK_TEXT_COLOR = "#000000"  # Цвет текста (черный)
BACKGROUND_COLOR = "#ecf0f1"  # Цвет фона (светло-серый)
BACKGROUND_COLOR_LIGHT = "#ffffff"  # Цвет фона (белый)

STANDARD_SIZE = 12
FONT_NAME = "Arial"
MIDDLE_FONT_SIZE = f"{STANDARD_SIZE}px"
BIG_FONT_SIZE = f"{int(STANDARD_SIZE * 1.6)}px"
SMALL_FONT_SIZE = f"{int(STANDARD_SIZE / 1.6)}px"

MIDDLE_LABEL_STYLE = """
QLabel {
    color: %s;
    font-family: %s;
    font-size: %s;
}
""" % (DARK_TEXT_COLOR, FONT_NAME, MIDDLE_FONT_SIZE)

BIG_LABEL_STYLE = """
QLabel {
    color: %s;
    font-family: %s;
    font-size: %s;
}
""" % (DARK_TEXT_COLOR, FONT_NAME, BIG_FONT_SIZE)

# Стиль для QLineEdit
LINEEDIT_STYLE = """
QLineEdit {
    background-color: %s;
    border: 1px solid %s;
    border-radius: 5px; 
    padding: 5px; 
    font-family: %s;
    font-size: %s;
}

QLineEdit:placeholder {
    color: %s;
    font-family: %s;
    font-size: %s;
}
""" % (
BACKGROUND_COLOR_LIGHT, SECONDARY_COLOR, FONT_NAME, MIDDLE_FONT_SIZE, DARK_TEXT_COLOR, FONT_NAME, SMALL_FONT_SIZE)

# Стили кнопок
BUTTON_STYLE = """
QPushButton {
    background-color: %s;
    color: %s;
    border-radius: 5px;
    padding: 10px 20px;
    font-family: %s;
    font-size: %s;
}

QPushButton:hover {
    background-color: %s;
}
""" % (PRIMARY_COLOR, LIGHT_TEXT_COLOR, FONT_NAME, MIDDLE_FONT_SIZE, SECONDARY_COLOR)

# Стиль для QWidget
Q_WIDGET_STYLE = """
QWidget {
    background-color: %s;
}
""" % BACKGROUND_COLOR

# Стиль для QCheckBox
CHECKBOX_STYLE = """
QCheckBox {
    color: %s;        /* Цвет текста */
    font-family: %s;
    font-size: %s;
}
""" % (DARK_TEXT_COLOR, FONT_NAME, MIDDLE_FONT_SIZE)

# Стиль для QMessageBox
MESSAGEBOX_STYLE = """
QMessageBox {
    background-color: %s;
}
""" % BACKGROUND_COLOR

# Стиль для QTabWidget
TAB_WIDGET_STYLE = """
QTabWidget {
    background-color: %s;    /* Цвет фона */
}
""" % BACKGROUND_COLOR

# Стиль для QComboBox
COMBOBOX_STYLE = """
QComboBox {
    background-color: %s;
    border: 1px solid %s;
    border-radius: 5px;
    padding: 5px;
    font-family: %s;
    font-size: %s;
}
""" % (BACKGROUND_COLOR, SECONDARY_COLOR, FONT_NAME, MIDDLE_FONT_SIZE)

# Стиль для QTableWidget
TABLE_WIDGET_STYLE = """
QTableWidget {
    background-color: %s;    /* Цвет фона */
    color: %s;                    /* Цвет текста */
    border: 1px solid %s;         /* Цвет рамки */
}
""" % (BACKGROUND_COLOR_LIGHT, DARK_TEXT_COLOR, SECONDARY_COLOR)

# Стиль для QTableWidgetItem
TABLE_ITEM_STYLE = """
QTableWidgetItem {
    background-color: #ffffff;    /* Цвет фона */
    color: %s;                    /* Цвет текста */
}
""" % LIGHT_TEXT_COLOR

# Стиль для QCalendarWidget
CALENDAR_WIDGET_STYLE = """
QCalendarWidget {
    background-color: %s;
    color: %s;
    header-text-color: %s;
}

QCalendarWidget QHeaderView {
    color: %s;  /* Цвет текста месяца и года */
}

QCalendarWidget QToolButton{
    background-color: transparent;
    color: %s;
}

""" % (BACKGROUND_COLOR_LIGHT, LIGHT_TEXT_COLOR, DARK_TEXT_COLOR, DARK_TEXT_COLOR, DARK_TEXT_COLOR)
