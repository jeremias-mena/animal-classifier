import json
import torch
from torchvision import models

def load_model(model_path, device):
    with open(f"{model_path}/config.json") as f:
        config = json.load(f)
    
    model = models.resnet50(weights=None)
    model.fc = torch.nn.Linear(2048, len(config["classes"]))

    state_dict = torch.load(f"{model_path}/resnet50_best.pt", map_location=device, weights_only=True)

    model.load_state_dict(state_dict["model_state"])
    model.to(device)
    model.eval()

    return model, config