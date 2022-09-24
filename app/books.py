import sqlite3
from pathlib import Path

import flask_resize  # type: ignore[import]
from bs4 import BeautifulSoup

resize = flask_resize.make_resizer(
    flask_resize.configuration.Config(url=".", root="app", target_directory="resized")
)


def get_books(lim: int = -1, search: str = "%") -> list[dict]:
    data_dir = Path("app/data/")
    db = data_dir / "metadata.db"
    con = sqlite3.connect(db)
    con.row_factory = sqlite3.Row
    cursor = con.cursor()

    if not search:
        search = "%"
    sql = f"""
    SELECT books.id AS id,
           books.title AS title,
           books.sort AS sort,
           authors.name AS author,
           books.author_sort AS authorSort,
           books.path AS path,
           data.name AS file,
           data.format AS format,
           books.timestamp AS added,
           comments.text AS comments
    FROM books
    INNER JOIN books_authors_link ON books.id=books_authors_link.book
    INNER JOIN authors ON books_authors_link.author=authors.id
    INNER JOIN data ON books.id=data.book
    LEFT JOIN comments ON books.id=comments.book
    WHERE data.format IN ('MOBI', 'AZW', 'AZW3', 'PDF')
      AND (authors.name LIKE '%{search}%'
           OR books.title LIKE '%{search}%'
           OR comments.text LIKE '%{search}%')
    GROUP BY books.id
    ORDER BY books.timestamp DESC
    LIMIT {lim}
    """

    cursor.execute(sql)
    books = [dict(b) for b in cursor.fetchall()]
    cursor.close()

    for b in books:
        cover = f"data/{b['path']}/cover.jpg"
        comments = ""
        if b["comments"]:
            comments = BeautifulSoup(b["comments"], "html.parser").get_text()
        b.update(
            comments=comments,
            added=b["added"].split(" ")[0],
            file=f"data/{b['path']}/{b['file']}.{b['format'].lower()}",
            cover=resize(cover, "400x600", fill=True, placeholder=True),
            coverSmall=resize(cover, "100x150", fill=True, placeholder=True),
        )

    return books
