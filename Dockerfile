FROM python:slim-buster

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY app app

ENV PORT 8000
EXPOSE $PORT

# ENTRYPOINT gunicorn app.app:app --bind 0.0.0.0:$PORT
ENTRYPOINT BOOKS_PREFIX=/books FLASK_DEBUG=1 FLASK_APP=app/app.py flask run -h 0.0.0.0 -p $PORT
