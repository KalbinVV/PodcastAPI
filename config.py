import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

DB_URL = os.environ.get('DB_URL')

SECRET = os.environ.get('SECRET')

ROOT_ROLE_NAME = os.environ.get('ROOT_ROLE_NAME')

ROOT_LOGIN = os.environ.get('ROOT_LOGIN')
ROOT_PASSWORD = os.environ.get('ROOT_PASSWORD')
