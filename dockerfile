FROM python:3.10

WORKDIR /app

# Используем аргументы для передачи переменных
ARG DATABASE_URL
ARG KEY_REGLOG

# Делаем переменные доступными внутри контейнера
ENV DATABASE_URL=${DATABASE_URL}
ENV KEY_REGLOG=${KEY_REGLOG}

# Копируем зависимости
COPY reg-zareg/requirements.txt /app/requirements.txt

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY reg-zareg /app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
