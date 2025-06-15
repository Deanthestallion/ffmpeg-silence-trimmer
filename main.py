from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Service is up!"

# Optional: your other API routes here
# @app.route("/process", methods=["POST"])
# def process():
#     ...

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
