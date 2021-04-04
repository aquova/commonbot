FROM python:alpine

RUN apk update && apk add \
    build-base \
    git \
    sqlite

ADD requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt
