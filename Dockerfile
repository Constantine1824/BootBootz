# syntax = docker/dockerfile:1.2

# pull official base image
FROM python:3.10.4-alpine

RUN --mount=type=secret,id=_env,dst=/etc/secrets/.env cat /etc/secrets/.env

# set working directory
WORKDIR /BB

# set environment variable
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Args
ARG username
ARG password
ARG SECRET_KEY
ARG DEBUG
ARG DATABASE_URL


ENV username=$username
ENV password=$password

# copy project
COPY . /BB/

# run psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# install dependecies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

#Expose
EXPOSE 8000

#Collect static files and migrate
RUN python manage.py collectstatic --noinput
RUN python manage.py makemigrations
RUN python manage.py migrate

RUN echo "This is the username: $username"
#Create Superuser
RUN python manage.py createsuperuser --username $username --password $password

#Start service
CMD ["waitress-serve", "--port=8000", "BB.wsgi:application"]
