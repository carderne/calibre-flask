# calibre-flask
Simple Flask server for Calibre ebook library

Must create a symlink called `data` within the `./static/` directory, that points to your Calibre ebook library. Example:
```bash
ln -s ~/Documents/Calibre/ ./static/data
```

Run with:
```bash
FLASK_DEBUG=1 FLASK_RUN_PORT=5010 FLASK_APP=app.py flask run
```
