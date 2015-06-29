# docker-guestbook

## Docker Docker Docker

1. Install Docker 1.7.0
1. Install Docker Compose 1.3.0
1. Install Docker Machine 0.3.0

## Local

```
docker-machine create --driver virtualbox gb-dev
eval "$(docker-machine env gb-dev)"
docker-compose -f docker-compose-dev.yml up -d
```

## Remote

```
docker-machine create --driver rackspace gb-prod
eval "$(docker-machine env gb-prod)"
docker-compose -f docker-compose-prod.yml up -d
```

## Initialize the Database

```
docker exec -it dockerguestbook_app_1 python app.py create_db
docker exec -it dockerguestbook_app_1 python app.py create_test_data
```
