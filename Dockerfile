FROM python:2.7.13

RUN mkdir /app
WORKDIR /app

ADD . ./
