from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status

# uvicorn books:app --reload
# fastapi dev books.py
# fastapi run books.py

app = FastAPI()


# Old way to define a model
# class Book:
#     id: int
#     title: str
#     author: str
#     description: str
#     rating: float

#     def __init__(self, id: int, title: str, author: str, description: str, rating: float):
#         self.id = id
#         self.title = title
#         self.author = author
#         self.description = description
#         self.rating = rating


# Pydantic way to define a model
class Book(BaseModel):
    id: int | None = Field(description="The ID of the book", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: float = Field(ge=0, le=5)
    published_year: int = Field(ge=2000, le=2025)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Example Book Title",
                "author": "Example Author",
                "description": "This is an example description of the book.",
                "rating": 5,
                "published_year": 2025,
            }
        }
    }


BOOKS = [
    Book(
        id=1,
        title="Title 1",
        author="Author 1",
        description="Description 1",
        rating=4.5,
        published_year=2011,
    ),
    Book(
        id=2,
        title="Title 2",
        author="Author 2",
        description="Description 2",
        rating=3.8,
        published_year=2012,
    ),
    Book(
        id=3,
        title="Title 3",
        author="Author 3",
        description="Description 3",
        rating=4.0,
        published_year=2013,
    ),
    Book(
        id=4,
        title="Title 4",
        author="Author 4",
        description="Description 4",
        rating=4.2,
        published_year=2014,
    ),
    Book(
        id=5,
        title="Title 5",
        author="Author 5",
        description="Description 5",
        rating=4.8,
        published_year=2015,
    ),
    Book(
        id=6,
        title="Title 6",
        author="Author 6",
        description="Description 6",
        rating=3.5,
        published_year=2016,
    ),
]


# @app.get("/books")
# async def get_all_books():
#     return BOOKS


# Query parameters 1
@app.get("/books", status_code=status.HTTP_200_OK)
async def find_books_by_rating(
    rating: float | None = Query(ge=0, le=5, default=None)
) -> list[Book]:
    if rating is None:
        return BOOKS

    books_found = []
    for book in BOOKS:
        if book.rating >= rating:
            books_found.append(book)
    return books_found


# Query parameters 2
@app.get("/books/publish/", status_code=status.HTTP_200_OK)
async def find_books_by_published_year(
    published_year: int | None = Query(ge=2000, le=2025, default=None)
) -> list[Book]:
    if published_year is None:
        return BOOKS

    books_found = []
    for book in BOOKS:
        if book.published_year == published_year:
            books_found.append(book)
    return books_found


# Path parameters
@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def find_book_by_id(book_id: int = Path(gt=0)) -> Book:
    for book in BOOKS:
        if book.id == book_id:
            return book
    else:
        raise HTTPException(status_code=404, detail="Book not found")


# @app.post("/books/create_v1")
# async def create_book(new_book=Body()):
#     BOOKS.append(new_book)


@app.post("/books/create_v2", status_code=status.HTTP_201_CREATED)
async def create_book_v2(new_book: Book) -> Book:
    new_book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    BOOKS.append(new_book)

    return new_book


# @app.put("/books/update_v1")
# async def update_book(updated_book=Body()):
#     for i in range(len(BOOKS)):
#         if BOOKS[i].get("title").casefold() == updated_book.get("title").casefold():
#             BOOKS[i] = updated_book


@app.put("/books/update_v2", status_code=status.HTTP_200_OK)
async def update_book(new_book: Book) -> Book:
    updated_book = None

    for i in range(len(BOOKS)):
        if BOOKS[i].id == new_book.id:
            updated_book = BOOKS[i] = new_book
            return updated_book

    raise HTTPException(status_code=404, detail="Book not found")


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)) -> None:
    is_book_deleted = False

    for book in BOOKS:
        if book.id == book_id:
            BOOKS.remove(book)
            is_book_deleted = True

    if not is_book_deleted:
        raise HTTPException(status_code=404, detail="Book not found")
