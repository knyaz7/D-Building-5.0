# Используем базовый образ Python 3.12.5-slim
FROM python:3.12.5-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл с зависимостями
COPY requirements.lock .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.lock

# Копируем все остальные файлы в рабочую директорию
COPY . .

# Запускаем Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
