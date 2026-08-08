#!/bin/bash

pip freeze | xargs pip uninstall -y
pip install ".[prod]"

python manage.py runapscheduler
