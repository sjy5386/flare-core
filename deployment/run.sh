#!/bin/bash

bash ./deployment/build.sh
bash ./deployment/test.sh

gunicorn --bind=0.0.0.0:8000 base.wsgi
