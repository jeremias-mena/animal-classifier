import torch
from torchvision import transforms

def accuracy(preds, labels):
    _, preds = torch.max(preds, 1)
    return (preds == labels).float().mean().item()

def get_transformer(mean, std, resize_shape):
    return transforms.Compose([transforms.Resize(resize_shape),
                               transforms.ToTensor(),
                               transforms.Normalize(mean=mean, std=std)
                               ])