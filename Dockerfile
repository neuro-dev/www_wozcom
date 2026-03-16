FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 443

# Запускаем через Gunicorn (production-сервер)
# --bind 0.0.0.0 — слушать все интерфейсы
# --workers 2 — количество процессов
# --timeout 120 — таймаут
# --capture-output — логирование
# --reload — автоперезагрузка при изменениях (для разработки)

CMD ["gunicorn", "--certfile=woz_cert.pem", "--keyfile=woz_key.pem", "--bind", "0.0.0.0:443", "--capture-output", "app:app"]