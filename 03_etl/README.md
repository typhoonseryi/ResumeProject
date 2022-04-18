#Проектное задание: ETL

##Скрипт movies_migrate.py осуществляет перенос обновленных данных из БД Postgres в ElasticSearch.
##На вход подаются 4 параметра:
- table: название таблицы БД для отслеживания изменений
- chunk-size: размер считываемой пачки данных
- search-period: период отслеживания изменений
- state-filename: название файла, куда будет записываться текуще состояние

##Пример вызова скрипта: 
python movies_migrate.py -t film_work -c 100 -s 5 -f state_file