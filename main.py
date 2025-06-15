from flask import Flask, request, jsonify, send_file
import subprocess
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Welcome to the FFmpeg Silence Trimmer API!",
        "usage": "POST a video file to /trim using the 'file' field in form-data."
    })

@app.route("/trim", methods=["POST"])
def trim_video():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    input_path = "input.mp4"
    output_path = "output_trimmed.mp4"
    
    file.save(input_path)

    command = [
        "ffmpeg", "-i", input_path,
        "-af", "silenceremove=stop_periods=-1:stop_duration=1:stop_threshold=-40dB",
        "-y", output_path
    ]

    try:
        subprocess.run(command, check=True)
        return send_file(output_path, mimetype='video/mp4', as_attachment=True)
    except subprocess.CalledProcessError as e:
        return jsonify({"error": str(e)}), 500
