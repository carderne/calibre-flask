# syntax=docker/dockerfile:1

FROM python:slim-buster

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN echo 'LOGIN_DISABLED=True' > config.py

ENV PORT 8000
EXPOSE $PORT

ENTRYPOINT gunicorn app.app:app --bind 0.0.0.0:$PORT
