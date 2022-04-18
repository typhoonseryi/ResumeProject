python manage.py collectstatic --noinput
python manage.py migrate
python manage.py createsuperuser --noinput || true
gunicorn config.wsgi:application -b :8000