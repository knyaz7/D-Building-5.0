from pyrogram import Client, filters
from evaluate_task import evaluate_task
import speech_recognition as sr
from pydub import AudioSegment
import asyncio

# Замените значениями вашего API_ID и API_HASH
API_ID = "24081739"
API_HASH = "8bbd21a1b4be67a4084d2c4ddd3194a9"

app = Client("TaskManagerAI", api_id=API_ID, api_hash=API_HASH)


async def create_chat_and_send_message(username, task, unfulfilled_list_point, count_day):
    # Добавляем метку "TASK:" к каждой задаче для более надежного поиска в тексте
    unfulfilled_formatted = "\n".join([f"TASK: {item}" for item in unfulfilled_list_point])

    user = await app.get_users(username)
    user_id = user.id

    await app.send_message(
        user_id,
        f"Привет!\n\n"
        f"🔔 *Напоминание по задаче*: **{task}**\n"
        f"⏳ Сроки подходят к концу, осталось **{count_day}** дней.\n\n"
        f"**Незавершенные подзадачи**:\n"
        f"{unfulfilled_formatted}\n\n"
        f"📋 Ответь одним сообщением о текущем прогрессе:\n"
        f"— Что уже выполнено?\n"
        f"— Какие шаги остаются до завершения?\n\n"
        f"Спасибо! 😊"
    )


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


@app.on_message(filters.private)
async def print_bot_responses(client, message):
    print(message)
    username = "Bebrbulinka"  # Это должно соответствовать пользователю, с которым мы работаем
    task = "Завершить финализацию документации по требованиям для новой функции учета расходов."
    user = await app.get_users(username)
    user_id = user.id
    formatted_history, history = await get_chat_history(client, user_id)
    last_message = history[0]  # Последнее сообщение в истории

    if message.chat.username == username:
        if last_message.text and last_message.text.replace(" ", "").isdigit():
            extract_tasks = extract_tasks_from_text(history[1].text, last_message.text)
            extract_tasks_formatted = "\n".join([f"{i + 1}. TASK: {item}" for i, item in enumerate(extract_tasks)])
            await client.send_message(message.chat.id, f"Задачи делегированы:\n\n"
                                                       f"{extract_tasks_formatted}\n\n")
            print(extract_tasks)
            print(extract_tasks_formatted)
            print(history[1])
            print(last_message)

        else:
            rating, subtasks = evaluate_task("Петров Петр Петрович", "Системный аналитик", message.text, task)

            subtasks_formatted = "\n".join([f"{i + 1}. TASK: {item}" for i, item in enumerate(subtasks)])

            await client.send_message(message.chat.id, f"Ваш рейтинг: {rating}\n\n"
            f" **Ваши задачи были разбиты на более мелкие**\n"
            f"{subtasks_formatted}\n\n"
            f" **Напишите номера задач через пробел, которые вы хотите делегировать**\n")



async def get_chat_history(client, chat_id, limit=5):
    history = []
    async for message in client.get_chat_history(chat_id, limit=limit):
        history.append(message)
    # Форматируем историю сообщений
    formatted_history = []
    for msg in history:
        sender_name = "Assistant" if msg.from_user and msg.from_user.is_self else (
            msg.from_user.first_name if msg.from_user else 'Unknown')
        role = "assistant" if sender_name == "Assistant" else "user"
        content = ""
        if msg.text:
            content = msg.text
        elif msg.voice:
            audio_file = await msg.download()
            wav_file = audio_file.replace(".ogg", ".wav")
            AudioSegment.from_ogg(audio_file).export(wav_file, format="wav")
            with sr.AudioFile(wav_file) as source:
                audio_data = recognizer.record(source)
                try:
                    content = recognizer.recognize_google(audio_data, language="ru-RU")
                except sr.UnknownValueError:
                    content = "Audio not recognized"
                except sr.RequestError as e:
                    content = f"Could not request results; {e}"
            os.remove(audio_file)  # Удаляем загруженный аудиофайл после обработки
            os.remove(wav_file)  # Удаляем конвертированный аудиофайл после обработки
        formatted_history.append({"role": role, "content": content})
    return formatted_history, history


async def main():
    unfulfilled_list_point = [
        "Сделать",
        "Запушить",
        "Протестировать",
        "Проинформировать"
    ]
    username = "Bebrbulinka"
    await app.start()
    await create_chat_and_send_message(username,
                                       "Сделать дизайн сайта.",
                                       unfulfilled_list_point, 4)
    await asyncio.Event().wait()  # Используем Event для ожидания событий


if __name__ == "__main__":
    app.run(main())
