FROM python:alpine

RUN apk update && apk add \
    build-base

ADD requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt
