from flask import Blueprint, request, jsonify
from deepgram import Deepgram
from pymongo import MongoClient
import os

audio_bp = Blueprint("audio", __name__)

# Load Deepgram API key from environment
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
if not DEEPGRAM_API_KEY:
    raise Exception("Deepgram API key not found. Check your .env file.")

deepgram = Deepgram(DEEPGRAM_API_KEY)

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["drift"]
meetings_collection = db["meetings"]
transcripts_collection = db["transcripts"]

# Route: Upload + Transcribe + Save Metadata + Transcript
@audio_bp.route('/upload', methods=['POST'])
def upload_audio():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Metadata fields from form (optional in case of dashboard use)
    meeting_id = request.form.get("meetingId")
    meeting_link = request.form.get("meetingLink")
    meeting_date = request.form.get("meetingDate")
    meeting_time = request.form.get("meetingTime")
    organizer = request.form.get("organizer")

    mime_type = file.mimetype or 'audio/wav'

    try:
        file_buffer = file.read()

        options = {
            'punctuate': True,
            'language': 'en',
            'detect_language': True
        }

        response = deepgram.transcription.sync_prerecorded(
            {'buffer': file_buffer, 'mimetype': mime_type},
            options
        )

        transcript = response['results']['channels'][0]['alternatives'][0].get('transcript', '')

        # Save all metadata and transcript in one place
        meeting_data = {
            'meetingId': meeting_id,
            'meetingLink': meeting_link,
            'meetingDate': meeting_date,
            'meetingTime': meeting_time,
            'organizer': organizer,
            'transcript': transcript
        }
        meetings_collection.insert_one(meeting_data)

        return jsonify({'transcript': transcript})

    except Exception as e:
        return jsonify({'error': 'Transcription failed', 'details': str(e)}), 500

# Route: Only store transcript (for extra/manual save)
@audio_bp.route('/store_transcript', methods=['POST'])
def store_transcript():
    data = request.get_json()
    transcript = data.get("transcript")

    if not transcript:
        return jsonify({"success": False, "message": "No transcript provided"}), 400

    transcripts_collection.insert_one({"transcript": transcript})
    print("✅ Transcript stored in MongoDB.")
    return jsonify({"success": True, "message": "Transcript stored successfully"})
