## Виртуальная стажировка 
___
**PerevalAddAPI** - бэкенд приложение для хранения и обработки данных от туристов о горных перевалах

Приложение передает данные в ФССП

**формат данных** - *JSON*

*requirements*:
+ asgiref==3.7.2
+ Django==4.2.3
+ django-environ==0.10.0
+ djangorestframework==3.14.0
+ environ==1.0
+ psycopg2==2.9.6
+ python-dotenv==1.0.0
+ pytz==2023.3
+ sqlparse==0.4.4
+ typing_extensions==4.7.1
+ tzdata==2023.3

## Installation
```bash
pip install https://github.com/AnatolyTimofeev/DjangoModels/tree/main/virtstage

```
## Взаимодействие с API
+ [X]  /api/v1/ - создание перевала методом POST
+ [X] /api/v1/patch/pk - обновление данных методом PACTH
+ [X] /api/v1/get/pk - детальная информация о перевале GET
+ [X] /api/v1/get/?user_email=user@email.ru - GET запрос для получения данных по email

**DATABASE**:

***PostgreSQL 15.3***

## License

The module is available as open source
