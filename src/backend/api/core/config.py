from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from pathlib import Path
import torch
 
global API_DIR, MODEL_DIR, PROJECT_ROOT, MODEL_PATH, CONFIG_MODEL_PATH
API_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = str(API_DIR.parent.parent.parent)
MODEL_DIR = PROJECT_ROOT + "/models"
MODEL_PATH = MODEL_DIR + "/resnet50_best.pt"
CONFIG_MODEL_PATH = MODEL_DIR + "/config.json"

class Settings(BaseSettings):
    PROJECT_NAME: str = "Animal classifier API"
    API_V1_STR: str = "/api/v1"

    DEVICE: str = "cuda" if torch.cuda.is_available() else "cpu"

    model_config = ConfigDict(env_prefix="", env_file=".env")

settings = Settings()
