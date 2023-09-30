from classes.vacancy import Vacancy
import operator
import os
import csv


class VacancyManage(Vacancy):
    def __init__(self, vacancies_list: list):
        """
        Инициализатор класса VacancyManage
        :param vacancies_list: список экземпляров класса Vacancy
        """
        self.vacancies_list = vacancies_list

    def sort_vacancies_by_salary_from(self):
        """
        Сортировка вакансий по начальной ставке зарплаты от большей к меньшей
        :return: отсортированный список вакансий
        """
        sort_vacancies = sorted(self.vacancies_list, key=operator.attrgetter('salary_from'), reverse=True)
        return sort_vacancies

    @staticmethod
    def get_vacancies_by_key_word(keywords, list_vacancies):
        """
        Поиск вакансий по ключевому слову
        :param list_vacancies: список вакансий
        :param keywords: текст для поиска
        :return: список вакансий, включающих в себя ключевые слова
        """
        vacancies_by_keywords = []
        for vacancy in list_vacancies:
            for key, value in vacancy.__dict__.items():
                if any(keyword.lower() in str(value).lower() for keyword in keywords):
                    vacancies_by_keywords.append(vacancy)
                    break
        return vacancies_by_keywords

    def get_top_vacancies_by_salary(self):
        """
        Выводит топ N вакансий по зарплате
        :return: список топ вакансий по зарплате
        """
        sort_vacancies = self.sort_vacancies_by_salary_from()
        try:
            number_of_top = int(
                input(f'Введите число от 1 до {len(sort_vacancies)} для вывода топ вакансий по зарплате: '))
            if number_of_top < 1 or number_of_top > len(sort_vacancies):
                print('Неверный формат ввода. Установлено значение в топ 3 вакансии')
                number_of_top = 3
        except ValueError:
            print('Неверный формат ввода. Установлено значение в топ 3 вакансии')
            number_of_top = 3

        top_vacancies = sort_vacancies[0:number_of_top]
        for vacancy in top_vacancies:
            print(vacancy)
        return top_vacancies

    def save_to_csv(self, filename, list_vacancies):
        directory = os.path.join('user_data')
        filename += '.csv'
        path = os.path.join(directory, filename)
        if not os.path.exists(directory):
            os.mkdir(directory)
        try:
            with open(path, 'w', newline='', encoding='utf-8') as file:
                fieldnames = ['vacancy_name', 'vacancy_city', 'salary_from',
                              'salary_to', 'currency', 'vacancy_requirement', 'vacancy_url']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for vacancy in list_vacancies:
                    writer.writerow(vacancy.__dict__)
                f'Данные по вакансиям записаны в файл {filename}'
        except Exception as e:
            print(f'Ошибка записи в файл {e}')
