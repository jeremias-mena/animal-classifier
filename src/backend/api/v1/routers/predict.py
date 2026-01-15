from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
import torch
from PIL import Image
from src.model.utils import get_transformer
from src.backend.api.core.dependencies import get_model, get_model_config
from src.backend.api.schemas.prediction import PredictionResponse
from src.backend.api.core.config import settings

router = APIRouter(prefix="/predict")

@router.post("", response_model=PredictionResponse)
async def predict(file: UploadFile = File(...), model = Depends(get_model), config = Depends(get_model_config)):
    try:
        image = Image.open(file.file).convert("RGB")
        transform = get_transformer(mean=config["imagenet_mean"], std=config["imagenet_std"], resize_shape=(config["input_size"][1], config["input_size"][2]))
        x = transform(image).unsqueeze(0).to(settings.DEVICE)

        with torch.no_grad():
            logits = model(x)
            probs = torch.softmax(logits, dim=1).squeeze().tolist()

            prediction_index = int(torch.argmax(torch.tensor(probs)))
            prediction = config["classes"][prediction_index]

        return {
                    "prediction": prediction,
                    "probabilities": {
                        config["classes"][0]: probs[0],
                        config["classes"][1]: probs[1],
                    }
                }
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid image file")    
    
    
         