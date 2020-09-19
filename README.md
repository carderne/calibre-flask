# calibre-flask
Simple Flask server for Calibre ebook library

## Setup

Must create a symlink called `data` within the `./static/` directory, that points to your Calibre ebook library. Example:
```bash
ln -s ~/Documents/Calibre/ ./static/data
```

Install requirements:
```bash
pip install -r requirements.txt
```

## Development
Run app in development mode:
```bash
FLASK_DEBUG=1 FLASK_RUN_PORT=5010 FLASK_APP=app.py flask run
```

## Serving
Serve with gunicorn:
```bash
gunicorn app:app
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

