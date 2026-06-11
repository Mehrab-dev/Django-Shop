FROM python:3.11-slim

LABEL maintainer="programmer.py.mail@gmail.com"

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

COPY ./requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY ./core .

EXPOSE 8000