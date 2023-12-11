#!/bin/bash

pip freeze | xargs pip uninstall -y
pip install -r requirements.txt

python manage.py runapscheduler
