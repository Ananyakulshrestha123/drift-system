from pymongo import MongoClient

# MongoDB configuration using PyMongo directly
client = MongoClient("mongodb://localhost:27017/")
db = client["meeting_drift"]
meetings = db["meeting_info"]

# Test MongoDB connection on startup
try:
    client.admin.command("ping")
    print("✅ Connected to MongoDB")
except Exception as e:
    print("❌ Database connection failed:", e)
