from fastapi import FastAPI, Body

# uvicorn books:app --reload
# fastapi dev books.py
# fastapi run books.py

app = FastAPI()

BOOKS = [
    {"title": "Title 1", "author": "Author 1", "category": "Science"},
    {"title": "Title 2", "author": "Author 2", "category": "History"},
    {"title": "Title 3", "author": "Author 3", "category": "Science"},
    {"title": "Title 4", "author": "Author 4", "category": "Thriller"},
    {"title": "Title 5", "author": "Author 5", "category": "Violence"},
]


# @app.get("/books")
# async def get_all_books():
#     return BOOKS


# Path parameters
@app.get("/books/{book_title}")
async def find_book_by_title(book_title: str):
    for book in BOOKS:
        if book.get("title").casefold() == book_title.casefold():
            return book
    else:
        return {"message": "Book Not Found"}


# Query parameters
@app.get("/books")
async def find_books_by_category(category: str = None):
    if not category:
        return BOOKS

    books_to_return = []
    for book in BOOKS:
        if book.get("category").casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return


@app.post("/books/create")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)


@app.put("/books/update")
async def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold() == updated_book.get("title").casefold():
            BOOKS[i] = updated_book


@app.delete("/books/delete/{book_title}")
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold() == book_title.casefold():
            return BOOKS.pop(i)
