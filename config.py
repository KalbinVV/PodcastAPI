import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

DB_URL = os.environ.get('DB_URL')
SECRET = os.environ.get('SECRET')