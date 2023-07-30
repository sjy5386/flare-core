#!/bin/bash

bash ./deployment/build.sh

python manage.py test

gunicorn --bind=0.0.0.0:8000 base.wsgi
