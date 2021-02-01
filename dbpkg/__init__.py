from pymongo import MongoClient
from werkzeug.security import generate_password_hash

# mongodb 연결
client = MongoClient("mongodb://localhost:27017/")
# mongodb 접근
db = client['board']
# board 컬렉션 생성
userDB = db['user_info']
loggedDB = db['logged']
boardDB = db['board']

if userDB.find({"$exist": {"email": "admin@admin.com", "name": "admin", "password": generate_password_hash("password")}}) == False:
    userDB.insert({"email": "admin@admin.com", "name": "admin", "password": generate_password_hash("password")})
if loggedDB.find({"$exist": {"logged_id": "admin"}}) == False:
    loggedDB.insert({"logged_id": "admin"})
if boardDB.find({"$exist": {"board_name": "공지사항"}}) == False:
    boardDB.insert({"board_name": "공지사항", "title": "공지", "content": "제곧내"})