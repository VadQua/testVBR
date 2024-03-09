# Тестовое задание Вдовиченко В.В. для Выберу.ру

Тестовое задание:
Нужно написать dag  на airflow,
 который выполняется раз в день
который берет список урлов из файла в сети (https://github.com/grimlyrosen/tests/raw/e04d9b18d0d2e087045e01b75d18aa0c21ce504a/urllist.csv) (задачи сбора данных из api можно выполнять параллельно в рамках лимитов)
и через api google page speed 
https://developers.google.com/speed/docs/insights/v5/get-started?hl=ru
собирает и значения LCP, TBT 
и сохраняет  эти значения в clickhouse
(нужно создать табличку для хранения).  Учесть, что для одного урла всего одно значение каждого параметра в день должно быть в таблице.

сделать любую визуализацию этих данных 

Результат код dag, ddl для таблички, код визуализаци в отдельном git репозитории

# Описание работы 
- в файле [ddl.sql](https://github.com/VadQua/testVBR/blob/main/ddl.sql) описан процесс создания абстрактной таблицы в БД (абстрактной потому что Кликхауса у меня на пк нет)
- в файле [data_save_dag.py](https://github.com/VadQua/testVBR/blob/main/data_save_dag.py) описан процесс выгрузки и сохранения данных в таблицу в базе Clickhouse, а также в файлы в csv-формате (сохранение в файлы обусловлено тем, что у меня нет базы ch на пк и процесс создания базы и загрузки в нее данных описан для абстрактно существующей базы и таблицы)
- в файле [build_dashboard.py](https://github.com/VadQua/testVBR/blob/main/build_dashboard.py) описан процесс построения дашборда на основе данных, сохраненных в csv-файле (также может быть реализован процесс выгрузки из ch-базы) ![Дашборд](https://github.com/VadQua/testVBR/assets/90639276/99768115-b2b6-4feb-9725-e29199e1b185) при помощи библиотеки Streamlit. Чтобы увидеть у себя дашборд, нужно прописать в консоли из директории с файлом [build_dashboard.py](https://github.com/VadQua/testVBR/blob/main/build_dashboard.py) **streamlit run build_dashboard.py**

