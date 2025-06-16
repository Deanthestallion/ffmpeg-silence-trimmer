import cv2
import sys
import os

def zoom_on_face(input_path, output_path):
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print(f"Error opening video file {input_path}")
        sys.exit(1)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        if len(faces) > 0:
            # Zoom on the largest face
            x, y, w, h = max(faces, key=lambda rect: rect[2] * rect[3])
            pad = 100
            x1 = max(0, x - pad)
            y1 = max(0, y - pad)
            x2 = min(width, x + w + pad)
            y2 = min(height, y + h + pad)
            zoomed = frame[y1:y2, x1:x2]
            zoomed = cv2.resize(zoomed, (width, height))
            out.write(zoomed)
        else:
            out.write(frame)

    cap.release()
    out.release()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python zoom_faces.py <input_path> <output_path>")
        sys.exit(1)

    zoom_on_face(sys.argv[1], sys.argv[2])
