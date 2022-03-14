FROM python:3.10

RUN apt update
RUN apt upgrade -y

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

RUN python manage.py makemigrations
RUN python manage.py migrate

EXPOSE 8000

ENTRYPOINT ["gunicorn", "--bind=0.0.0.0:8000", "base.wsgi"]