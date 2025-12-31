import torch

def accuracy(preds, labels):
    _, preds = torch.max(preds, 1)
    return (preds == labels).float().mean().item()