# Subshorts

Free **sub**domains and **short** URLs

## Available Providers

### Records (Subdomains)

* [DigitalOcean](https://docs.digitalocean.com/products/networking/dns/)
* [Vultr](https://www.vultr.com/docs/introduction-to-vultr-dns/)

### Short URLs

* [Bitly](https://bitly.com/pages/products/link-management)
* [Firebase Dynamic Links](https://firebase.google.com/products/dynamic-links)

## Installation

### Register your domain

You must have your domain to run this project.

### Prepare the provider

#### DigitalOcean

1. [Sign up](https://m.do.co/c/d31ac39bdd48) if you are not already registered.
2. Log in to your account.
3. Create new project. (Optional)
4. [Add your domain](https://docs.digitalocean.com/products/networking/dns/how-to/add-domains/).
5. Change name servers.
6. [Generate new **writable** token](https://docs.digitalocean.com/reference/api/create-personal-access-token/).

#### Firebase Dynamic Links

1. Sign in to your *Google* account.
2. Go to [*Firebase* console page](https://console.firebase.google.com/).
3. Add project.
4. Go to *Hosting* page. [Add your domain](https://firebase.google.com/docs/hosting/custom-domain).
5. Go to *Dynamic Links* page. [Add URL prefix](https://firebase.google.com/docs/dynamic-links/custom-domains).
6. Go to project settings page. Check your Web API Key.

### Install Docker

1. [Install Docker](https://docs.docker.com/engine/install/)
2. [Install Docker Compose](https://docs.docker.com/compose/install/)

### Clone this project

```shell
git clone https://github.com/sjy5386/subshorts
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
python manage.py makemigrations
python manage.py migrate
```

### Create superuser

```shell
python manage.py createsuperuser
```

## Usage

### Subdomains

1. You must have at least one contact created.
2. Search for available subdomain names.
3. Create a available subdomain.
4. Add records.

### Short URLs

1. Choose a domain.
2. Enter a name.
3. Enter a long URL.
4. Create a short URL.
