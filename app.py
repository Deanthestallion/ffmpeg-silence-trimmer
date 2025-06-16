import os
import uuid
from flask import Flask, request, jsonify, send_from_directory
from threading import Thread
import subprocess

app = Flask(__name__)

# Directories
INPUT_DIR = 'inputs'
OUTPUT_DIR = 'outputs'
BASE_URL = 'https://auto-editor-33k6.onrender.com'

os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- Step 1: Cut Silence ---
def cut_silence(input_path, output_path):
    try:
        print(f"[INFO] Cutting silence from: {input_path}")
        subprocess.run([
            'auto-editor', input_path,
            '--silent-threshold', '0.03',
            '--frame-margin', '6',
            '--export', 'ffmpeg',
            '--output', output_path
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] auto-editor failed: {e}")

# --- Step 2: Zoom on Face ---
def zoom_on_face(input_path, output_path):
    try:
        print(f"[INFO] Zooming on face: {input_path}")
        command = [
            'python3', 'zoom_faces.py',  # Assumes you have a script for face zoom
            '--input', input_path,
            '--output', output_path
        ]
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] zoom_faces failed: {e}")

# --- Background Processing ---
def process_video_pipeline(input_path, final_output_path):
    trimmed_path = os.path.join(OUTPUT_DIR, f"trimmed_{uuid.uuid4().hex}.mp4")

    # 1. Cut silence
    cut_silence(input_path, trimmed_path)

    # 2. Zoom on face
    zoom_on_face(trimmed_path, final_output_path)

    print(f"[INFO] Finished processing {final_output_path}")

# --- API Endpoint ---
@app.route('/process', methods=['POST'])
def process():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400

    video_id = uuid.uuid4().hex
    input_path = os.path.join(INPUT_DIR, f"input_{video_id}.mp4")
    final_output_path = os.path.join(OUTPUT_DIR, f"output_{video_id}.mp4")

    file.save(input_path)

    # Process in background
    Thread(target=process_video_pipeline, args=(input_path, final_output_path)).start()

    return jsonify({
        'message': 'Video is being processed in background',
        'output_filename': os.path.basename(final_output_path),
        'download_url': f"{BASE_URL}/download/{os.path.basename(final_output_path)}"
    })

# --- Serve processed file ---
@app.route('/download/<path:filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(OUTPUT_DIR, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
