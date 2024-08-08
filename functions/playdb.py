import datetime
import os
import sys

import pymysql

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../functions')))

from variables import host, port, username, db_name

def create_table_with_added_tests():
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=username,
            password='',
            database=db_name
        )
        print("Создание таблицы с тестами")
        print("#" * 10)
        try:
            with connection.cursor() as cursor:
                products_tb = '''
                CREATE TABLE IF NOT EXISTS test_task (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name_of_test TEXT NOT NULL,
                    time_of_test TEXT DEFAULT '* * * * *',
                    data_add DATETIME,
                    test_path TEXT,
                    next_time DATETIME,
                    next_work INT DEFAULT 0,
                    next_condition DATETIME,
                    start_test DATETIME,
                    end_test DATETIME
                )'''
                cursor.execute(products_tb)
                print('таблица с тестами создана создана')
                connection.commit()

        finally:
            connection.close()
    except BaseException as e:
        print('ОШИБКА создания таблицы с тестами...')
        print(e)

def create_table_with_tests_results():
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=username,
            password='',
            database=db_name
        )
        print("Создание таблицы с результатами тестами")
        print("#" * 10)
        try:
            with connection.cursor() as cursor:
                products_tb = '''
                CREATE TABLE IF NOT EXISTS test_log (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    test_name TEXT NOT NULL,
                    test_time_length TEXT NOT NULL,
                    result TEXT NOT NULL,
                    time DATETIME,
                    mistake TEXT
                )'''
                cursor.execute(products_tb)
                print('таблица с результатами создана')
                connection.commit()

        finally:
            connection.close()
    except BaseException as e:
        print('ОШИБКА создания таблицы с результатами тестов...')
        print(e)

def get_all_add_test_data():
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=username,
            password='',
            database=db_name
        )
        print("получение всей информации о добавленных тестах")
        print("#" * 10)
        # mn = []
        try:
            with connection.cursor() as cursor:
                select_all_sql = "SELECT * FROM test_task"
                cursor.execute(select_all_sql)
                row = cursor.fetchall()
            return row
        finally:
            connection.close()
    except BaseException as e:
        print('ОШИБКА получения информации по тестам...')
        print(e)

def get_column_names():
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=username,
            password='',
            database=db_name
        )
        print("выбор названий для колонок из БД")
        print("#" * 10)
        # mn = []
        try:
            with connection.cursor() as cursor:
                select_all_sql = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'test_task'"
                cursor.execute(select_all_sql)
                row = cursor.fetchall()
            return row
        finally:
            connection.close()
    except BaseException as e:
        print('ОШИБКА выбора названий колонок для таблицы...')
        print(e)


def get_condition(id):
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=username,
            password='',
            database=db_name
        )
        print("состояние по тесту")
        print("#" * 10)
        try:
            with connection.cursor() as cursor:
                select_all_sql = f"SELECT next_work FROM test_task WHERE id = {id}"
                cursor.execute(select_all_sql)
                row = cursor.fetchone()
                symbols_to_remove = ",()"
                for symbol in symbols_to_remove:
                    row = str(row).replace(symbol, "")
            return row
        finally:
            connection.close()
    except BaseException as e:
        print('ОШИБКА получения состояния теста...')
        print(e)
# print(get_condition(2))

def get_all_result_test_data():
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=username,
            password='',
            database=db_name
        )
        print("получение всей информации по результатам тестов")
        print("#" * 10)
        # mn = []
        try:
            with connection.cursor() as cursor:
                select_all_sql = "SELECT id, test_name, test_time_length, result, mistake FROM test_log"
                cursor.execute(select_all_sql)
                row = cursor.fetchall()
            #     for i in row:
            #         # i = str(i)
            #         mn.append(i)
            # print(mn)
            return row
        finally:
            connection.close()
    except BaseException as e:
        print('ОШИБКА получения информации по результатам теста...')
        print(e)
# print(get_all_result_test_data())


