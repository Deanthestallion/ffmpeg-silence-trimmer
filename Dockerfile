from flask import Flask, request, jsonify
import os
import subprocess
import uuid

app = Flask(__name__)

@app.route("/trim", methods=["POST"])
def trim():
    file = request.files["video"]
    filename = f"{uuid.uuid4()}.mp4"
    file.save(filename)

    output_file = f"trimmed_{filename}"
    command = [
        "ffmpeg", "-i", filename,
        "-af", "silencedetect=n=-30dB:d=0.5",
        "-f", "null", "-"
    ]
    subprocess.run(command)

    return jsonify({"message": "Silence detected. Trimming logic not yet implemented."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
