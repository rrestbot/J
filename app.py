from flask import Flask, request, send_file
from flask_cors import CORS
import yt_dlp
import os
import uuid

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "🎧 YouTube MP3 API Working"

@app.route("/stream-direct")
def stream_direct():
    url = request.args.get("url")
    if not url:
        return "Missing URL", 400

    filename = f"{uuid.uuid4()}.mp3"
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'outtmpl': filename,
        'cookiefile': 'cookies.txt',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '128',
        }]
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return send_file(filename, mimetype="audio/mpeg")
    except Exception as e:
        return f"Error: {str(e)}", 500
    finally:
        if os.path.exists(filename):
            os.remove(filename)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
