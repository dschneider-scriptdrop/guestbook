# docker-guestbook

## Docker Docker Docker

1. [Docker](https://docs.docker.com/installation/) 1.7.0
1. [Docker Machine](https://docs.docker.com/machine/#installation) 0.3.0
1. [Docker Compose](https://docs.docker.com/compose/install/) 1.3.0

# Local

## Initialize the Environment

```
docker-machine create --driver virtualbox guestbook-dev
eval "$(docker-machine env guestbook-dev)"
docker-compose -f docker-compose-dev.yml up -d
```

## Initialize the Database

```
docker-compose -f docker-compose-dev.yml run --rm --no-deps app python app.py create_db
docker-compose -f docker-compose-dev.yml run --rm --no-deps app python app.py create_dummy_data
```

# Remote

## Initialize the Environment

```
docker-machine create --driver rackspace guestbook-prod
eval "$(docker-machine env guestbook-prod)"
docker-compose -f docker-compose-prod.yml build
docker-compose -f docker-compose-prod.yml up -d
```

## Security

```
docker-machine ssh guestbook-prod "apt-get update"
docker-machine ssh guestbook-prod "ufw default deny"
docker-machine ssh guestbook-prod "ufw allow ssh"
docker-machine ssh guestbook-prod "ufw allow http"
docker-machine ssh guestbook-prod "ufw allow https"
docker-machine ssh guestbook-prod "ufw allow 2376"
docker-machine ssh guestbook-prod "ufw --force enable"
docker-machine ssh guestbook-prod "apt-get -y install fail2ban"
```

## Initialize the Database

```
docker-compose -f docker-compose-prod.yml run --rm --no-deps app python app.py create_db
docker-compose -f docker-compose-prod.yml run --rm --no-deps app python app.py create_dummy_data
```

## Deploy Changes to Remote

```
docker-compose -f docker-compose-prod.yml build
docker-compose -f docker-compose-prod.yml up -d --x-smart-recreate
```

## Work with the Database

```
docker run --rm --link dockerguestbook_db_1:db mysql:5.7 sh -c \
  'exec mysql \
  --host=$DB_PORT_3306_TCP_ADDR \
  --user=root \
  --password=$DB_ENV_MYSQL_ROOT_PASSWORD \
  --database=$DB_ENV_MYSQL_DATABASE \
  --execute="show tables;" \
  --table'

docker run --rm --link dockerguestbook_db_1:db mysql:5.7 sh -c \
  'exec mysqldump \
  --host=$DB_PORT_3306_TCP_ADDR \
  --user=root \
  --password=$DB_ENV_MYSQL_ROOT_PASSWORD \ 
  --databases $DB_ENV_MYSQL_DATABASE \
  --single-transaction \
  --add-drop-database' > $DB_ENV_MYSQL_DATABASE.sql
```

## Alias

```
alias de='env | grep DOCKER_'
```