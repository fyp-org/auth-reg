FROM python:3.10

WORKDIR /app

# Копируем зависимости
COPY reg-zareg/requirements.txt /app/requirements.txt

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY reg-zareg /app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
