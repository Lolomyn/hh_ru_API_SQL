from src.config import config
from src.db_manager import DBManagerPostgres, HeadHunterAPI
from src.utils import (
    get_all_vacancies,
    get_companies_and_vacancies_count,
    get_vacancies_with_higher_salary,
    get_vacancies_with_keyword,
)

hh_api = HeadHunterAPI()
params = config()

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


def main():
    vacancies = []
    for employer in employers:
        vacancies.extend(hh_api.get_vacancies(employer["id"]))

    db_name = input("Введите имя для базы данных: ")
    db_manager = DBManagerPostgres(params)

    db_manager.create_database(db_name, params)
    db_manager.create_tables()
    db_manager.save_employers_to_db(employers)
    db_manager.save_vacancies_to_db(vacancies)

    print("\nКомпании и количество вакансий:")
    companies_and_vacancies_count = db_manager.get_companies_and_vacancies_count()
    get_companies_and_vacancies_count(companies_and_vacancies_count)

    print(
        """\nВыберите что Вас интересует:
    - Все вакансии (1)
    - Средняя зарплата по вакансиям (2)
    - Вакансии, где зарплата выше средней (3)
    - Вакансии по ключевому слову (4)
    """
    )

    choice = int(input("Введите значение от 1 до 4: "))
    match choice:
        case 1:
            all_vacancies = db_manager.get_all_vacancies()
            get_all_vacancies(all_vacancies)
        case 2:
            print(db_manager.get_avg_salary())
        case 3:
            vacancies_with_higher_salary = db_manager.get_vacancies_with_higher_salary()
            get_vacancies_with_higher_salary(vacancies_with_higher_salary)
        case 4:
            keyword = input("Укажите ключевое слово: ")
            vacancies_with_keyword = db_manager.get_vacancies_with_keyword(keyword)
            get_vacancies_with_keyword(vacancies_with_keyword)
        case _:
            print("Некорректный выбор")


if __name__ == "__main__":
    main()
