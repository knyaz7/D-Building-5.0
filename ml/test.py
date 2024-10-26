def extract_tasks_from_text(text, selected_numbers):
    # Проверяем, есть ли текст, если нет - возвращаем пустой список
    if not text:
        return []

    # Извлекаем все задачи из текста
    tasks = [line.replace("TASK: ", "").strip() for line in text.strip().split('\n') if "TASK:" in line]

    # Преобразуем введённые номера в список целых чисел, исключаем пустые или нечисловые значения
    try:
        numbers = [int(num) for num in selected_numbers.split() if num.isdigit()]
    except ValueError:
        return []

    # Получаем задачи, соответствующие введённым номерам
    selected_tasks = [tasks[i - 1] for i in numbers if 1 <= i <= len(tasks)]

    return selected_tasks



text = """
Ваш рейтинг: 8

 Ваши задачи были разбиты на более мелкие
1. TASK: Проверить документацию на соответствие требованиям.
2. TASK: Внести окончательные правки в документ.
3. TASK: Подготовить отчет об изменениях в документации.
4. TASK: Получить обратную связь от заинтересованных сторон.
5. TASK: Завершить оформление документации для публикации.
6. TASK: Подготовить материал для презентации функции учета расходов. 
7. TASK: Проверить качество оформления документа.
8. TASK: Убедиться в наличии всех необходимых подписей/одобрений.

 Напишите номера задач через пробел, которые вы хотите делегировать
"""

selected_numbers = "1 4"

# Вызов функции
selected_tasks = extract_tasks_from_text(text, selected_numbers)

# Вывод результатов
print("Задачи делегированы:")
for task in selected_tasks:
    print(task)