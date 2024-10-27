from g4f.client import Client
import g4f.Provider
import re


async def evaluate_employees(employees, task, required_stack):
    """
    Оценивает сотрудников по заданной задаче и возвращает ранжированный список по рекомендациям.

    :param employees: Список сотрудников, где каждый сотрудник представлен как словарь с ключами:
                      'fullname', 'position', 'description', 'stack', 'rating'.
    :param task: Задача, по которой проводится оценка.
    :param required_stack: Стек технологий, необходимый для выполнения задачи.
    :return: Отсортированный список сотрудников по убыванию оценки выполнения задачи.
    """
    client = Client()
    evaluations = []

    for employee in employees:
        # Фильтрация сотрудников по требуемому стеку технологий
        if not set(required_stack).issubset(set(employee['stack'])):
            continue  # Пропускаем, если стек технологий не соответствует

        fullname = employee['fullname']
        position = employee['position']
        description = employee['description']
        rating = employee['rating']

        # Формирование запроса на оценку задачи
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{
                "role": "user",
                "content": f"Поставь рейтинг человека от 1 до 10, насколько сотрудник подходит для задачи: {task}.  {position} - {fullname}. Описание сотрудника: {description}. Рейтинг выполненности задач: {rating}. Пиши только число от 1 до 10."
            }],
            provider=g4f.Provider.Ai4Chat
        )

        # Получение текста ответа от модели
        result = response.choices[0].message.content.strip()
        print(f"Результат от модели для {fullname}: {result}")

        # Поиск числовой оценки выполнения задачи с помощью регулярного выражения
        match = re.search(r'\b(10|[1-9])\b', result)
        if match:
            res = int(match.group(1))  # Сохранение найденного значения оценки
        else:
            res = 0  # Если оценка не найдена, устанавливаем 0

        # Добавляем информацию о сотруднике и его оценке в список
        evaluations.append({
            'fullname': fullname,
            'position': position,
            'res': res,
        })

    # Сортировка сотрудников по убыванию рейтинга
    sorted_evaluations = sorted(evaluations, key=lambda x: x['res'], reverse=True)

    return sorted_evaluations  # Возвращение отсортированного списка сотрудников


# # Пример использования функции
# employees = [
#     {
#         'FIO': 'Иванов И.И.',
#         'job_title': 'Разработчик',
#         'description': 'Разработчик с опытом работы в Django, специализируется на создании серверных API и оптимизации производительности. Недавно завершил проект по разработке функционала системы отчетности, осталось внести правки по UI.',
#         "rating": 6,
#         'stack': ['Python', 'Django']  # Пример стека технологий
#     },
#     {
#         'FIO': 'Петров П.П.',
#         'job_title': 'Тестировщик',
#         'description': 'Проводит тестирование на Java и Selenium, выявляет критические баги. Ответственный за автоматизированное тестирование API и фронтенда. В настоящее время занимается отловом багов в новом релизе системы.',
#         "rating": 8,
#         'stack': ['Java', 'Selenium']
#     },
#     {
#         'FIO': 'Сидоров С.С.',
#         'job_title': 'Менеджер',
#         'description': 'Менеджер проектов с навыками организации рабочих процессов, контроля сроков и качества. Все задачи выполняются в срок и соответствуют ожиданиям заказчика. Имеет опыт работы с кросс-функциональными командами.',
#         "rating": 5,
#         'stack': ['Управление проектами', 'Коммуникации']
#     },
#     {
#         'FIO': 'Александров А.А.',
#         'job_title': 'Разработчик',
#         'description': 'Специализируется на Flask и интеграции с API внешних сервисов. В текущем проекте отвечает за интеграцию с платёжной системой и создание безопасных методов обработки данных.',
#         "rating": 2,
#         'stack': ['Python', 'Flask']
#     }
# ]


# task = "Завершить разработку нового функционала."
# required_stack = ['Python']  # Необходимый стек технологий для задачи

# Вызов функции
# ranked_employees = evaluate_employees(employees, task, required_stack)

# # Вывод результатов
# for employee in ranked_employees:
#     print(f"{employee['FIO']} - Рейтинг: {employee['res']} ")
