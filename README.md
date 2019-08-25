## rest_api_py
This is the implementation of the entrance project to the yandex backend development school
If you want to launch this project, follow these steps:
  1)Clone this project and go to project folder
  2)Print this command "bash start_server.sh"
  

Сервер будет работать после перезагрузки Виртуальной машины - соответствующее правило прописано в crontab ("cat /etc/crontab")
Тесты находятся в папке tests, невалидные тесты содержат в имени 'invalid' с описанием того что именно невалидно


При реализации были использованы библиотеки: 
Flask - Общее строение, 
flask_SQLAlchemy - для работы с базой данных, 
Datetime - для валидации и сохранения даты, 
Numpy - для реализации подсчета перцентилей;
Для хранения данных была использована база данных Mysql


# Файлы проекта
  1)view.py - Отвечает за всю валидацию и все комманды Rest API сервиса
  2)models.py - Хранит класс жителя
  3)config.py - конфигурация проекта
  4)app.py - первичное объявление и обращение к базе данных
  5)main.py - запуск программы
  6)tests/ - содержит shell скрипты тестов каждой функции с валидными и невалидными данными/запросами
  7)start_server.sh - скрипт запуска сервера через gunicorn, именно его запускает Виртуальная машина при перезагрузке
