from pymongo import MongoClient
import bcrypt

client = MongoClient("mongodb://localhost:27017/")
db = client["drift"]
users = db["users"]

username = "admin"
password = "admin123"
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

users.insert_one({
    "username": username,
    "password": hashed
})
print("✅ User added.")
