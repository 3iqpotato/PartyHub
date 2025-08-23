# Dockerfile
FROM python:3.12-slim

# Работна директория в контейнера
WORKDIR /app

# Инсталираме системни зависимости (за psycopg2, Pillow и др.)
RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Копираме requirements
COPY requirements.txt .

# Инсталираме Python зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копираме целия проект (в dev ще монтираме volume и това няма да пречи)
COPY . .

# Стартираме сървъра
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
