import json
import os

from classes.abstract_classes.abstract_saver import VacanciesSaver


class JSONSaver(VacanciesSaver):
    """
    Класс для работы с json файлами
    """

    def __init__(self, filename):
        """
        Инициализатор класса JSONSaver
        :param filename: имя json файла
        directory: директория где будет храниться json файл
        """
        self.filename = filename
        self.directory = os.path.join('json_data')
        self.path_to_json = os.path.join(self.directory, self.filename)

    def save_vacancies_to_json(self, list_vacancies):
        """
        Сохраняет вакансии в json файл
        :param list_vacancies: список вакансий
        """
        if not os.path.exists(self.directory):
            os.mkdir(self.directory)
        try:
            with open(self.path_to_json, 'w', encoding='utf-8') as file:
                json.dump(list_vacancies, file, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f'Ошибка записи в файл {e}')

    def load_vacancies(self):
        """
        Загружает вакансии из json файла
        :return: список вакансий
        """
        try:
            with open(self.path_to_json, 'r') as file:
                vacancies = json.load(file)
                return vacancies
        except FileNotFoundError:
            raise FileNotFoundError('Файл не найден')

    def get_instances_from_json(self, class_name):
        """
        Преобразует словарь из json файла в экземпляр класса
        :param class_name: имя класса
        :return: список экземпляров класса
        """
        vacancies = self.load_vacancies()
        instances = [class_name(vacancy) for vacancy in vacancies]
        return instances

    def clear_json(self):
        """
        Очищает json файл
        """
        with open(self.path_to_json, 'w') as file:
            file.write(json.dumps({}))
        print('Данные по вакансиям удалены из json файла')
