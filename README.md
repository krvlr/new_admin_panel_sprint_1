# Greetings traveller
Описание структуры и порядок выполнения проекта:
1. `schema_design` - раздел c материалами для архитектуры базы данных.
2. `movies_admin` - раздел с материалами для панели администратора.
3. `sqlite_to_postgres` - раздел с материалами по миграции данных.

Порядок установки проекта:
0. Создание виртуального огружения и установка зависимостей:
В корневой директории выполните:
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
1. Установите postgresql
2. Выполните инициализирующую миграцию movies_database.ddl из директории schema_design:
psql -h postgres_host_name -U postgres_user_name -d movies_database -f movies_database.ddl
3. Задайте параметры запуска приложения, создав файл .env с параметрами по аналогии с .env.example
4. Выполните создание служебных таблиц django и последующие миграции. 
Для этого в директории movies_admin выполните следующее:
python manage.py migrate --fake movies 0001_initial -- для пропуска инициализирующей миграции
python manage.py migrate movies
5. Запустите приложение 
python manage.py runserver

Для миграции данных из sqlite выполните скрипт load_data.py из папки sqlite_to_postgres,
предварительно задав параметры запуска, создав файл .env по аналогии с .env.example