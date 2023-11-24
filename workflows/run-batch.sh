#!/bin/bash

bash ./workflows/build.sh
bash ./workflows/test.sh

python manage.py runserver
