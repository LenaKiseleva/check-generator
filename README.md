## Сервис генерации чеков 
У сети ресторанов есть множество точек, на которых готовятся заказы для клиентов. 
Каждый клиент хочет вместе с заказом получить чек, содержащий детальную информацию о заказе. 
Сотрудники кухни также хотят чек, чтобы в процессе готовки и упаковки заказа не забыть положить всё что нужно.
Сервис получает информацию о новом заказа, создаёт в БД чеки для всех принтеров точки указанной в заказе и ставит асинхронные задачи на генерацию PDF-файлов для этих чеков. 

## Технический стек

- Python
- Django
- Docker
- wkhtmltopdf
- PostgreSQL
- Redis

## Установка

Установите зависимости из requirements.txt:
```bash
pip install -r requirements.txt
```
Запустите docker:
```bash
sudo docker-compose up -d --build
```
Создайте .env файл с переменными окружения:


**Например**
```bash
# Переменные для базы данных
# DATABASE_URL=psql://<имя_пользователя>:<пароль>@<host>:<port>/<имя_базы_данных>

DATABASE_URL=psql://postgres_user:xxxyyyzzz@127.0.0.1:5432/postgres1
SECRET_KEY='vn&#d#fn%-6ccri7jji=%(n#&)7$$uy9o$k)+(icrqw%^h_tyz'
HOST='localhost'
PORT=6379
RQ_DB=0
RQ_PASSWORD='123456789'
RQ_DEFAULT_TIMEOUT=360
```
Примените миграции и создайте суперюзера:
```bash
python manage.py makemigrations api
python manage.py migrate
python manage.py createsuperuser
```
Примените fixtures:
```bash
python manage.py loaddata fixtures/initial_data.json
```
Запустите django-rq:
```bash
python manage.py rqworker default
```
Запустите приложение:
```bash
python manage.py runserver
```