def insert_data(file, text, path):
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=username,
            password='',
            database=db_name
        )
        print("Добавление теста в таблицу")
        print("#" * 10)
        all_name = names_tests()
        try:
            with connection.cursor() as cursor:
                if file in all_name:
                    update_sql = f"UPDATE test_task SET time_of_test = '{text}', data_add = NOW() WHERE name_of_test = '{file}'"
                    cursor.execute(update_sql)
                else:
                    if text == '':
                        create_table_sql = f"INSERT INTO test_task (name_of_test, data_add, test_path) VALUES ('{file}', NOW(), '{path}')"
                    else:
                        create_table_sql = f"INSERT INTO test_task (name_of_test, time_of_test,data_add, test_path) VALUES ('{file}','{text}', NOW(), '{path}')"
                    cursor.execute(create_table_sql)
                print("запись добавлена успешно")
                connection.commit()

        finally:
            connection.close()
    except BaseException as e:
        print('ОШИБКА добавления записи...')
        print(e)


def insert_result_data(name, time, result):
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=username,
            password='',
            database=db_name
        )
        print("Добавление результата теста в таблицу если нет ошибки")
        print("#" * 10)
        try:
            with connection.cursor() as cursor:

                create_table_sql = f"INSERT INTO test_log (test_name, test_time_length, result, time) VALUES ('{name}','{time}', '{result}', NOW())"

                cursor.execute(create_table_sql)
                print("результат теста добавлен успешно")
                connection.commit()

        finally:
            connection.close()
    except BaseException as e:
        print('ОШИБКА добавления результата теста без ошибки...')
        print(e)

def insert_mistake(name, time, result,mistake):
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=username,
            password='',
            database=db_name
        )
        print("Добавление результата теста с ошибкой")
        print("#" * 10)
        try:
            with connection.cursor() as cursor:
                create_table_sql = f"INSERT INTO test_log (test_name, test_time_length, result, time,mistake) VALUES ('{name}','{time}', '{result}', NOW(), '{mistake}')"
                cursor.execute(create_table_sql)
                print("результат с ошибкой добавлен успешно")
                connection.commit()

        finally:
            connection.close()
    except BaseException as e:
        print('ОШИБКА добавления результата с ошибкой...')
        print(e)


def all_add_tests():
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=username,
            password='',
            database=db_name
        )
        print("получение информации о тестах")
        print("#" * 10)
        mn = []
        try:
            with connection.cursor() as cursor:
                select_all_sql = "SELECT id,time_of_test,next_time,test_path FROM test_task"
                cursor.execute(select_all_sql)
                row = cursor.fetchall()
                # for i in row:
                #     i = str(i)
                #     mn.append(i[1:-3])
                # print(row)
            return row
        finally:
            connection.close()
    except BaseException as e:
        print('ОШИБКА выбора информации о тестов...')
        print(e)


def get_path(id):
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=username,
            password='',
            database=db_name
        )
        print("получение пути до теста")
        print("#" * 10)
        mn = []
        try:
            with connection.cursor() as cursor:
                select_all_sql = f"SELECT test_path FROM test_task WHERE id = {id}"
                cursor.execute(select_all_sql)
                row = cursor.fetchall()
                for i in row:
                    i = str(i)
                    mn.append(i[2:-3])
                # print(mn)
            return mn
        finally:
            connection.close()
    except BaseException as e:
        print('ОШИБКА получения пути до теста...')
        print(e)

# print(get_path(4))

def update_next_time(id,next_time):
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=username,
            password='',
            database=db_name
        )
        print("добавление времени следующего выполнения задания")
        print("#" * 10)
        try:
            with connection.cursor() as cursor:
                select_all_sql = f"UPDATE test_task set next_time = '{next_time}', next_work = 0 WHERE id = {id}"
                cursor.execute(select_all_sql)
                connection.commit()
        finally:
            connection.close()
    except BaseException as e:
        print('ОШИБКА обновления следующего времени...')
        print(e)
def work(name):
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=username,
            password='',
            database=db_name
        )
        print("текущая работа теста")
        print("#" * 10)
        try:
            with connection.cursor() as cursor:
                select_all_sql = f"UPDATE test_task set next_work = 1, next_condition = NOW() WHERE name_of_test = '{name}'"
                cursor.execute(select_all_sql)
                connection.commit()
        finally:
            connection.close()
    except BaseException as e:
        print('ОШИБКА добавления текущей работы теста...')
        print(e)


