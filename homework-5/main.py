from database import DataBase
from utils import *


def main():
    db_name = input('Введите название базы данных: ')

    data_base = DataBase(db_name)
    create_supplier_table(db_name)
    add_foreign_key(db_name)
    add_supplier_in_products(db_name)


if __name__ == '__main__':
    main()
