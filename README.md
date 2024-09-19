## Инструкция по запуску скрипта

### Все команды выполняйте из главного репозитория проекта

1. Устанавливаем и активируем виртуальное окружение:

for macos/unix
```
python -m venv venv
source venv/bin/activate
```
for windows
```
python3 -m venv venv
.\Scripts\activate
```

2. Обновляем пакетный менеджер и устанавливаем зависимости:

```
pip install --upgrade pip
pip install -r requirements.txt
```

3. Создаем файл ```.env``` и заполняем его:

```
# Все поля обязательны для заполнение, имя юзера, пароль и название бд будут использоваться при создании базы данных PostgreSQL, 
# их вы придумайте сами прям в этом файле. Дальнейший вход в бд будет происходит по этим данным.
# PORT и HOST можете оставить как в этом примере, эти значения нужны для корректного коннекта к БД в контейнере.

POSTGRES_USER=myuser
POSTGRES_PASSWORD=mypassword
POSTGRES_DB=pocket
POSTGRES_PORT=5432
POSTGRES_HOST=localhost
```

4. Запускаем docker контейнер с базой данных PosgtreSQL
(Если не установлен docker, перед запуском контейнера, загуглите команды и установите по ним docker и docker compose)

```
docker compose -f docker-compose.production.yml up -d
```

5. Выполняем миграции из accounts.csv в базу данных PostgreSQL в контейнере
```
python db_logic.py
```

6. Запускаем скрипт
```
python main.py
```
