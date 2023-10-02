import requests

from classes.abstract_classes.abstract_api import AbstractAPI


class HeadHunterAPI(AbstractAPI):
    """Класс для работы с API Head Hunter"""
    API_vacancies_url = 'https://api.hh.ru/vacancies/'
    API_areas_url = 'https://api.hh.ru/areas/'

    def __init__(self, num_vacancies=20, search_query='Python', area='Москва'):
        """
        Инициализатор экземпляров класса для работы с API
        :param num_vacancies: количество вакансий на странице, по умолчанию 20
        :param search_query: текст запроса для поиска вакансий, по умолчанию Python
        :param area: название страны, региона или города для поиска, по умолчанию Москва
        verify_area: проверка региона/города. Если регион/город не найден устанавливается значение "Россия"
        page: страница поиска, по умолчанию = 0
        query_parameters: словарь с параметрами запроса
        """
        self.page = 0
        self.per_page = num_vacancies
        self.text = search_query
        self.area = self.verify_area(area)

        self.query_parameters = {
            'page': self.page,
            'per_page': self.per_page,
            'text': self.text,
            'area': self.area
        }

    def get_vacancies_by_api(self):
        """Получает вакансии через API"""
        response = requests.get(self.API_vacancies_url, params=self.query_parameters)
        if response.status_code == 200:
            response_json = response.json()
            vacancies = response_json['items']
            list_vacancies = self.select_vacancy_parameters(vacancies)
            print(f'Получено {len(list_vacancies)} вакансий с платформы Head Hunter')
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
            vacancy_name = vacancy.get('name')
            vacancy_city = vacancy.get('area')['name']
            vacancy_salary = vacancy.get('salary')
            if not vacancy_salary:
                salary_from = salary_to = 0
                currency = ''
            else:
                salary_from = vacancy_salary['from']
                salary_to = vacancy_salary['to']
                if not salary_from:
                    salary_from = salary_to
                if not salary_to:
                    salary_to = salary_from
                currency = vacancy_salary['currency']
            vacancy_requirement = vacancy.get('snippet')['requirement']
            vacancy_url = vacancy.get('url')

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

    def verify_area(self, area):
        """
        Проверка введенных параметров
        :param area: название страны, региона или города для поиска
        :return:
        """
        location_id = self.get_location_id(area, self.get_areas())
        if not location_id:
            print('Такой страны, региона или города нет в базе данных. Установлено значение "Россия"')
            return '113'
        else:
            return location_id

    def get_areas(self):
        """
        Получаем список со всеми регионами через API
        :return: список с регионами
        """
        response = requests.get(self.API_areas_url)
        response_json = response.json()
        return response_json

    def get_location_id(self, location, areas):
        """
        Рекурсивная функция для получения id страны, региона или города
        :param location: название страны, региона или города
        :param areas: список со всеми регионами
        :return: id страны, региона или города
        """
        for area in areas:
            if area['name'].lower() == location.lower():
                return area['id']
            recursive = self.get_location_id(location, area['areas'])
            if recursive:
                return recursive
        return None
