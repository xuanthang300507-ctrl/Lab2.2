class Book:
    def __init__(self, book_id, title, author, pages, year_published, status, category):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.pages = pages
        self.year_published = year_published
        self.status = status
        self.category = category

    def __str__(self):
        trang_thai = "Đã mượn" if self.status == 1 else "Có sẵn"
        return f"ID: {self.book_id} | Tên sách: {self.title} | Tác giả: {self.author} | Trạng thái: {trang_thai}"

    def add_book(self, db):
        query = "INSERT INTO books (title, author, pages, year_published, status, category) VALUES (?, ?, ?, ?, ?, ?)"
        params = (self.title, self.author, self.pages, self.year_published, self.status, self.category)
        db.execute_query(query, params)

    def update_book(self, db):
        query = "UPDATE books SET title = ?, author = ?, pages = ?, year_published = ?, status = ?, category = ? WHERE book_id = ?"
        params = (self.title, self.author, self.pages, self.year_published, self.status, self.category, self.book_id)
        db.execute_query(query, params)
        book = Book.search_book(db, self.book_id)
        return book

    def delete_book(self, db):
        query = "DELETE FROM books WHERE book_id = ?"
        db.execute_query(query, (self.book_id,))

    def return_book(self, db):
        query = "UPDATE books SET status = 0 WHERE book_id = ?"
        db.execute_query(query, (self.book_id,))

    @staticmethod
    def search_book(db, book_id):
        query = "SELECT * FROM books WHERE book_id = ?"
        row = db.fetch_one(query, (book_id,))
        if row:
            return Book(row['book_id'], row['title'], row['author'], row['pages'], row['year_published'], row['status'], row['category'])
        return None

    @staticmethod
    def get_all_books(db):
        query = "SELECT * FROM books"
        rows = db.fetch_all(query)
        books = []
        for row in rows:
            books.append(Book(row['book_id'], row['title'], row['author'], row['pages'], row['year_published'], row['status'], row['category']))
        return books

    @staticmethod
    def search_book_by_title(db, title):
        query = "SELECT * FROM books WHERE title = ?"
        rows = db.fetch_all(query, (title,))
        books = []
        for row in rows:
            books.append(Book(row['book_id'], row['title'], row['author'], row['pages'], row['year_published'], row['status'], row['category']))
        return books