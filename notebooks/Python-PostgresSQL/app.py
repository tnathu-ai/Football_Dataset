from user import User
from database import Database

Database.initialise(database="tnathu", user="postgres", password="1234", host="localhost")

user = User('thu.tna@kpim.vn', 'Thu', 'Tran')

user.save_to_db()

user_from_db = User.load_from_db_by_email('thu.tna@kpim.vn')

print(user_from_db)