def end_work(name):
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=username,
            password='',
            database=db_name
        )
        print("добавление 2 кода - завершение работы теста")
        print("#" * 10)
        try:
            with connection.cursor() as cursor:
                select_all_sql = f"UPDATE test_task set next_work = 2 WHERE name_of_test = '{name}'"
                cursor.execute(select_all_sql)
                connection.commit()
        finally:
            connection.close()
    except BaseException as e:
        print('ОШИБКА добавления 2 кода...')
        print(e)

def select_dashboard_result(name):
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=username,
            password='',
            database=db_name
        )
        print("Выбор результатов для дашборда")
        print("#" * 10)
        mn = []
        try:
            with connection.cursor() as cursor:
                select_all_sql = f"SELECT result FROM test_log WHERE test_name = '{name}'"
                cursor.execute(select_all_sql)
                row = cursor.fetchall()
                for i in row:
                    i = str(i)
                    mn.append(i[2:-3])

                return mn
        finally:
            connection.close()
    except BaseException as e:
        print('ОШИБКА выбора результатов для дашборда...')
        print(e)

def select_dashboard_mistake(name):
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=username,
            password='',
            database=db_name
        )
        print("Получение ошибки с проваленного теста")
        print("#" * 10)
        try:
            mn=[]
            with connection.cursor() as cursor:
                select_all_sql = f"SELECT id, mistake FROM test_log WHERE test_name = '{name}' and result='failed'"
                cursor.execute(select_all_sql)
                row = cursor.fetchall()
                for i in row:
                    i = str(i)
                    mn.append(i[1:-3])
                return mn
        finally:
            connection.close()
    except BaseException as e:
        print('ОШИБКА получения ошибки...')
        print(e)

def delete_all_data():
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=username,
            password='',
            database=db_name
        )
        print("Очищение таблицы с результатами тестов")
        print("#" * 10)
        try:
            with connection.cursor() as cursor:
                delete_sql = "DELETE FROM test_log"
                cursor.execute(delete_sql)
                alter_sql = "ALTER TABLE test_log AUTO_INCREMENT = 1"
                cursor.execute(alter_sql)
                connection.commit()
                print("Удалено")
        finally:
            connection.close()
    except BaseException as e:
        print('ОШИБКА очищения таблицы с результатами тестов...')
        print(e)


def delete_all_result():
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=username,
            password='',
            database=db_name
        )
        print("очищение таблицы с тестами")
        print("#" * 10)
        try:
            with connection.cursor() as cursor:
                delete_sql = "DELETE FROM test_task"
                # alter_sql = ""
                cursor.execute(delete_sql)
                alter_sql = "ALTER TABLE test_task AUTO_INCREMENT = 1"
                # alter_sql = ""
                cursor.execute(alter_sql)
                connection.commit()
                print("удалено")
        finally:
            connection.close()
    except BaseException as e:
        print('ОШИБКА очищения таблицы с тестами...')
        print(e)


def delete_select_data(id):
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=username,
            password='',
            database=db_name
        )
        print("удалить выбранный тест")
        print("#" * 10)
        try:
            with connection.cursor() as cursor:
                delete_sql = f"DELETE FROM test_task WHERE id={id}"
                cursor.execute(delete_sql)
                connection.commit()
        finally:
            connection.close()
    except BaseException as e:
        print('ОШИБКА удаления выбранного теста')
        print(e)


def names_tests():
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=username,
            password='',
            database=db_name
        )
        print("выбор названий добавленных в очередь тестов")
        print("#" * 10)
        try:
            mn = []
            with connection.cursor() as cursor:
                select_all_sql = "SELECT name_of_test FROM test_task"
                cursor.execute(select_all_sql)
                row = cursor.fetchall()
                for i in row:
                    i = str(i)
                    mn.append(i[2:-3])
                return mn

        finally:
            connection.close()
    except BaseException as e:
        print('ОШИБКА выбора названий тестов...')
        print(e)
def add_start_end(start, end, name):
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=username,
            password='',
            database=db_name
        )
        print("добавление start end выполнения задания")
        print("#" * 10)
        try:
            with connection.cursor() as cursor:
                select_all_sql = f"UPDATE test_task set start_test = '{start}', end_test = '{end}' WHERE name_of_test = '{name}'"
                cursor.execute(select_all_sql)
                connection.commit()
        finally:
            connection.close()
    except BaseException as e:
        print('ОШИБКА добавление start end выполнения задания...')
        print(e)

def convert_seconds(seconds):
    return str(datetime.timedelta(seconds=seconds))
