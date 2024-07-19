import psycopg2


# Функция для cоздания базы данных и таблиц для сохранения данных
def create_database(database: str, params: dict):
    conn = psycopg2.connect(**params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE {database}")
    cur.execute(f"CREATE DATABASE {database}")

    conn.close()

    conn = psycopg2.connect(dbname=database, **params)
    with conn.cursor() as cur:
        # создание таблицы companies
        cur.execute("""
        CREATE TABLE IF NOT EXISTS companies(
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            url_company TEXT NOT NULL,
            open_vacancies int NOT NULL
            );
        """)

        # создание таблицы companies
        cur.execute("""
        CREATE TABLE IF NOT EXISTS vacancies(
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            salary_from int,
            salary_to int,
            company_id SERIAL REFERENCES companies(id),
            url_vacancy TEXT NOT NULL, 
            description TEXT
            );
        """)

    conn.commit()
    conn.close()


# Функция для записи компаний и их вакансий в базу данных
def save_data_to_database(data, database_name: str, params: dict):
    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for items in data:
            company_dict = items['company']

            # заполняем таблицу companies
            cur.execute(
                """
                INSERT INTO companies (id, name, url_company, open_vacancies)
                VALUES (%s, %s, %s, %s)
                RETURNING id
                """,
                (company_dict['id'], company_dict['name'], company_dict['alternate_url'], company_dict['open_vacancies']))

            company_id = cur.fetchone()[0]
            vacancy_dict = items['vacancy']
            for vacancy in vacancy_dict:
                salary = vacancy.get('salary')

                # валидация зарплаты
                try:
                    salary_from = salary.get('from')
                except Exception:
                    salary_from = 0
                else:
                    salary_from = salary_from or 0

                try:
                    salary_to = salary.get('to')
                except Exception:
                    salary_to = 0
                else:
                    salary_to = salary_to or 0

                # заполняем таблицу vacancies
                cur.execute(
                    """
                    INSERT INTO vacancies (id, name, salary_from, salary_to, url_vacancy, description, company_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (vacancy['id'], vacancy['name'], salary_from, salary_to,
                     vacancy['alternate_url'], vacancy.get('snippet').get('requirement'), company_id))

    conn.commit()
    conn.close()
