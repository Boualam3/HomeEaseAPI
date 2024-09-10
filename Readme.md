# Quick Start Guide

## Prerequisites

Ensure you have the following installed on your machine:

- [Docker](https://www.docker.com/get-started) (for running the app in a containerized environment)
- [Docker Compose](https://docs.docker.com/compose/install/) (for managing multi-container Docker applications)

```bash
docker --version
```

similar output :

`Docker version 24.0.7, .....`

---

```bash
docker-compose --version
```

similar output :

`docker-compose version 1.29.2 .....`

## Running the Application

### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone  git@github.com:Boualam3/HomeEaseAPI.git

cd HomeEaseAPI/

git checkout properties_app
```

### 2. Build and Run the Docker Container

To build and run the Docker container, use Docker Compose. This command will build the image and start the container:

```bash
docker-compose up --build
```

hit ctrl+C to exit from docker logs

### 3. Running Migrations

If you need to apply database migrations, run the following commands:
-1 run :

```bash
docker-compose run web python manage.py makemigrations
```

-2 then run:

```bash
docker-compose run web python manage.py migrate
```

-3 populate database with dummy data

```
docker-compose run web python manage.py seed_db
```

### 3. Access the Application

Once the container is running, tou can use credentials of created users to get access key via curl or swagger ui

- Host user

```curl
curl -X 'POST' \
  'http://localhost:8000/auth/jwt/create/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'X-CSRFTOKEN: oxW5uy4mcIsBWfX9viSy8brwshuPa2aYq2Y2HO2Jrgf7WmDeuDpyWQYMR0YOu4ZT' \
  -d '{
  "username": "host_user",
  "password": "hostpasskey123"
}'
```

or Guest user

```curl
curl -X 'POST' \
  'http://localhost:8000/auth/jwt/create/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'X-CSRFTOKEN: oxW5uy4mcIsBWfX9viSy8brwshuPa2aYq2Y2HO2Jrgf7WmDeuDpyWQYMR0YOu4ZT' \
  -d '{
  "username": "guest_user",
  "password": "guestpasskey123"
}'
```

or create your own user by following the documentation here :

> Development Server: [localhost] (http://localhost:8000)
> SMTP Development Server: [smtp-server](http://localhost:5000)
> API Documentation (Swagger UI): [Swagger] (http://localhost:8000/api/docs/swagger/)
> API Documentation (ReDoc): [ReDoc] (http://localhost:8000/api/docs/redoc/)

### 5. Creating a Superuser

To create a superuser for accessing the Django admin interface:

```bash
docker-compose run web python manage.py createsuperuser
```

### 6. Stopping the Application

To stop the running Docker containers:

```bash
docker-compose down
```

Development Tips

    Code Changes: Changes to the codebase will be reflected immediately if you have set up volume mappings in Docker.

    Logs: To view logs from your running containers, use:

```bash
docker-compose logs
```
