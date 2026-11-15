#!/usr/bin/env bash
# Выход при ошибке
set -o errexit

# Установка зависимостей
pip install -r requirements.txt

# Сбор статических файлов
python manage.py collectstatic --no-input

# Применение миграций к базе данных
python manage.py migrate

# Создание администратора (|| true нужно, чтобы ошибка "already taken" не ломала сборку)
export DJANGO_SUPERUSER_PASSWORD="admin12345"
python manage.py createsuperuser --noinput --username admin --email admin@example.com || true