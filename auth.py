from flask import Blueprint, request, jsonify
from pymongo import MongoClient
import bcrypt
import os

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["drift"]
users = db["users"]

# Define the Blueprint
auth_bp = Blueprint("auth", __name__)

@auth_bp.route('/login', methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"success": False, "message": "Username and password are required."}), 400

    user = users.find_one({"username": username})
    if not user:
        return jsonify({"success": False, "message": "User not found."}), 404

    if bcrypt.checkpw(password.encode(), user["password"]):
        return jsonify({"success": True, "message": "Login successful."})
    
    return jsonify({"success": False, "message": "Incorrect password."}), 401
