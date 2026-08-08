#!/bin/bash

pip freeze | xargs pip uninstall -y
pip install ".[prod]"

if [ -d ./out/static ]
then
  rm -rf ./out/static/*
fi
python manage.py collectstatic
