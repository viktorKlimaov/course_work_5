import requests


# Функция для requests запроса, и получения компаний
def get_company():
    id_companies = [
        78638, 1942330, 2748, 49357, 2180, 1740, 87021, 3529, 23427, 52951
    ]
    companies = []
    for id_company in id_companies:
        url = f'https://api.hh.ru/employers/{id_company}'
        headers = {'User-Agent': 'HH-User-Agent'}
        params = {'page': 10, 'per_page': 100, 'locale': 'RU', 'only_with_vacancies': 'true'}

        response = requests.get(url, headers=headers, params=params)
        company = response.json()
        companies.append(company)

    return companies


# Функция для получения списка из компаний и их вакансий
def get_vacancies(companies: list[dict]):
    data = []
    for company in companies[0:10]:
        vacancies_url = company.get('vacancies_url')
        response = requests.get(vacancies_url)
        vacancies = response.json()['items']

        list_vacancy = []
        for vacancy in vacancies:
            list_vacancy.append(vacancy)

        data.append({
            'company': company,
            'vacancy': list_vacancy
        })
    return data
