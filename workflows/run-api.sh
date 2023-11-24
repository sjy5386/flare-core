#!/bin/bash

bash ./workflows/build.sh
bash ./workflows/test.sh

gunicorn --bind=0.0.0.0:8000 base.wsgi
