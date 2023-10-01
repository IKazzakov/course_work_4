import csv
import operator
import os

import openpyxl

from classes.vacancy import Vacancy


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
            for value in vacancy.__dict__.values():
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
                number_of_top = 3
                print('Неверный формат ввода. Установлено значение в топ 3 вакансии')
        except ValueError:
            number_of_top = 3
            print('Неверный формат ввода. Установлено значение в топ 3 вакансии')

        top_vacancies = sort_vacancies[:number_of_top]
        print(*top_vacancies, sep='\n')
        return top_vacancies

    def save_to_csv(self, filename, list_vacancies):
        """
        Сохраняет вакансии в csv файл
        :param filename: имя файла
        :param list_vacancies: список вакансий
        """
        # Создаем директорию для сохранения вакансий
        directory = self.create_directory()
        path = os.path.join(directory, filename)
        try:
            with open(path, 'w', newline='', encoding='utf-8') as file:
                fieldnames = [
                    'vacancy_name', 'vacancy_city', 'salary_from',
                    'salary_to', 'currency', 'vacancy_requirement', 'vacancy_url'
                ]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows([vacancy.__dict__ for vacancy in list_vacancies])
                print(f'Данные по вакансиям записаны в файл {filename}')
        except Exception as e:
            print(f'Ошибка записи в файл {e}')

    def save_to_excel(self, filename, list_vacancies):
        """
        Сохраняет вакансии в excel файл
        :param filename: имя файла
        :param list_vacancies: список вакансий
        """
        # Создаем директорию для сохранения вакансий
        directory = self.create_directory()
        path = os.path.join(directory, filename)
        try:
            book = openpyxl.Workbook()
            sheet = book.active
            headers = list(list_vacancies[0].__dict__.keys())
            sheet.append(headers)
            for vacancy in list_vacancies:
                row = list(vacancy.__dict__.values())
                sheet.append(row)
            book.save(path)
            print(f'Данные по вакансиям записаны в файл {filename}')
        except Exception as e:
            print(f'Ошибка записи в файл {e}')

    @staticmethod
    def create_directory():
        """
        Создает директорию для сохранения вакансий
        :return: имя директории
        """
        directory_name = 'user_data'
        directory_path = os.path.join(directory_name)
        if not os.path.exists(directory_path):
            os.mkdir(directory_path)
        return directory_name
