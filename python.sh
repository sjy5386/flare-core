#!/bin/bash

pip install -r requirements.txt

gunicorn --bind=0.0.0.0:8000 base.wsgi
