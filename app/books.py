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

    sql = """
    SELECT books.id, books.title, books.sort, authors.name, books.author_sort,
        books.path, data.name, data.format, books.has_cover, books.timestamp
    FROM books
    INNER JOIN books_authors_link ON books.id=books_authors_link.book
    INNER JOIN authors ON books_authors_link.author=authors.id
    INNER JOIN data ON books.id=data.book
    WHERE data.format IN ('MOBI', 'AZW', 'AZW3', 'PDF')
    GROUP BY books.id
    """
    cursor.execute(sql)
    books = cursor.fetchall()
    cursor.close()

    book_list = []
    for book in books:
        try:
            description = (
                ET.parse(data_dir / book[5] / "metadata.opf")
                .getroot()[0]
                .find("{http://purl.org/dc/elements/1.1/}description")
                .text
            )
            description = BeautifulSoup(description, "html.parser").get_text()
        except AttributeError:
            description = ""

        has_cover = book[8]
        book_file = f"/data/{book[5]}/{book[6]}.{book[7].lower()}"
        cover_to_resize = (
            f"data/{book[5]}/cover.jpg" if has_cover else "static/cover.jpg"
        )
        cover = resize(cover_to_resize, "400x600", fill=True)
        cover_small = resize(cover_to_resize, "100x150", fill=True)

        book_list.append(
            {
                "id": book[0],
                "title": book[1],
                "sort": book[2],
                "author": book[3],
                "authorSort": book[4],
                "description": description,
                "cover": cover,
                "coverSmall": cover_small,
                "added": book[9].split(" ")[0],
                "file": book_file,
            }
        )

    book_list = sorted(book_list, key=lambda x: x["authorSort"])
    return book_list
