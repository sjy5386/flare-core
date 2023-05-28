#!/bin/bash

pip install -r requirements.txt

python manage.py collectstatic

python manage.py test

gunicorn --bind=0.0.0.0:8000 base.wsgi
