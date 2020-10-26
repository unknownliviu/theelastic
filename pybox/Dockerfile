FROM python:3.8-alpine

RUN mkdir /app
WORKDIR /app

RUN apk add tzdata curl
ENV TZ 'Europe/Bucharest'

COPY ./requirements.txt /app
RUN pip3 install -r requirements.txt
