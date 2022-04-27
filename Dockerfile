FROM python:alpine

RUN apk update && apk add \
    build-base \
    git \
    sqlite

RUN pip3 install mypy

COPY setup.py /tmp
COPY commonbot /tmp/commonbot
RUN git clone https://github.com/Rapptz/discord.py /tmp/discord.py
RUN pip3 install -U /tmp/discord.py
RUN python3 /tmp/setup.py bdist_wheel
RUN pip3 install /tmp/dist/commonbot-2.0.0b1-py3-none-any.whl
