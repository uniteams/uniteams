release: cd api && python manage.py migrate && python manage.py runserver 0.0.0.0:5000
api: cd api && gunicorn api.wsgi
web: nuxt start
