import os
from dotenv import load_dotenv
load_dotenv()

# SECRET_KEY = os.urandom(32)

HOST = os.environ['HOST']
PORT = os.environ['PORT']
USERNAME = os.environ['USERNAME']
PASSWORD = os.environ['PASSWORD']
DATABASE_NAME = os.environ['DATABASE_NAME']

database_path = f'postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}'

SQLALCHEMY_DATABASE_URI = database_path
SQLALCHEMY_TRACK_MODIFICATIONS = False
