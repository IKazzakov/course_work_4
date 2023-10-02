import os

import requests

from classes.abstract_classes.abstract_api import AbstractAPI


class SuperJobAPI(AbstractAPI):
    """Класс для работы с API Super Job"""
    API_vacancies_url = 'https://api.superjob.ru/2.0/vacancies/'
    API_KEY = os.getenv('API_TOKEN_SJ')

    def __init__(self, num_vacancies=20, search_query='Python', area='Москва'):
        """
        Инициализатор экземпляров класса для работы с API
        :param num_vacancies: количество вакансий на странице, по умолчанию 20
        :param search_query: текст запроса для поиска вакансий, по умолчанию Python
        :param area: название страны, региона или города для поиска, по умолчанию Москва
        page: страница поиска, по умолчанию = 0
        query_parameters: словарь с параметрами запроса
        """
        self.page = 0
        self.per_page = num_vacancies
        self.text = search_query
        self.area = area

        self.query_parameters = {
            'page': self.page,
            'count': self.per_page,
            'keywords': self.text,
            'town': self.area
        }

    def get_vacancies_by_api(self):
        """Получает вакансии через API"""
        headers = {'X-Api-App-Id': self.API_KEY}
        response = requests.get(self.API_vacancies_url, headers=headers, params=self.query_parameters)
        if response.status_code == 200:
            response_json = response.json()
            vacancies = response_json['objects']
            list_vacancies = self.select_vacancy_parameters(vacancies)
            print(f'Получено {len(list_vacancies)} вакансий с платформы Super Job')
            return list_vacancies
        print(f'Ошибка {response.status_code} выполнения запроса')
        return []

    @staticmethod
    def select_vacancy_parameters(vacancies_data):
        """
        Выборка определенных параметров вакансии
        :param vacancies_data: список вакансий полученных через API
        :return: список вакансий по указанным параметрам
        """
        vacancies_by_parameters = []
        for vacancy in vacancies_data:
            vacancy_name = vacancy.get('profession')
            vacancy_city = vacancy.get('town')['title']
            salary_from = vacancy.get('payment_from')
            salary_to = vacancy.get('payment_to')
            if not salary_from:
                salary_from = salary_to
            if not salary_to:
                salary_to = salary_from
            currency = vacancy.get('currency')
            vacancy_requirement = vacancy.get('candidat')
            vacancy_url = vacancy.get('link')

            vacancy_card = {
                'vacancy_name': vacancy_name,
                'vacancy_city': vacancy_city,
                'salary_from': salary_from,
                'salary_to': salary_to,
                'currency': currency,
                'vacancy_requirement': vacancy_requirement,
                'vacancy_url': vacancy_url
            }
            vacancies_by_parameters.append(vacancy_card)
        return vacancies_by_parameters
