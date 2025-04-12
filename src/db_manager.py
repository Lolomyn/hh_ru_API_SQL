from abc import ABC, abstractmethod
from typing import Any

import psycopg2
import requests
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


class DBManager(ABC):
    """Абстрактный класс для работы с данными о вакансиях"""

    @abstractmethod
    def get_companies_and_vacancies_count(self) -> list[Any]:
        """Получает список всех компаний и количество вакансий у каждой"""
        pass

    @abstractmethod
    def get_all_vacancies(self) -> list[Any]:
        """Получает список всех вакансий"""
        pass

    @abstractmethod
    def get_avg_salary(self) -> list[Any]:
        """Получает среднюю зарплату по вакансиям"""
        pass

    @abstractmethod
    def get_vacancies_with_higher_salary(self) -> list[Any]:
        """Получает список вакансий с зарплатой выше средней"""
        pass

    @abstractmethod
    def get_vacancies_with_keyword(self, keyword: str) -> list[Any]:
        """Получает список вакансий по ключевому слову"""
        pass


class HeadHunterAPI:
    """Класс для работы с API HeadHunter"""

    def __init__(self) -> None:
        self.base_url = "https://api.hh.ru"
        self.headers = {"User-Agent": "HH-User-Agent"}

    def get_employers(self, employer_ids: list[int]) -> list[dict]:
        """Получает информацию о работодателях по их ID"""
        employers = []

        for employer_id in employer_ids:
            url = f"{self.base_url}/employers/{employer_id}"
            response = requests.get(url, headers=self.headers)

            if response.status_code == 200:
                employers.append(response.json())

        return employers

    def get_vacancies(self, employer_id: int) -> Any:
        """Получает вакансии работодателя по его ID"""
        url = f"{self.base_url}/vacancies"
        params = {"employer_id": employer_id, "per_page": 100}

        response = requests.get(url, params=params, headers=self.headers)

        if response.status_code == 200:
            return response.json().get("items", [])

        return []


class DBManagerPostgres(DBManager):
    """Класс для работы с базой данных PostgreSQL"""

    def __init__(self, params: dict):
        self.conn = psycopg2.connect(dbname="postgres", **params)

        self.cur = self.conn.cursor()

    def __del__(self) -> None:
        self.cur.close()
        self.conn.close()

    def create_database(self, db_name: str, params: dict) -> None:
        """Создает базу данных с полученным именем"""
        self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        self.cur.execute(f"DROP DATABASE IF EXISTS {db_name}")
        self.cur.execute(f"CREATE DATABASE {db_name}")

        self.cur.close()
        self.conn.close()

        self.conn = psycopg2.connect(dbname=db_name, **params)
        self.cur = self.conn.cursor()

    def create_tables(self) -> None:
        """Создает таблицы в базе данных"""
        self.cur.execute(
            """
                CREATE TABLE IF NOT EXISTS employers (
                    employer_id serial PRIMARY KEY,
                    name varchar(255) NOT NULL,
                    url varchar(255),
                    description text,
                    open_vacancies integer
                )
            """
        )

        self.cur.execute(
            """
                CREATE TABLE IF NOT EXISTS vacancies (
                    vacancy_id serial PRIMARY KEY,
                    employer_id integer REFERENCES employers(employer_id),
                    title varchar(255) NOT NULL,
                    salary_from integer,
                    salary_to integer,
                    currency varchar(10),
                    url varchar(255),
                    requirement text
                )
            """
        )
        self.conn.commit()

    def save_employers_to_db(self, employers: list[dict]) -> None:
        """Сохраняет работодателей в базу данных"""
        for employer in employers:
            self.cur.execute(
                """
                    INSERT INTO employers (employer_id, name, url, description, open_vacancies)
                    VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    employer["id"],
                    employer["name"],
                    employer["alternate_url"],
                    employer.get("description", ""),
                    employer.get("open_vacancies", 0),
                ),
            )
        self.conn.commit()

    def save_vacancies_to_db(self, vacancies: list[dict]) -> None:
        """Сохраняет вакансии в базу данных"""
        for vacancy in vacancies:
            salary = vacancy.get("salary")
            self.cur.execute(
                """
                    INSERT INTO vacancies (
                        vacancy_id, employer_id, title, salary_from,
                        salary_to, currency, url, requirement
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    vacancy["id"],
                    vacancy["employer"]["id"],
                    vacancy["name"],
                    salary["from"] if salary else None,
                    salary["to"] if salary else None,
                    salary["currency"] if salary else None,
                    vacancy["alternate_url"],
                    vacancy.get("snippet", {}).get("requirement", ""),
                ),
            )
        self.conn.commit()

    def get_companies_and_vacancies_count(self) -> Any:
        """Получает список всех компаний и количество вакансий у каждой"""
        self.cur.execute(
            """
                SELECT name, COUNT(vacancy_id) as vacancies_count
                FROM employers
                LEFT JOIN vacancies USING(employer_id)
                GROUP BY name
                ORDER BY vacancies_count DESC
            """
        )
        return self.cur.fetchall()

    def get_all_vacancies(self) -> Any:
        """Получает список всех вакансий"""
        self.cur.execute(
            """
                SELECT employers.name, title, salary_from, salary_to, currency, vacancies.url
                FROM vacancies
                JOIN employers USING(employer_id)
            """
        )
        return self.cur.fetchall()

    def get_avg_salary(self) -> Any:
        """Получает среднюю зарплату по вакансиям"""
        self.cur.execute(
            """
                SELECT AVG((salary_from + salary_to) / 2) as avg_salary
                FROM vacancies
                WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL
            """
        )
        return round(self.cur.fetchone()[0], 2)

    def get_vacancies_with_higher_salary(self) -> Any:
        """Получает список вакансий с зарплатой выше средней"""
        avg_salary = self.get_avg_salary()
        self.cur.execute(
            """
                SELECT employers.name, title, (salary_from + salary_to) / 2 as salary, currency, vacancies.url
                FROM vacancies
                JOIN employers USING(employer_id)
                WHERE (salary_from + salary_to) / 2 > %s
                ORDER BY salary DESC
            """,
            (avg_salary,),
        )
        return self.cur.fetchall()

    def get_vacancies_with_keyword(self, keyword: str) -> Any:
        """Получает список вакансий по ключевому слову"""
        self.cur.execute(
            """
                SELECT employers.name, title, salary_from, salary_to, currency, vacancies.url
                FROM vacancies
                JOIN employers USING(employer_id)
                WHERE title LIKE %s OR requirement LIKE %s
            """,
            (f"%{keyword}%", f"%{keyword}%"),
        )
        return self.cur.fetchall()
