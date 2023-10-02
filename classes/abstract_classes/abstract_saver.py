from abc import ABC, abstractmethod


class VacanciesSaver(ABC):
    """
    Абстрактный класс для работы с json файлами
    """
    @abstractmethod
    def save_vacancies_to_json(self, vacancies):
        """
        Сохраняет вакансии в json файл
        :param vacancies: список вакансий
        """
        pass

    def load_vacancies(self):
        """
        Загружает вакансии из json файла
        :return: список вакансий
        """
        pass

    def get_instances_from_json(self, class_name):
        """
        Преобразует словарь из json файла в экземпляр класса
        :param class_name: имя класса
        :return:
        """
        pass

    def clear_json(self):
        """
        Очищает json файл
        """
        pass
