import cv2
import numpy as np
from ultralytics import YOLO
from flask import Flask, render_template, Response, request

app = Flask(__name__)

# Load YOLO model
model = YOLO('models/yolov8n.pt')

# Load accessories and convert to RGBA if they lack transparency
def load_and_convert_image(path):
    image = cv2.imread(path, cv2.IMREAD_UNCHANGED)

    # Convert to RGBA if not already
    if image is not None and image.shape[2] == 3:
        print(f"Converting {path} to RGBA (adding alpha channel)")
        image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
    elif image is None:
        print(f"Error: Could not load image from {path}")
    return image

glasses = load_and_convert_image('C:\\Users\\shush\\Downloads\\imgdtc\\Virtual-Try-On-YOLO\\static\\images\\glasses.png')
watch = load_and_convert_image('Virtual-Try-On-YOLO\\static\\images\\watch.png')


selected_accessory = 'glasses'  # Default accessory

# Resize image
def resize_image(image, width, height):
    return cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)

# Overlay image
def overlay_image(background, overlay, x, y):
    h, w = overlay.shape[:2]
    alpha_overlay = overlay[:, :, 3] / 255.0
    alpha_background = 1.0 - alpha_overlay

    for c in range(3):
        background[y:y+h, x:x+w, c] = (
            alpha_overlay * overlay[:, :, c] +
            alpha_background * background[y:y+h, x:x+w, c]
        )
    return background

# Video streaming
def generate_frames():
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break

        results = model(frame)

        # Select accessory
        accessory = glasses if selected_accessory == 'glasses' else watch

        for result in results[0].boxes:
            x1, y1, x2, y2 = map(int, result.xyxy[0])
            label = result.cls[0].item()

            if label == 0:  # Face detection
                face_width = x2 - x1
                resized_accessory = resize_image(accessory, face_width, int(face_width / 2.5))
                overlay_image(frame, resized_accessory, x1, y1 - int(face_width / 4))

        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Accessory change route
@app.route('/change_accessory')
def change_accessory():
    global selected_accessory
    accessory = request.args.get('accessory')
    if accessory in ['glasses', 'watch']:
        selected_accessory = accessory
        print(f"Accessory changed to {accessory}")
        return '', 204
    else:
        return 'Invalid accessory', 400
def overlay_image(background, overlay, x, y):
    if overlay.shape[2] < 4:
        print("Error: Accessory image does not have an alpha channel.")
        return background

    h, w = overlay.shape[:2]
    alpha_overlay = overlay[:, :, 3] / 255.0
    alpha_background = 1.0 - alpha_overlay

    for c in range(3):
        background[y:y+h, x:x+w, c] = (
            alpha_overlay * overlay[:, :, c] +
            alpha_background * background[y:y+h, x:x+w, c]
        )
    return background

if __name__ == '__main__':
    app.run(debug=True)
