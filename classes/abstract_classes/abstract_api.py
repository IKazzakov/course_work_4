from abc import ABC, abstractmethod


class AbstractAPI(ABC):
    """Абстрактный класс для работы с API сайтов"""
    @abstractmethod
    def get_vacancies_by_api(self):
        """Получает список вакансий по API"""
        pass

    @staticmethod
    @abstractmethod
    def selection_vacancy_parameters(vacancies_data):
        """Выборка определенных параметров вакансии.
        Возвращает список вакансий с этими параметрами"""
        pass

