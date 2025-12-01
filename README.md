# Aerospace Surface Defect Detection

## Introduction
This project implements a complete pipeline for aerospace surface defect detection using Convolutional Neural Networks (CNNs) built with PyTorch. The trained models are deployed through a FastAPI, providing an interactive interface for uploading images and viewing defect predictions. This end-to-end solution covers dataset preparation, model training, evaluation, export, and deployment.

## Features

- 🔍 **Real-time Detection**: Detect 4 types of aerospace defects (Crack, Deform, Paint Peel, Rivet Damage)
- 📊 **Visual Results**: Bounding boxes with confidence scores
- ⚡ **Fast Inference**: Optimized YOLOv8 model (~92% test accuracy)
- 🌐 **REST API**: Exposed endpoints for integration
- 📱 **Responsive UI**: Clean, simple interface
- ☁️ **Cloud Ready**: Deployed on Render

## Detectable Defects

1. **Crack** - Surface cracks in aircraft skin
2. **Deform** - Structural deformations
3. **Paint Peel** - Paint damage and peeling
4. **Rivet Damage** - Damaged or missing rivets

## Project Structure

```
aerospace-defect-detection/
├── app/
│   ├── api/routes.py          # API endpoints
│   ├── core/inference.py      # YOLO inference
│   ├── static/                # CSS, JS, uploads
│   ├── config.py              # Settings
│   ├── models.py              # Pydantic schemas
│   └── main.py                # FastAPI app
├── models/best.pt             # Trained YOLOv8 model
├── templates/index.html       # Frontend
└── requirements.txt
```

## Local Setup

### Prerequisites
- Python 3.11


### Installation

1. **Clone repository**
```bash
git clone https://github.com/SANK-0311/Aerospace-Defect-Detection.git
cd aerospace-defect-detection
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
python -m app.main
```

Visit `http://localhost:8000`

## API Endpoints

### `GET /api/`
Health check and model status

### `POST /api/predict`
Upload image for defect detection

**Request:**
- Method: POST
- Body: multipart/form-data
- Field: `file` (image file)

**Response:**
```json
{
  "success": true,
  "image_name": "aircraft.jpg",
  "detections": [
    {
      "class_name": "Crack",
      "confidence": 0.89,
      "bounding_box": {
        "x1": 120.5,
        "y1": 230.1,
        "x2": 450.3,
        "y2": 380.7
      }
    }
  ],
  "total_detections": 1,
  "inference_time": 0.234,
  "image_url": "/static/uploads/annotated_xyz.jpg"
}
```

### `GET /api/classes`
Get list of detectable defect classes


## Configuration

Edit `.env` file:

```env
MODEL_PATH=models/best.pt
CONFIDENCE_THRESHOLD=0.25    # Detection confidence threshold
IOU_THRESHOLD=0.45           # Intersection over Union threshold
MAX_UPLOAD_SIZE=10485760     # Max file size (10MB)
```

## Model Details

- **Architecture**: YOLOv8
- **Training**: Transfer learning with data augmentation
- **Input**: High-resolution aerospace surface images
- **Classes**: 4 defect types

## Technologies Used

- **Backend**: FastAPI, Uvicorn
- **ML Framework**: PyTorch, Ultralytics YOLO
- **Image Processing**: OpenCV, Pillow
- **Frontend**: Vanilla JavaScript, HTML, CSS
- **Deployment**: Render



## Author

SANTHOSH KUMAR - Aerospace Defect Detection System
```