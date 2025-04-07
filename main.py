from src.config import config
from src.db_manager import DBManagerPostgres, HeadHunterAPI

hh_api = HeadHunterAPI()
params = config()

if __name__ == "__main__":

    employer_ids = [
        78638,  # Т-БАНК
        9498112,  # Яндекс.Крауд
        3529,  # СБЕР
        6111353,  # SWOYO
        2180,  # OZON
        3776,  # МТС
        15478,  # VK
        1993194,  # YADRO
        6093775,  # ASTON
        80,  # ALFA-BANK
        3707941,  # Цитадель
    ]

    employers = hh_api.get_employers(employer_ids)

    vacancies = []
    for employer in employers:
        vacancies.extend(hh_api.get_vacancies(employer["id"]))

    db_name = input("Введите имя для базы данных: ")
    db_manager = DBManagerPostgres(params)

    db_manager.create_database(db_name, params)
    db_manager.create_tables()
    db_manager.save_employers_to_db(employers)
    db_manager.save_vacancies_to_db(vacancies)

    # Примеры запросов
    print("Компании и количество вакансий:")
    print(db_manager.get_companies_and_vacancies_count())

    print("\nВсе вакансии:")
    print(db_manager.get_all_vacancies())

    print("\nСредняя зарплата по вакансиям:")
    print(db_manager.get_avg_salary())

    print("\nВакансии, где зарплата выше средней:")
    print(db_manager.get_vacancies_with_higher_salary())

    print("\nВакансии по ключевому слову 'Python':")
    print(db_manager.get_vacancies_with_keyword("Python"))
