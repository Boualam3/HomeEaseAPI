FROM python:3.10-slim

# set environment variables for python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set working directory in container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/


RUN pip install --no-cache-dir -r requirements.txt


COPY . /app/


EXPOSE 8000


CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
