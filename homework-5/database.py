import psycopg2

from config import config


class DataBase:
    '''
    Класс для создания базы данных
    '''
    instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self, db_name):
        self.__db_name = db_name

        self.__create_db()

    def __repr__(self):
        return f'{self.__class__.__name__}({self.db_name})'

    def __str__(self):
        return f'База данных {self.db_name}'

    def __create_db(self):
        '''
        Создаёт базу данных с переданным пользователем названием,
        заполняя её таблицами, которые создаются в последствии
        выполнения кода из файла fill_db.sql. Если база данных уже создана,
        то код просто не срабатывает
        '''
        db_data = config()

        try:
            connection = psycopg2.connect(dbname='postgres', **db_data)
            connection.autocommit = True

            with connection.cursor() as cursor:
                cursor.execute(f'CREATE DATABASE {self.db_name}')

            connection.close()

            # подключение к созданной базе данных
            connection = psycopg2.connect(dbname=f'{self.db_name}', **db_data)

            with connection.cursor() as cursor:
                with open('fill_db.sql', 'r', encoding='UTF-8') as sql_file:
                    create_query = sql_file.read()

                cursor.execute(create_query)

            connection.commit()
            connection.close()

        except psycopg2.errors.DuplicateDatabase:
            pass
        finally:
            connection.close()

    @property
    def db_name(self):
        '''
        Возвращает имя базы данных
        '''
        return self.__db_name


