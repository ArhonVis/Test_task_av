# -*- coding: utf-8 -*
import databases
from databases import Database

from config import db as cf


DB_USER = cf.get("DB_USER", "login")
DB_PASSWORD = cf.get("DB_PASSWORD", "password")
DB_HOST = cf.get("DB_HOST", "localhost")
DB_NAME = cf.get("DB_NAME", "dbname")
SQLALCHEMY_DATABASE_URL = (
	f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"
)
database: Database = databases.Database(SQLALCHEMY_DATABASE_URL)
