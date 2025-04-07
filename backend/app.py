from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# ✅ Register your routes
from routes.audio import audio_bp
from routes.auth import auth_bp  # import login blueprint

app.register_blueprint(audio_bp)
app.register_blueprint(auth_bp)

# ✅ Optional: Default route to avoid 404 on root
@app.route("/")
def index():
    return "🎧 Drift Monitor Backend is Running!"

if __name__ == '__main__':
    app.run(debug=True)
