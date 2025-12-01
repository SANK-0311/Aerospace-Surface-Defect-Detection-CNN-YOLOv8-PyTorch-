from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Aerospace Defect Detection API"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Model
    MODEL_PATH: str = "models/best.pt"
    CONFIDENCE_THRESHOLD: float = 0.25
    IOU_THRESHOLD: float = 0.45
    
    # Upload
    MAX_UPLOAD_SIZE: int = 10485760  # 10MB
    ALLOWED_EXTENSIONS: str = "jpg,jpeg,png,bmp"
    UPLOAD_DIR: Path = Path("app/static/uploads")
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    class Config:
        env_file = ".env"
        case_sensitive = True

    def get_allowed_extensions(self) -> list:
        return [ext.strip() for ext in self.ALLOWED_EXTENSIONS.split(",")]

settings = Settings()

# Ensure upload directory exists
settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)