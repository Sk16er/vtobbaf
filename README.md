# Virtual Try-On with Object Detection

This is a Flask-based virtual try-on application using YOLO for object detection. It allows users to overlay accessories like glasses or watches on detected objects in real-time using a webcam.

## Features
- Real-time object detection using YOLOv8
- Virtual try-on of accessories (Glasses or Watch)
- Easy accessory switching via URL endpoint
- Flask web interface for video streaming

## Prerequisites
Make sure you have the following installed:
- Python 3.8+
- OpenCV
- NumPy
- Flask
- Ultralytics YOLO
- A webcam for real-time video

## Installation
1. Clone the repository:
```bash
git clone https://github.com/yourusername/virtual-tryon-yolo.git
cd virtual-tryon-yolo
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate   # On Linux/macOS
venv\Scripts\activate      # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Download the YOLOv8 model:
```bash
from ultralytics import YOLO
model = YOLO('yolov8n.pt')
model.export()
```
Save the model in the `models/` directory.

5. Place your accessory images in `static/images/` with transparent backgrounds (PNG format).
- `glasses.png`
- `watch.png`

## Usage
1. Run the application:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000/
```

3. Switch accessories using the endpoint:
```
http://localhost:5000/change_accessory?accessory=glasses
http://localhost:5000/change_accessory?accessory=watch
```

## Troubleshooting
- Ensure accessory images have transparency (RGBA format).
- Check your webcam connection if video is not displayed.
- Confirm that the YOLO model is correctly placed in the `models/` directory.

## Contributing
Feel free to fork this project, submit pull requests, or report any issues.

## License
This project is licensed under the MIT License.

