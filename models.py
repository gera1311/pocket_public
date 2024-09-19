import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

load_dotenv()

# Создание подключения к базе данных
engine = create_engine(f'postgresql://{os.getenv("POSTGRES_USER")}:'
                       f'{os.getenv("POSTGRES_PASSWORD")}@localhost:'
                       f'{os.getenv("POSTGRES_PORT")}/'
                       f'{os.getenv("POSTGRES_DB")}')

# Создание базового класса для моделей
Base = declarative_base()


class MyTable(Base):
    __tablename__ = 'my_table'

    id = Column(Integer, primary_key=True)
    auth_data = Column(String)
    proxy_ip = Column(String)
    ip = Column(String)


Base.metadata.create_all(engine)
