release: python manage.py migrate --no-input
web: gunicorn --chdir TimeEstim TimeEstim.wsgi:application --log-file -