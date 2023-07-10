import json
import psycopg2

from config import config


def connect_to_db(db_name: str) -> tuple:
    '''
    Подключается к созданной базе данных
    '''
    db_data = config()
    connection = psycopg2.connect(dbname=f'{db_name}', **db_data)

    return (db_data, connection)


def get_supplier_data(file_name: str) -> list:
    '''
    Считывает данные из JSON-файла
    '''
    with open(file_name, 'r', encoding='UTF-8') as j_file:
        data = json.load(j_file)

    return data


def create_supplier_table(db_name: str) -> None:
    '''
    Создавёт таблицу supplier и заполяет её даннымми
    '''
    db_data, connection = connect_to_db(db_name)
    sup_data = get_supplier_data('suppliers.json')

    with connection.cursor() as cursor:
        cursor.execute('''
        CREATE TABLE suppliers(
            supplier_id serial,
            company_name varchar(100) NOT NULL,
            contact varchar(100) NOT NULL,
            address text,
            phone varchar(20) NOT NULL,
            fax varchar(20),
            homepage text,
            
            CONSTRAINT pk_suppliers_supplier_id PRIMARY KEY(supplier_id)
        )
        '''
                       )

        for data in sup_data:
            cursor.execute(
                'INSERT INTO suppliers (company_name, contact, address, phone, fax, homepage) '
                'VALUES (%s, %s, %s, %s, %s, %s)',
                (data['company_name'], data['contact'], data['address'], data['phone'],
                 data['fax'], data['homepage'])
            )

    connection.commit()
    connection.close()


def add_foreign_key(db_name) -> None:
    '''
    Добавляет foreign key в таблицу products, а так же
    ограничение на foreign key
    '''
    db_data, connection = connect_to_db(db_name)

    with connection.cursor() as cursor:
        cursor.execute('ALTER TABLE products ADD COLUMN supplier_id smallint')
        cursor.execute(
            'ALTER TABLE products ADD CONSTRAINT fk_products_supplier_id '
            'FOREIGN KEY(supplier_id) REFERENCES suppliers(supplier_id)'
        )

    connection.commit()
    connection.close()


def add_supplier_in_products(db_name):
    '''
    Обновляет таблицу, заполняя столбец supplier_id
    '''
    db_data, connection = connect_to_db(db_name)
    sup_data = get_supplier_data('suppliers.json')

    with connection.cursor() as cursor:
        for data in sup_data:
            for product in data['products']:
                cursor.execute(
                    "UPDATE products SET supplier_id = %s WHERE product_name = %s",
                    (sup_data.index(data) + 1, product)
                )

    connection.commit()
    connection.close()
