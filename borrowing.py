from datetime import date, timedelta

class Borrowing:
    def __init__(self, borrowing_id, member_id, book_id, borrow_date, due_date = None, return_date=None):
        self.borrowing_id = borrowing_id
        self.member_id = member_id
        self.book_id = book_id
        self.borrow_date = borrow_date
        self.due_date = due_date
        self.return_date = return_date

    def borrow_book(self, db):
        query = """
        INSERT INTO borrowing (member_id, book_id, borrow_date, due_date, return_date) 
        VALUES (?, ?, ?, ?, ?)
        """
        params = (self.member_id, self.book_id, self.borrow_date, self.due_date, self.return_date)
        db.execute_query(query, params)

    def return_book(self, db):
        query = "UPDATE borrowing SET return_date = ? WHERE borrowing_id = ?"
        params = (self.return_date, self.borrowing_id)
        db.execute_query(query, params)

    @staticmethod
    def get_overdue_books(db):
       query = """
        SELECT b.title, m.name, bo.borrow_date, bo.return_date
        FROM borrowing bo
        JOIN books b ON bo.book_id = b.book_id
        JOIN members m ON bo.member_id = m.member_id
        WHERE bo.return_date IS NOT NULL AND bo.return_date < ?
        """
       today = date.today()
       return db.fetch_all(query, (today,))
    @staticmethod
    def get_borrowing_by_id(db, borrowing_id):
      """Lấy thông tin trả sách theo ID mượn sách"""
      query = "SELECT * FROM borrowing WHERE borrowing_id = ?"
      return db.fetch_one(query, (borrowing_id,))