class Vacancy:
    """Класс для работы с вакансиями"""
    def __init__(self, vacancy_card: dict):
        """
        Инициализируем экземпляр класса со следующими атрибутами
        vacancy_name: название вакансии
        vacancy_city: страна, регион, город
        salary_from: нижний уровень зарплаты
        salary_to: верхний уровень зарплаты
        currency: валюта зарплаты
        vacancy_requirement: требования к вакансии
        vacancy_url: ссылка на вакансию
        """
        self.vacancy_name = vacancy_card.get('vacancy_name')
        self.vacancy_city = vacancy_card.get('vacancy_city')
        self.salary_from = vacancy_card.get('salary_from')
        self.salary_to = vacancy_card.get('salary_to')
        self.currency = vacancy_card.get('currency')
        self.vacancy_requirement = vacancy_card.get('vacancy_requirement')
        self.vacancy_url = vacancy_card.get('vacancy_url')

    def __str__(self):
        """Строковое представление вакансии"""
        return (
            f'Название вакансии: {self.vacancy_name}\n'
            f'Страна, регион, город: {self.vacancy_city}\n'
            f'Нижний уровень зарплаты: {self.salary_from}\n'
            f'Верхний уровень зарплаты: {self.salary_to}\n'
            f'Валюта зарплаты: {self.currency}\n'
            f'Требования к вакансии: {self.vacancy_requirement}\n'
            f'Ссылка на вакансию: {self.vacancy_url}\n'
        )

