# Rest_api_py
Здесь представлена реализация Rest API сервиса, в рамках отбора в школу бэкенд-разработки Яндекса.
Для запуска проекта нужно выполнить следующие шаги:
  1) Склонировать проект и зайти в папку проекта
  2) Если сервер уже запущен то выполнить команду - 'killall python' 
  или 'sudo kill -9 "process PID"' PID можно найти командой 'sudo netstat -ltup'
  3) Выполнить команду 'bash start_server.sh'
  
  2.5) Вместо 2 и 3 шага можно выполнить 'make all'


Перед использованием желательно удалить все текущие таблицы которые есть в mysql в базе данных rest_api1, сделать это можно так:
  
  1) Зайти в mysql (команда в bash - 'mysql')
  
  2) Выбрать базу данных - 'use rest_api1;'
  
  3) Очистить таблицу - 'TRUNCATE TABLE citizen;'
  
  4) Выйти из mysql('exit') и начать запускать тесты

Сервер будет работать после перезагрузки Виртуальной машины - соответствующее правило прописано в crontab ("cat /etc/crontab")

Тесты находятся в папке tests, невалидные тесты содержат в имени 'invalid' с описанием того что именно невалидно


При реализации были использованы библиотеки:

Flask - Общее строение, 

flask_SQLAlchemy - для работы с базой данных, 

Datetime - для валидации и сохранения даты, 

Numpy - для реализации подсчета перцентилей;

Для хранения данных была использована база данных Mysql

Также есть тесты для apache benchmark, если он скачан то можно запустить скрипты в папке apache_test, там есть для каждой функции скрипт, import_id по дефолту 10, его можно изменить.

## Файлы проекта
  1) view.py - Отвечает за всю валидацию и все комманды Rest API сервиса
  
  2) models.py - Хранит класс жителя
  
  3) config.py - конфигурация проекта
  
  4) app.py - первичное объявление и обращение к базе данных
  
  5) main.py - запуск программы
  
  6) tests/ - содержит shell скрипты тестов каждой функции с валидными и невалидными данными/запросами
  
  7) start_server.sh - скрипт запуска сервера через gunicorn, именно его запускает Виртуальная машина при перезагрузке
  
  8) apache_test/ - содержит скрипты для проверок через apache benchmark. Можно запустить с помощью Makefile: 'make ap_get', 'make ap_stat', 'make ap_birth'.
