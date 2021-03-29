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

## Configuration
Create a `config.py` file containing a secret key for Flask to use for encryption.
```
./bin/make_config.py > config.py
```

If you want the website to work without a username/password (e.g. on a RPi firewalled from the internet) then add the following line to `config.py`:
```
LOGIN_DISABLED = True
```

Next create a `users.yaml` to control authentication. This scripts outputs usernames with hashed passwords.
```
./bin/create_user.py
# and follow the prompts
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
