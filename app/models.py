from pydantic import BaseModel, Field
from typing import List, Optional

class BoundingBox(BaseModel):
    x1: float = Field(..., description="Top-left x coordinate")
    y1: float = Field(..., description="Top-left y coordinate")
    x2: float = Field(..., description="Bottom-right x coordinate")
    y2: float = Field(..., description="Bottom-right y coordinate")

class Detection(BaseModel):
    class_name: str = Field(..., description="Defect class name")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    bounding_box: BoundingBox

class PredictionResponse(BaseModel):
    success: bool
    image_name: str
    detections: List[Detection]
    total_detections: int
    inference_time: float = Field(..., description="Inference time in seconds")
    image_url: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    app_name: str
    version: str

class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    detail: Optional[str] = None