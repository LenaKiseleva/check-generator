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
Примените миграции и создайте суперюзера:
```bash
python manage.py makemigrations api
python manage.py migrate
python manage.py createsuperuser
```
Примените fixtures:
```bash
python manage.py loaddata api/fixtures/initial_data.json
```
Запустите django-rq:
```bash
python manage.py rqworker default
```
Запустите приложение:
```bash
python manage.py runserver
```
