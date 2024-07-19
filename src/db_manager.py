import psycopg2


class DBManager:
    """
    Класс для подключения к БД PostgreSQL и получения данных
    """
    def __init__(self, host, database, user, password, port):
        self.conn = psycopg2.connect(host=host, database=database, user=user, password=password, port=port)

    def get_companies_and_vacancies_count(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT companies.name, open_vacancies
                FROM companies;
            """)
            return cur.fetchall()

    def get_all_vacancies(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT companies.name, vacancies.name, vacancies.salary_from, vacancies.salary_to, vacancies.url_vacancy
                FROM vacancies
                JOIN companies ON vacancies.company_id = companies.id;
            """)
            return cur.fetchall()

    def get_avg_salary(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT AVG(salary_from)
                FROM vacancies;
            """)
            return cur.fetchall()

    def get_vacancies_with_higher_salary(self):
        cur = self.conn.cursor()
        cur.execute("""
            SELECT *
            FROM vacancies
            WHERE vacancies.salary_from > (SELECT AVG(salary_from) FROM vacancies);
        """)
        return cur.fetchall()

    def get_vacancies_with_keyword(self, word):
        cur = self.conn.cursor()
        cur.execute(f"""
            SELECT *
            FROM vacancies
            WHERE vacancies.name LIKE '%{word}%';
        """)
        return cur.fetchall()


