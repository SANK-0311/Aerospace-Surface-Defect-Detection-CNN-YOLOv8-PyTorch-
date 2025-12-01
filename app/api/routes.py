from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pathlib import Path

from app.models import PredictionResponse, HealthResponse, ErrorResponse
from app.core.inference import detector
from app.utils import validate_image, save_upload_file, cleanup_old_files
from app.config import settings

router = APIRouter()

@router.get("/", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        model_loaded=detector.model_loaded,
        app_name=settings.APP_NAME,
        version=settings.VERSION
    )

@router.post("/predict", response_model=PredictionResponse)
async def predict_defects(file: UploadFile = File(...)):
    """
    Upload an image and detect aerospace surface defects
    
    Returns:
        PredictionResponse with detections and bounding boxes
    """
    
    try:
        # Validate image
        validate_image(file)
        
        # Save uploaded file
        file_path = save_upload_file(file)
        
        # Run inference
        detections, inference_time = detector.predict(str(file_path))
        
        # Create annotated image
        annotated_filename = f"annotated_{file_path.name}"
        annotated_path = settings.UPLOAD_DIR / annotated_filename
        detector.draw_detections(str(file_path), detections, str(annotated_path))
        
        # Cleanup old files (optional, runs in background)
        cleanup_old_files(settings.UPLOAD_DIR, max_age_hours=1)
        
        return PredictionResponse(
            success=True,
            image_name=file.filename,
            detections=detections,
            total_detections=len(detections),
            inference_time=round(inference_time, 3),
            image_url=f"/static/uploads/{annotated_filename}"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/classes")
async def get_classes():
    """Get list of defect classes"""
    return {
        "classes": detector.class_names,
        "total_classes": len(detector.class_names)
    }