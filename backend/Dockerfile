# Используем базовый образ Python 3.12.5-slim
FROM python:3.12.5-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл с зависимостями
COPY pyproject.toml requirements.lock requirements-ml.lock ./

# Устанавливаем зависимости
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.lock && \
    pip install --no-cache-dir -r requirements-ml.lock

# Копируем все остальные файлы в рабочую директорию
COPY . .

# Запускаем Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
