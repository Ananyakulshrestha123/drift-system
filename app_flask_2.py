from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from pymongo.errors import DuplicateKeyError

app = Flask(__name__)

# MongoDB configuration using PyMongo directly
client = MongoClient("mongodb://localhost:27017/")
db = client["meeting_drift"]
meetings = db["meeting_info"]

# Convert ObjectId to string
def serialize_meeting(meeting):
    meeting["_id"] = str(meeting["_id"])
    return meeting

# ✅ Test MongoDB connection on startup
try:
    client.admin.command("ping")
    print("✅ Connected to MongoDB")
except Exception as e:
    print("❌ Database connection failed:", e)

# ✅ POST endpoint
@app.route("/meetings", methods=["POST"])
def create_meeting():
    try:
        print("🟡 Headers:", dict(request.headers))
        print("🟢 Raw data:", request.data.decode("utf-8"))

        data = request.get_json(force=True)
        print("🔵 Parsed JSON:", data)

        full_meeting = {
            "_id": ObjectId(),
            "meeting_id": data.get("meeting_id", ""),
            "meeting_topic": data.get("meeting_topic", ""),
            "meeting_date": data.get("meeting_date", ""),
            "duration": data.get("duration", 0),
            "status": data.get("status", "NEW"),
            "created_by": data.get("created_by", ""),
            "created_by_name": data.get("created_by_name", ""),
            "lastupdated_by": data.get("lastupdated_by", ""),
            "lastupdated_name": data.get("lastupdated_name", ""),
            "created_date": data.get("created_date", ""),
            "meeting_time": data.get("meeting_time", ""),
            "agenda": data.get("agenda", []),
            "comments": data.get("comments", "")
        }

        result = meetings.insert_one(full_meeting)
        inserted = meetings.find_one({"_id": result.inserted_id})
        return jsonify(serialize_meeting(inserted)), 201

    except DuplicateKeyError:
        return jsonify({"error": "Meeting ID must be unique"}), 400
    except Exception as e:
        print("❌ Error in POST:", e)
        return jsonify({"error": str(e)}), 500

# ✅ GET all meetings
@app.route("/meetings", methods=["GET"])
@app.route("/", methods=["GET"])
def get_meetings():
    try:
        all_meetings = list(meetings.find())
        return jsonify([serialize_meeting(m) for m in all_meetings]), 200
    except Exception as e:
        print("❌ Error in GET:", e)
        return jsonify({"error": str(e)}), 500

# ✅ PUT (Update meeting)
@app.route("/meetings/<id>", methods=["PUT"])
def update_meeting(id):
    try:
        data = request.get_json(force=True)
        update_fields = {key: value for key, value in data.items() if key != "_id"}
        result = meetings.update_one({"_id": ObjectId(id)}, {"$set": update_fields})

        if result.matched_count == 0:
            return jsonify({"message": "Meeting not found"}), 404
        elif result.modified_count == 0:
            updated = meetings.find_one({"_id": ObjectId(id)})
            return jsonify({
                "message": "No changes made",
                "meeting": serialize_meeting(updated)
            }), 200

        updated = meetings.find_one({"_id": ObjectId(id)})
        return jsonify(serialize_meeting(updated)), 200
    except Exception as e:
        print("❌ Error in PUT:", e)
        return jsonify({"error": str(e)}), 500

# ✅ DELETE (Delete meeting)
@app.route("/meetings/<id>", methods=["DELETE"])
def delete_meeting(id):
    try:
        result = meetings.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 0:
            return jsonify({"message": "Meeting not found"}), 404
        return jsonify({"message": "Meeting deleted successfully"}), 200
    except Exception as e:
        print("❌ Error in DELETE:", e)
        return jsonify({"error": str(e)}), 500

# ✅ Test Flask server
@app.route("/test", methods=["GET"])
def test():
    return jsonify({"status": "✅ Flask server running"}), 200

# ✅ Test DB connection
@app.route("/test-mongo", methods=["GET"])
def test_mongo():
    try:
        client.admin.command("ping")
        return jsonify({"status": "✅ Database connected"}), 200
    except Exception as e:
        return jsonify({"status": "❌ Database error", "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
