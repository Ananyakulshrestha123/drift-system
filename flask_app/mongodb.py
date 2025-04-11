from bson.objectid import ObjectId

def serialize_meeting(meeting):
    meeting["_id"] = str(meeting["_id"])
    return meeting
