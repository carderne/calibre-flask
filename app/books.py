from pathlib import Path
from xml.etree import ElementTree as ET
import sqlite3

from bs4 import BeautifulSoup
import flask_resize

resize = flask_resize.make_resizer(
    flask_resize.configuration.Config(url="", root="app", target_directory="resized")
)


def get_books():
    data_dir = Path("app/data/")
    db = data_dir / "metadata.db"
    con = sqlite3.connect(db)
    cursor = con.cursor()

    cursor.execute(
        "SELECT book, name, format FROM data "
        "WHERE format IN ('MOBI', 'AZW', 'AZW3', 'PDF')"
    )
    data = {x[0]: f"{x[1]}.{x[2].lower()}" for x in cursor.fetchall()}

    cursor.execute("SELECT id, name FROM authors")
    authors = {x[0]: x[1] for x in cursor.fetchall()}

    cursor.execute("SELECT book, author FROM books_authors_link")
    link = {x[0]: x[1] for x in cursor.fetchall()}

    cursor.execute(
        "SELECT id, title, sort, author_sort, path, has_cover, last_modified FROM books"
    )
    books = []
    for book in cursor.fetchall():
        idd = book[0]
        if idd in data:
            try:
                description = (
                    ET.parse(data_dir / book[4] / "metadata.opf")
                    .getroot()[0]
                    .find("{http://purl.org/dc/elements/1.1/}description")
                    .text
                )
                description = BeautifulSoup(description, "html.parser").get_text()
            except AttributeError:
                description = ""

            has_cover = book[5]
            book_file = f"data/{book[4]}/{data[idd]}"
            cover_to_resize = f"data/{book[4]}/cover.jpg"
            cover = resize(cover_to_resize, "400x600") if has_cover else ""
            cover_small = resize(cover_to_resize, "100x150") if has_cover else ""

            books.append(
                {
                    "id": idd,
                    "title": book[1],
                    "sort": book[2],
                    "author": authors[link[idd]],
                    "authorSort": book[3],
                    "description": description,
                    "cover": cover,
                    "coverSmall": cover_small,
                    "hasCover": has_cover,
                    "lastModified": book[6],
                    "file": book_file,
                }
            )

    cursor.close()
    return books
