from g4f.client import Client
import g4f.Provider
import re


def evaluate_task(FIO, job_title, message, task):
    # Создание клиента для общения с моделью GPT-4 через указанный провайдер
    client = Client()

    # Формирование запроса на оценку задачи
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user",
                   "content": f"Ты team lead. По задаче {task}. Ты общаешься с подчиненым {FIO} - {job_title}. По сообщению, выяви по 10-бальной шкале, на сколько выполнена задача. Дай ответ строго следующего вида: Задача выполнена на (1-10), (разбей невыполненную часть {task} на мелкие подзадачи и напиши их со следующей строчки, строго пронумеровав начиная с единицы). Сообщение сотрудника: {message}."}],
        provider=g4f.Provider.Ai4Chat
    )

    # Получение текста ответа от модели
    result = response.choices[0].message.content

    # Поиск числовой оценки выполнения задачи с помощью регулярного выражения
    match = re.search(r'на\s+([1-9]|10)', result)
    if match:
        rating = match.group(1)  # Сохранение найденного значения оценки
    else:
        print("Оценка выполнения задачи не найдена.")

    # Регулярное выражение для поиска подзадач: берет текст между точкой/запятой и до следующей запятой
    pattern = r'(?<=\.|,)\s*([A-Za-zА-Яа-яЁёЁ][^,]*)'

    # Применение регулярного выражения для поиска всех подзадач в ответе
    matches = re.findall(pattern, result)

    # Создание списка для подзадач и фильтрация пустых строк
    subtasks = []
    for match in matches:
        subtasks.extend(filter(None, match.splitlines()))  # Удаление пустых строк и добавление подзадач в список

    return rating, subtasks  # Возвращение оценки выполнения и списка подзадач

