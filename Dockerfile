# pull official base image
FROM python:3.9.6-alpine

# set working directory
WORKDIR /usr/src/BB

# set environment variable
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# run pscopg2 dependencies
# RUN apk update \
#     && apk add postgresql-dev gcc python3-dev musl-dev

# install dependecies
# RUN pip install --upgrade pip
# COPY ./requirements.txt .
# RUN pip install -r requirements.txt

# copy project
COPY . .

# start server
CMD python manage.py runserver
