import sqlite3
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Book:
    author: str
    title: str
    format: str
    path: str
    file: str


def get_books(search: str = "%") -> list[Book]:
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
    """

    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    books = [
        Book(
            path=b["path"],
            format=b["format"],
            author=b["author"],
            title=b["title"],
            file=f"data/{b['path']}/{b['file']}.{b['format'].lower()}",
        )
        for b in data
    ]
    return books
