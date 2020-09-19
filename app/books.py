from pathlib import Path
from xml.etree import ElementTree as ET
import sqlite3

from bs4 import BeautifulSoup

root = Path("app/static/data")
db = root / "metadata.db"


def get_books():
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
            path = root / book[4]
            try:
                description = (
                    ET.parse(path / "metadata.opf")
                    .getroot()[0]
                    .find("{http://purl.org/dc/elements/1.1/}description")
                    .text
                )
            except AttributeError:
                description = ""
            description = BeautifulSoup(description, "html.parser").get_text()
            books.append(
                {
                    "id": idd,
                    "title": book[1],
                    "sort": book[2],
                    "author": authors[link[idd]],
                    "authorSort": book[3],
                    "description": description,
                    "cover": str(path / "cover.jpg"),
                    "hasCover": book[5],
                    "lastModified": book[6],
                    "file": str(path / data[idd]),
                }
            )

    cursor.close()
    return books