import torch
from tqdm import tqdm

from model.utils import accuracy

def train_one_epoch(model, loader, optimizer, criterion, device):
    model.train()
    epoch_loss, epoch_acc = 0.0, 0.0

    for images, labels in tqdm(loader, leave=False):
        images, labels = images.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        epoch_loss += loss.item()
        epoch_acc += accuracy(outputs, labels)

    return epoch_loss / len(loader), epoch_acc / len(loader)

@torch.no_grad()
def validate(model, loader, criterion, device):
    model.eval()
    epoch_loss, epoch_acc = 0.0, 0.0

    for images, labels in loader:
        images, labels = images.to(device), labels.to(device)
        outputs = model(images)
        loss = criterion(outputs, labels)

        epoch_loss += loss.item()
        epoch_acc += accuracy(outputs, labels)
    
    return epoch_loss / len(loader), epoch_acc / len(loader)