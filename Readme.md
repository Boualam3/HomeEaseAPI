# Quick Start Guide

## Prerequisites

Ensure you have the following installed on your machine:

- [Docker](https://www.docker.com/get-started) (for running the app in a containerized environment)
- [Docker Compose](https://docs.docker.com/compose/install/) (for managing multi-container Docker applications)

`docker --version`
output:

```
Docker version 24.0.7, .....
```

---

`docker-compose --version`
output

```
docker-compose version 1.29.2 .....
```

## Running the Application

### 1. Clone the Repository

First, clone the repository to your local machine:

```
git clone  git@github.com:Boualam3/HomeEaseAPI.git

cd HomeEaseAPI/

git checkout master
```

### 2. Build and Run the Docker Container

To build and run the Docker container, use Docker Compose. This command will build the image and start the container:

`docker-compose up --build`
hit ctrl+C to exit from docker logs

### 3. Access the Application

Once the container is running, you can access the application at:

    Development Server: http://localhost:8000
    API Documentation (Swagger UI): http://localhost:8000/api/docs/swagger/
    API Documentation (ReDoc): http://localhost:8000/api/docs/redoc/

### 4. Running Migrations

If you need to apply database migrations, run the following command:

`docker-compose run web python manage.py migrate`

### 5. Creating a Superuser

To create a superuser for accessing the Django admin interface:

`docker-compose run web python manage.py createsuperuser`

### 6. Stopping the Application

To stop the running Docker containers:

`docker-compose down`

Development Tips

    Code Changes: Changes to the codebase will be reflected immediately if you have set up volume mappings in Docker.

    Logs: To view logs from your running containers, use:

`docker-compose logs`
