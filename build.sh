#!/bin/bash

pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('uszek', 'uszek619@gmail.com', 'Mati1906!') if not User.objects.filter(username='admin').exists() else None"
