FROM python:3.12-slim-bookworm

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY app app

ENV PORT 8000
EXPOSE $PORT

ENTRYPOINT BOOKS_PREFIX=/books gunicorn app.app:app --bind 0.0.0.0:$PORT
