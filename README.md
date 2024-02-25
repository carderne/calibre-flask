# calibre-flask
Simple Flask server for Calibre ebook library.

## Setup
Clone the repo:
```
git clone https://github.com/carderne/calibre-flask
```

Create a symlink called `data` within the `static/` directory, that points to your Calibre ebook library (that contains `metadata.db`).
```
cd calibre-flask
ln -s ~/path/to/calibre/library/ ./app/data
```

Create a virtual env (if needed) and install requirements. Note: to run this in production (i.e., through `systemd` and `gunicorn`), these libraries might need to also be installed in the system Python, or somewhere where they're available...
```
python3 -m venv ./venv/
source ./venv/bin/activate
pip install -r requirements.txt
```

## Development
Run app in development mode:
```
FLASK_DEBUG=1 FLASK_APP=app/app.py flask run
```

## Serving
Serve with gunicorn:
```
gunicorn app.app:app
```

## Docker
Build:
```bash
docker build --tag carderne/calibre-flask .
```

Run:
```bash
docker run --name calibre-flask --rm \
  -p 8000:8000 \
  -v /path/to/books:/app/app/data \
  carderne/calibre-flask
```
