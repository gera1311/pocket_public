import pandas as pd
from sqlalchemy.orm import sessionmaker

from models import engine, MyTable


# Создание сессии
Session = sessionmaker(bind=engine)
session = Session()

# Чтение CSV файла
df = pd.read_csv('accounts.csv', delimiter=';')

session.query(MyTable).delete()

# Импорт данных в таблицу
for index, row in df.iterrows():
    entry = MyTable(
        id=row['id'],
        auth_data=row['auth_data'],
        proxy_ip=row['proxy_data'],
        ip=row['proxy_ip']
    )
    session.add(entry)

# Сохранение данных в базе данных
session.commit()
