from src.config import config
from src.db_manager import DBManager


# Функция для взаимодействия с пользователем
def user_interaction():
    print('Для получения списка всех компаний и количества вакансий у каждой компании, введите 1')
    print('Для получения списка всех вакансий с названием компании, названием вакансии,'
          'зарплаты и ссылки на вакансию, введите 2')
    print('Для получения средней зарплаты по всем вакансиям, введите 3')
    print("Для получения списка всех вакансий, у которых зарплата выше средней по всем вакансиям, введите 4")
    print("Для получения списка всех вакансий, в названии которых содержатся введенное вами слово, введите 5")
    try:
        user_input = int(input('Ведите выбранный вами вариант: '))
        if user_input not in [1, 2, 3, 4, 5]:
            raise ValueError
    except ValueError:
        print('Такого варианта нет')
        return ValueError

    params = config()
    db = DBManager(**params, database='curs_work')

    if user_input == 1:
        list_company = db.get_companies_and_vacancies_count()
        for company in list_company:
            company_name, quantity_vacancy = company
            print()
            print(f'Компания: {company_name}\nКоличество вакансий: {quantity_vacancy}')

    elif user_input == 2:
        list_company = db.get_all_vacancies()
        for company in list_company:
            companies_name, vacancies_name, salary_from, salary_to, url_vacancy = company
            print()
            print(f'Компания: {companies_name}\nВакансия: {vacancies_name}\nЗарплата: от {salary_from} до {salary_to}\n'
                  f'Ссылка на вакансию: {url_vacancy}')

    elif user_input == 3:
        list_company = db.get_avg_salary()
        for company in list_company:
            print(int(company[0]))

    elif user_input == 4:
        list_company = db.get_vacancies_with_higher_salary()
        for company in list_company:
            vacancy_id, name, salary_from, salary_to, company_id, url_vacancy, description = company
            print()
            print(f'id вакансии: {vacancy_id}\nВакансия: {name}\nЗарплата: от {salary_from}, до {salary_to}\n'
                  f'id компании: {company_id}\nСсылка на вакансию: {url_vacancy}\nОписание вакансии: {description}')

    elif user_input == 5:
        word_user = input("Введите слово: ")
        list_company = db.get_vacancies_with_keyword(word_user)
        for company in list_company:
            vacancy_id, name, salary_from, salary_to, company_id, url_vacancy, description = company
            print()
            print(f'id вакансии: {vacancy_id}\nВакансия: {name}\nЗарплата: от {salary_from}, до {salary_to}\n'
                  f'id компании: {company_id}\nСсылка на вакансию: {url_vacancy}\nОписание вакансии: {description}')
