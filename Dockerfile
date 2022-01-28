FROM python:alpine

RUN apk update && apk add \
    build-base \
    git \
    sqlite

RUN pip3 install mypy

COPY setup.py /tmp
COPY commonbot /tmp/commonbot
RUN python3 /tmp/setup.py bdist_wheel
RUN pip3 install /tmp/dist/commonbot-1.7.3.2-py3-none-any.whl
