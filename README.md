# Flare Core

Free **sub**domains and **short** URLs

## Installation

### Register your domain

You must have your domain to run this project.

### Install Docker

1. [Install Docker](https://docs.docker.com/engine/install/)
2. [Install Docker Compose](https://docs.docker.com/compose/install/)

### Clone this project

```shell
git clone https://github.com/sjy5386/flare-core
```

### Set environment

1. Copy `.env.sample`.

```shell
cp .env.sample .env
```

2. Edit `.env`.

```shell
nano .env
```

### Connect to the database

1. Copy `my.cnf.sample`.

```shell
cp my.cnf.sample my.cnf
```

2. Edit `my.cnf`.

```shell
nano my.cnf
```

[MySQLdb connection options](https://mysqlclient.readthedocs.io/user_guide.html#functions-and-attributes)

### Run

```shell
docker compose up
```

### Deploy

```shell
sh deploy.sh
```

### Migrate database

```shell
python manage.py migrate
```

### Create superuser

```shell
python manage.py createsuperuser
```

### Configure NGINX

1. Copy NGINX configuration file.

```shell
cp ./docker/nginx/sites-enabled/flare.conf <your-nginx-sites-enabled-directory>
```

2. Edit your NGINX configuration file.

```shell
nano <your-nginx-sites-enabled-directory>/flare.conf
```

* You can get static files from `./out/static`.

3. Reload NGINX.

```shell
nginx -s reload
```

## Usage

### Subdomains

1. You must have at least one contact created.
2. Search for available subdomain names.
3. Create a available subdomain.
4. Add dns records.
