from database import Database
from book import Book
from member import Member
from borrowing import Borrowing
from datetime import datetime, timedelta

def main():
    db = Database()
    
    while True:
        print("\n--- HỆ THỐNG QUẢN LÝ THƯ VIỆN ---")
        print("1. Thêm sách")
        print("2. Sửa thông tin sách")
        print("3. Tìm kiếm sách")
        print("4. Hiển thị danh sách sách")
        print("5. Thêm thành viên")
        print("6. Tìm kiếm thành viên")
        print("7. Mượn sách")
        print("8. Trả sách")
        print("9. Hiển thị sách đã mượn quá hạn")
        print("10. Thoát")

        choice = input("Chọn chức năng: ")
        
        if choice == "1":
            title = input("Nhập tên sách: ")
            author = input("Nhập tác giả: ")
            pages = int(input("Nhập số trang: "))
            year_published = int(input("Nhập năm xuất bản: "))
            status = int(input("Nhập trạng thái sách (0: có sẵn, 1: đã mượn, 2 : trạng thái khác ): "))
            category = input("Nhập chủng loại sách (Toan , Van , Anh ): ")
            book = Book(None, title, author, pages, year_published, status, category)
            book.add_book(db)

        elif choice == "2":
            book_id = int(input("Nhập ID sách: "))
            book = Book.search_book(db, book_id)
            if book:
                title = input("Nhập tên mới: ")
                author = input("Nhập tác giả mới: ")
                pages = int(input("Nhập số trang mới: "))
                year_published = int(input("Nhập năm xuất bản mới: "))
                status = int(input("Nhập trạng thái mới: "))
                category = input("Nhập chủng loại mới: ")
                updated_book = Book(book_id, title, author, pages, year_published, status, category)
                updated_book.update_book(db)
                print ("Thông tin sách đã được cập nhật.")
            else:
                print("Sách không tồn tại.")
          

        elif choice == "3":
            book_id = int(input("Nhập ID sách cần tìm: "))
            book = Book.search_book(db, book_id)
            if book:
                print(book)
            else:
                print("Sách không tồn tại.")

        elif choice == "4":
            books = Book.get_all_books(db)
            for book in books:
               print(book)

        elif choice == "5":  # Thêm thành viên
            name = input("Nhập tên thành viên: ")
            member = Member(None, name)
            member.add_member(db)
        elif choice == "6":  # Tìm kiếm thành viên
            member_name = input("Nhập tên thành viên cần tìm: ")
            member = Member.search_member(db, member_name)
            if member:
                print(f"ID Thành viên: {member['member_id']} | Họ tên: {member['name']}")
            else:
                print("Thành viên không tồn tại.")
        elif choice == "7":  # Mượn sách
            member_name = input("Nhập tên thành viên: ")
            book_id = input("Nhập ID sách cần mượn: ")
            member = Member.search_member(db, member_name)
            book = Book.search_book(db, book_id)
            print (f"Thông tin sách: {book}")
            if book and book.status == 0:  # Kiểm tra xem sách có sẵn để mượn hay không
                # Cập nhật trạng thái sách thành đã mượn
                book.status = 1
                book.update_book(db)
                print (f"Sách '{book.title}' đã được mượn thành công.")


            if book:
                borrow_date = datetime.today().strftime('%Y-%m-%d')
                
                # Tính ngày trả sách (14 ngày sau ngày mượn)
                return_date = (datetime.strptime(borrow_date, '%Y-%m-%d') + timedelta(days=14)).strftime('%Y-%m-%d')
                
                borrowing = Borrowing(None,member.member_id, book.book_id, borrow_date, return_date)
                borrowing.borrow_book(db)
                print(f" Ngày trả sách là {return_date}.")
            else:
                print(f"Sách '{book.title}' không tồn tại trong thư viện.")

        elif choice == "8":  # Trả sách
            borrowing_id = input("Nhập ID trả sách: ")
            return_date = datetime.today().strftime('%Y-%m-%d')
            borrowing_record = Borrowing.get_borrowing_by_id(db, borrowing_id)
            if borrowing_record:
              borrowing = Borrowing(**borrowing_record)
              borrowing.return_book(db)
            book = Book.search_book(db, borrowing_record['book_id'])
            if book:
             book.status = 0
             book.update_book(db)                                                   
             print("Sách đã được trả thành công.")

        elif choice == "9":  # Hiển thị sách đã mượn quá hạn
            overdue_books = Borrowing.get_overdue_books(db)
            if overdue_books:
                print("\nDanh sách sách đã mượn quá hạn:")
                for book in overdue_books:
                    print("Tên sách: {}, Tên thành viên: {}, Ngày mượn: {}, Ngày đến hạn: {}".format(book['title'], book['name'], book['borrow_date'], book['return_date']))
            else:
                print("Không có sách nào quá hạn.")

if __name__ == "__main__":
    main()
