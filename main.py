from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Server is live"

@app.route('/trim', methods=['POST'])
def trim_video():
    if 'video' not in request.files:
        return jsonify({"error": "No video uploaded"}), 400

    video = request.files['video']
    input_path = f"/tmp/{video.filename}"
    output_path = f"/tmp/trimmed_{video.filename}"
    
    video.save(input_path)

    # FFmpeg command to remove silence (example)
    os.system(f"ffmpeg -i {input_path} -af silenceremove=1:0:-50dB {output_path}")

    # Send the trimmed file back (optional)
    return jsonify({"message": "Video trimmed successfully", "output": output_path})
