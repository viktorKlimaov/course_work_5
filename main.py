from src.api_hh import get_vacancies, get_company
from src.config import config
from src.user_interaction import user_interaction
from src.utils import create_database, save_data_to_database


def main():
    #  Получения списка из компаний и их вакансий
    data = get_vacancies(get_company())

    params = config()
    # Создание базы данных и таблиц
    create_database(params=params, database='curs_work')
    # Заполнение таблиц данными
    save_data_to_database(data=data, params=params, database_name='curs_work')

    user_interaction()


if __name__ == '__main__':
    main()