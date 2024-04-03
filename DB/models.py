from sqlalchemy import MetaData, Table, Column, Integer, String, Date, ForeignKey, TIMESTAMP

# Определяем метаданные
metadata = MetaData()

# Определяем таблицу Космонавт
cosmonauts = Table(
    'cosmonauts', metadata,
    Column('ID', Integer, primary_key=True, autoincrement=True),
    Column('email', String, nullable=False),
    Column('password', String, nullable=False),
    Column('surname', String, nullable=False),
    Column('name', String, nullable=False),
    Column('patronymic', String, nullable=True),
    Column('date_of_birth', TIMESTAMP, nullable=False),
    Column('passport_data', String(10), nullable=False),
    Column('citizenship', String, nullable=False),
    Column('marital_status', String, nullable=False),
    Column('registration_address', String, nullable=False),
    Column('residence_address', String, nullable=False),
    Column('nationality', String, nullable=False),
    Column('phone_number', String, nullable=False),
    Column('education', String, nullable=False)
)

# Определяем таблицу Инструктор
instructors = Table(
    'instructors', metadata,
    Column('ID', Integer, primary_key=True, autoincrement=True),
    Column('email', String, nullable=False),
    Column('password', String, nullable=False),
    Column('surname', String, nullable=False),
    Column('name', String, nullable=False),
    Column('patronymic', String, nullable=True),
    Column('date_of_birth', TIMESTAMP, nullable=False),
    Column('passport_data', String(10), nullable=False),
    Column('citizenship', String, nullable=False),
    Column('marital_status', String, nullable=False),
    Column('registration_address', String, nullable=False),
    Column('residence_address', String, nullable=False),
    Column('nationality', String, nullable=False),
    Column('phone_number', String, nullable=False),
    Column('education', String, nullable=False),
    Column('work_experience', Integer, nullable=False)
)

# Определяем таблицу Кураторство
supervisions = Table(
    'supervisions', metadata,
    Column('ID', Integer, primary_key=True, autoincrement=True),
    Column('ID_cosmonaut', ForeignKey(cosmonauts.c.ID), nullable=False),
    Column('ID_instructor', ForeignKey(instructors.c.ID), nullable=False)
)

# Определяем таблицу Входные данные
input_data = Table(
    'input_data', metadata,
    Column('ID', Integer, primary_key=True, autoincrement=True),
    Column('ID_instructor', ForeignKey(instructors.c.ID), nullable=False),
    Column('param_A', String),
    Column('param_B', String),
    Column('param_C', String)
)

# Определяем таблицу Тренировка
trainings = Table(
    'trainings', metadata,
    Column('ID', Integer, primary_key=True, autoincrement=True),
    Column('train_name', String, nullable=False),
    Column('description', String, nullable=False),
    Column('date_of_start', TIMESTAMP, nullable=False),
    Column('duration', Integer, nullable=False),
    Column('ID_input_data', ForeignKey(input_data.c.ID), nullable=False)
)

# Определяем таблицу Результаты
results = Table(
    'results', metadata,
    Column('ID', Integer, primary_key=True, autoincrement=True),
    Column('ID_cosmonaut', ForeignKey(cosmonauts.c.ID), nullable=False),
    Column('ID_instructor', ForeignKey(instructors.c.ID), nullable=False),
    Column('ID_training', ForeignKey(trainings.c.ID), nullable=False),
    Column('results', String, nullable=False),
    Column('comments', String, nullable=False)
)