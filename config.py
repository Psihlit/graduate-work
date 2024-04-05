from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

SECRET = os.environ.get("SECRET")

EMAIL = os.environ.get("EMAIL")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

SECRET_KEY = os.environ.get("SECRET_KEY")

START_LOGIN_X = 660
START_LOGIN_Y = 300
LOGIN_X = 300
LOGIN_Y = 200
START_MAIN_X = 10
START_MAIN_Y = 10
MAIN_X = 1366
MAIN_Y = 768
