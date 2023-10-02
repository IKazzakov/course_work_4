from classes.hh_api import HeadHunterAPI
from classes.sj_api import SuperJobAPI


def get_vacancy_parsing(json_instance):
    """
    Выполняет поиск вакансий на выбранной пользователем платформе и записывает результат в json файл
    :param json_instance: экземпляр класса JSONSaver
    """
    print('Необходимо указать данные для поиска вакансий')
    text_query = input('Ведите базовый запрос (например: "Python developer"): ')
    area_query = input('Ведите страну, регион или город: ')
    vacancy_amount = input('Введите какое количество вакансий необходимо найти с каждого сайта (не более 100): ')
    vacancy_amount = validate_vacancy_amount(vacancy_amount)

    # Создаем экземпляры классов HeadHunterAPI, SuperJobAPI
    hh_instance = HeadHunterAPI(num_vacancies=vacancy_amount, search_query=text_query, area=area_query)
    sj_instance = SuperJobAPI(num_vacancies=vacancy_amount, search_query=text_query, area=area_query)
    hh_sj_instances = [hh_instance, sj_instance]

    # Выбор платформы
    user_platform_choice = get_user_platform_choice()

    # Получаем данные через api и записываем их в json файл
    if user_platform_choice == 0:
        hh_vacancies_list = hh_instance.get_vacancies_by_api()
        json_instance.save_vacancies_to_json(hh_vacancies_list)
    elif user_platform_choice == 1:
        sj_vacancies_list = sj_instance.get_vacancies_by_api()
        json_instance.save_vacancies_to_json(sj_vacancies_list)
    elif user_platform_choice == 2:
        hh_sj_vacancies_list = []
        for platform_instance in hh_sj_instances:
            platform_vacancies_list = platform_instance.get_vacancies_by_api()
            hh_sj_vacancies_list += platform_vacancies_list
        json_instance.save_vacancies_to_json(hh_sj_vacancies_list)
    print(f'Данные по вакансиям записаны в файл {json_instance.filename}', end='\n')


def validate_vacancy_amount(vacancy_amount):
    """
    Проверяет корректность введенного значения количества вакансий
    :param vacancy_amount: количество вакансий
    :return: количество вакансий
    """
    try:
        vacancy_amount = int(vacancy_amount)
        if vacancy_amount <= 0 or vacancy_amount > 100:
            print('Неверный формат ввода. Установлено значение в 20 вакансий')
            vacancy_amount = 20
    except ValueError:
        print('Неверный формат ввода. Установлено значение в 20 вакансий')
        vacancy_amount = 20
    return vacancy_amount


def get_user_platform_choice():
    """
    Выбор платформы для поиска вакансий
    :return: значение, указывающее платформу
    """
    print("С каких платформ необходимо загрузить вакансии: 0 - Head Hunter, 1 - SuperJob, 2 - с обоих платформ: ")
    try:
        user_platform_choice = int(input(''))
    except ValueError:
        print('Неверный формат ввода. Поиск вакансий будет осуществляться с обоих платформ')
        user_platform_choice = 2
    return user_platform_choice


def get_filtered_vacancies_and_save(vacancy_manage, top_vacancies):
    """
    Отбор вакансий по ключевым словам.
    Вывод вакансий на экран или запись их в файл.
    :param vacancy_manage: Экземпляр класса VacancyManage
    :param top_vacancies: список топ вакансий
    """
    print('Если хотите отсортировать вакансии по ключевым словам введите "1", для выхода нажмите "Enter": ')
    user_choice = input('')
    if user_choice == '1':
        print('Введите ключевые слова для отбора вакансий: ')
        user_keywords = input('').split()
        if user_keywords:
            vacancies_by_keywords = vacancy_manage.get_vacancies_by_key_word(user_keywords, top_vacancies)
            if vacancies_by_keywords:
                print(f'Отобрано {len(vacancies_by_keywords)} вакансий')
                while True:
                    print('Выберите действие: 0 - показать вакансии, 1 - сохранить в файл, 2 - выйти: ', end='\n')
                    choice = input('')
                    if choice == '0':
                        for vacancy in vacancies_by_keywords:
                            print(vacancy)
                    elif choice == '1':
                        save_vacancies_to_file(vacancy_manage, vacancies_by_keywords)
                        break
                    elif choice == '2':
                        exit(0)
                    else:
                        print('Неверный формат ввода, попробуйте еще раз')
            else:
                print('Вакансий по заданным ключевым словам не найдено')
        else:
            print('Ключевые слова не введены')
    print('Записать топ вакансий в файл?: 1 - да, "Enter" - выйти')
    user_answer = input('')
    if user_answer == '1':
        save_vacancies_to_file(vacancy_manage, top_vacancies)


def save_vacancies_to_file(vacancy_manage, vacancies_list):
    filename = input('Введите название файла для сохранения вакансий: ')
    if filename == '':
        filename = 'vacancies'
    while True:
        print('Выберите формат файла для сохранения вакансий: 1 - excel, 2 - csv')
        user_choice = input('')
        if user_choice == '1':
            filename += '.xlsx'
            vacancy_manage.save_to_excel(filename, vacancies_list)
            break
        elif user_choice == '2':
            filename += '.csv'
            vacancy_manage.save_to_csv(filename, vacancies_list)
            break
        else:
            print('Неверный формат ввода, попробуйте еще раз')
