#!/bin/bash

pip install -r requirements.txt

if [ -d ./static ]
then
  rm -rf ./static
fi
python manage.py collectstatic
