# Используем официальный легковесный образ Python
FROM python:3.10-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файл зависимостей и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь исходный код проекта
COPY . .

# Открываем порт для Streamlit дашборда
EXPOSE 8501

# Команда по умолчанию (будет переопределена в docker-compose)
CMD ["python3","-m", "src.main"]