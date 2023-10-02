import user_interaction
from classes.json_saver import JSONSaver
from classes.vacancy import Vacancy
from classes.vacancy_manage import VacancyManage


def main():
    # Создаем экземпляр класса JSONSaver
    json_saver = JSONSaver('vacancies_json.json')
    # Вызываем функцию для поиска вакансий и их сохранения в json файл
    user_interaction.get_vacancy_parsing(json_saver)
    # Получаем список экземпляров класса Vacancy из json файла с вакансиями
    vacancies_from_json = json_saver.get_instances_from_json(Vacancy)
    # Создаем экземпляр класса VacancyManage
    vacancy_manage = VacancyManage(vacancies_from_json)
    # Вызываем функцию для вывода топ N вакансий по зарплате
    top_vacancies = vacancy_manage.get_top_vacancies_by_salary()
    # Вызываем функцию для поиска вакансий по ключевым словам и сохранения в csv/excel файл
    user_interaction.get_filtered_vacancies_and_save(vacancy_manage, top_vacancies)
    print('Программа завершена')
    json_saver.clear_json()


if __name__ == '__main__':
    main()
