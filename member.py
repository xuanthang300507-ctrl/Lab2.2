class Member:
    def __init__(self, member_id, name):
        self.member_id = member_id
        self.name = name
	# Implement các phương thức cho thao tác insert update delete select vào DB
    def add_member(self, db):
        query = "INSERT INTO members (name) VALUES (?)"
        db.execute_query(query, (self.name,))
    def delete_member(self, db):
        query = "DELETE FROM members WHERE member_id = ?"
        db.execute_query(query, (self.member_id,))
    def update_member_info(self, db):
        query = "UPDATE members SET name = ? WHERE member_id = ?"
        db.execute_query(query, (self.name, self.member_id))    
    @staticmethod
    def search_member(db, member_name):
        query = "SELECT * FROM members WHERE name = ?"
        return db.fetch_one(query, (member_name,))

    @staticmethod
    def get_all_members(db):
        query = "SELECT * FROM members"
        return db.fetch_all(query)
