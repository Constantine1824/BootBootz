# syntax = docker/dockerfile:1.2

# pull official base image
FROM python:3.9.6-alpine

# set working directory
WORKDIR /BB

# set environment variable
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

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

#Get environment variables at build time
RUN --mount=type=secret,id=_env,dst=/etc/secrets/.env cat /etc/secrets/.env
#Collect static files and migrate
RUN python manage.py collectstatic --noinput
#Get environment variables at build time
RUN --mount=type=secret,id=_env,dst=/etc/secrets/.env cat /etc/secrets/.env
RUN python manage.py makemigrations
#Get environment variables at build time
RUN --mount=type=secret,id=_env,dst=/etc/secrets/.env cat /etc/secrets/.env
RUN python manage.py migrate

#Get environment variables at build time
RUN --mount=type=secret,id=_env,dst=/etc/secrets/.env cat /etc/secrets/.env
# start server
CMD ["gunicorn", "--bind", "0.0.0.0.8000", "BB.wsgi:application"]
