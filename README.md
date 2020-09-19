# calibre-flask
Simple Flask server for Calibre ebook library.

## Setup
Clone the repo:
```bash
git clone https://github.com/carderne/calibre-flask
```

Create a symlink called `data` within the `./static/` directory, that points to your Calibre ebook library (that contains `metadata.db`).
```bash
cd calibre-flask
ln -s ~/path/to/calibre/library/ ./app/static/data
```

Install requirements:
```bash
pip install -r requirements.txt
```

## Configuration
Create a `./secrets` file containing a secret key for Flask to use for encryption.
```
echo export FLASK_SECRET_KEY=$(python3 -c 'import secrets; \
    print(secrets.token_urlsafe(16))') > secrets
```

Next create a `users.yaml` to control authentication. This scripts outputs usernames with hashed passwords.
```bash
./create_user.py
# and follow the prompts
```

## Development
Run app in development mode:
```bash
source ./secrets
FLASK_DEBUG=1 FLASK_RUN_PORT=5010 FLASK_APP=app/app.py flask run
```

## Serving
Serve with gunicorn:
```bash
gunicorn app.app:app
```

## Nginx config
```
client_header_buffer_size 50000k;
large_client_header_buffers 16 50000k;
client_max_body_size 200m;

server {
    listen 80;
    server_name 35.240.48.205;

    location / {
        proxy_pass http://127.0.0.1:8000;
    }
}
```

