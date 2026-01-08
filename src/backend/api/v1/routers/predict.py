from fastapi import APIRouter, UploadFile, File, Depends
import torch
from PIL import Image
from src.model.utils import get_transformer
from src.backend.api.core.dependencies import get_model, get_model_config
from src.backend.api.schemas.prediction import PredictionResponse

router = APIRouter(prefix="/predict")

@router.post("", response_model=PredictionResponse)
async def predict(file: UploadFile = File(...), model = Depends(get_model), config = Depends(get_model_config)):
    image = Image.open(file.file).convert("RGB")
    transform = get_transformer(config["imagenet_mean"], config["imagenet_std"])
    x = transform(image).unsqueeze(0)

    with torch.no_grad():
        logits = model(x)
        probs = torch.softmax(logits, dim=1).squeeze().tolist()

        prediction_index = int(torch.argmax(torch.tensor(probs)))
        prediction = config["classes"][prediction_index]

    return {
                "prediction": prediction,
                "probabilites": {
                    config["classes"][0]: probs[0],
                    config["classes"][1]: probs[1]
                }
            }
         