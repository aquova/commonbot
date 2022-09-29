FROM python:alpine

ARG COMMONBOT_VER=2.0.0.3

RUN apk update && apk add \
    build-base \
    git \
    sqlite

RUN pip3 install pylint

COPY setup.py /tmp
COPY commonbot /tmp/commonbot
WORKDIR /tmp
RUN python3 setup.py bdist_wheel
RUN pip3 install dist/commonbot-$COMMONBOT_VER-py3-none-any.whl
