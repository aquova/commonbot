FROM python:alpine

ENV DISCORD_PY_SHA=69b4d9a4fae44bef5414c5846f6e0c4712c1fda5
ENV COMMONBOT_VER=2.0.0b1

RUN apk update && apk add \
    build-base \
    git \
    sqlite

RUN pip3 install mypy

COPY setup.py /tmp
COPY commonbot /tmp/commonbot
RUN git clone https://github.com/Rapptz/discord.py /tmp/discord.py

WORKDIR /tmp/discord.py
RUN git checkout $DISCORD_PY_SHA
RUN pip3 install -U .

WORKDIR /tmp
RUN python3 setup.py bdist_wheel
RUN pip3 install dist/commonbot-$COMMONBOT_VER-py3-none-any.whl
