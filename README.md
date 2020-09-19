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

## Configuration
Need to create a `./secrets` file like this:
```
export FLASK_SECRET_KEY=makeyourownsecretkeyhere
```

Next need to create a user file. Use `werkzeug` to create hashed passwords:
```python
from werkzeug.security import generate_password_hash
generate_password_hash("your-unhashed-password", "sha256")
```

Store the output for each password in a users file `./users.yaml`:
```
user1: "hashedpassword"
user2: "anotherhashedpassword"
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

