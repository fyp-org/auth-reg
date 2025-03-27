FROM python:3.10

# Установка рабочей директории внутри контейнера
WORKDIR /app

# Копируем файл .env из корня проекта
COPY .env /app/

# Копируем файл зависимостей из папки reg-zareg/.requirements
COPY reg-zareg/requirements.txt /app/requirements.txt

# Обновляем pip и устанавливаем зависимости
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Копируем исходный код приложения из папки reg-zareg в контейнер
COPY reg-zareg /app

# Открываем порт 8000 для доступа к приложению
EXPOSE 8000

# Команда для запуска приложения через uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]