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

## Nginx config
```
server {
    listen 80;
    server_name server_name_here;
    access_log /var/log/nginx/access.log;

    location / {
        proxy_pass http://127.0.0.1:8000;
    }

    location /resized/ {
        root /path/to/app/resized;
        expires max;
        add_header Cache-Control "public";
    }
}
```

## systemctl
[source](https://docs.gunicorn.org/en/stable/deploy.html)

Create `/etc/systemd/system/gunicorn.service`:
```
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
Type=notify
User=someuser
Group=someuser
RuntimeDirectory=gunicorn
WorkingDirectory=/home/someuser/applicationroot
ExecStart=/home/someuser/flask-app/venv/bin/gunicorn app.app:app
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true

# add this to serve under a subdirectory
# eg mydomain.com/books
Environment="SCRIPT_NAME=/books"

[Install]
WantedBy=multi-user.target
```

And `/etc/systemd/system/gunicorn.socket`:
```
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock
User=www-data

[Install]
WantedBy=sockets.target
```

And:
```
sudo systemctl enable --now gunicorn.socket
```

In nginx conf, change `proxy_pass` to:
```
proxy_pass http://unix:/run/gunicorn.sock;
include proxy_params;
```
