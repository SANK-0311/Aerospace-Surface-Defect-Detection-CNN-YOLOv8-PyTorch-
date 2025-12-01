import time
from pathlib import Path
from typing import List, Optional
import cv2
import numpy as np
from ultralytics import YOLO

from app.config import settings
from app.models import Detection, BoundingBox

class DefectDetector:
    def __init__(self):
        self.model: Optional[YOLO] = None
        self.model_loaded = False
        self.class_names = ['Crack', 'Deform', 'Paint Peel', 'Rivet Damage']
        
    def load_model(self):
        """Load the YOLO model"""
        try:
            model_path = Path(settings.MODEL_PATH)
            if not model_path.exists():
                raise FileNotFoundError(f"Model file not found at {model_path}")
            
            self.model = YOLO(str(model_path))
            self.model_loaded = True
            print(f"✅ Model loaded successfully from {model_path}")
            
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            raise
    
    def predict(self, image_path: str) -> tuple[List[Detection], float]:
        """
        Run inference on an image
        
        Returns:
            tuple: (list of detections, inference time)
        """
        if not self.model_loaded:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        
        start_time = time.time()
        
        # Run inference
        results = self.model.predict(
            source=image_path,
            conf=settings.CONFIDENCE_THRESHOLD,
            iou=settings.IOU_THRESHOLD,
            verbose=False
        )
        
        inference_time = time.time() - start_time
        
        # Parse results
        detections = []
        
        if results and len(results) > 0:
            result = results[0]  # Get first result
            
            if result.boxes is not None and len(result.boxes) > 0:
                boxes = result.boxes.xyxy.cpu().numpy()  # Bounding boxes
                confidences = result.boxes.conf.cpu().numpy()  # Confidence scores
                class_ids = result.boxes.cls.cpu().numpy().astype(int)  # Class IDs
                
                for box, conf, cls_id in zip(boxes, confidences, class_ids):
                    detection = Detection(
                        class_name=self.class_names[cls_id],
                        confidence=float(conf),
                        bounding_box=BoundingBox(
                            x1=float(box[0]),
                            y1=float(box[1]),
                            x2=float(box[2]),
                            y2=float(box[3])
                        )
                    )
                    detections.append(detection)
        
        return detections, inference_time
    
    def draw_detections(self, image_path: str, detections: List[Detection], output_path: str):
        """Draw bounding boxes on image"""
        # Read image
        image = cv2.imread(image_path)
        
        # Color map for each class (BGR format)
        colors = {
            'Crack': (0, 0, 255),        # Red
            'Deform': (0, 255, 0),       # Green
            'Paint Peel': (255, 0, 0),   # Blue
            'Rivet Damage': (0, 255, 255) # Yellow
        }
        
        for detection in detections:
            bbox = detection.bounding_box
            x1, y1 = int(bbox.x1), int(bbox.y1)
            x2, y2 = int(bbox.x2), int(bbox.y2)
            
            color = colors.get(detection.class_name, (255, 255, 255))
            
            # Draw rectangle
            cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
            
            # Prepare label
            label = f"{detection.class_name}: {detection.confidence:.2f}"
            
            # Calculate text size for background
            (text_width, text_height), baseline = cv2.getTextSize(
                label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2
            )
            
            # Draw background rectangle for text
            cv2.rectangle(
                image,
                (x1, y1 - text_height - 10),
                (x1 + text_width, y1),
                color,
                -1
            )
            
            # Draw text
            cv2.putText(
                image,
                label,
                (x1, y1 - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                2
            )
        
        # Save annotated image
        cv2.imwrite(output_path, image)

# Global detector instance
detector = DefectDetector()