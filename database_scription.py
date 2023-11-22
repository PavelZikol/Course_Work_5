import psycopg2
from abstract_class import DBOperator


class DBScriptor(DBOperator):
    """Класс для выполнения скриптов создания БД, таблиц и заполнения таблиц"""

    def __init__(self):
        pass

    def create_db(self, params, db_name) -> None:
        """Создание БД"""
        connection = psycopg2.connect(**params)
        connection.autocommit = True
        cur = connection.cursor()
        cur.execute(f"DROP DATABASE IF EXISTS {db_name};")
        cur.execute(f"CREATE DATABASE {db_name};")
        cur.close()
        connection.close()

    def create_tables(self, cursor, fill_script_file) -> None:
        """Выполняет скрипт из файла create_tables_script для создания таблиц в БД"""
        with open(fill_script_file, 'r') as file:
            cursor.execute(file.read())

    def fill_tables(self, cursor, vacancies_dict: dict, vacancies_list: list):
        """Заполнение таблиц данными о вакансиях из json файла"""
        for k_name, v_id in vacancies_dict.items():
            cursor.execute(f"INSERT INTO employers VALUES (%s, %s)",
                           (int(v_id), k_name))

        for item in vacancies_list:
            cursor.execute(f"INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s)",
                           (int(item['id']), int(item['employer']['id']), item['name'],
                            item['salary']['from'], item['salary']['to'], item['alternate_url']))