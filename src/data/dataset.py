from torch.utils.data import Dataset

class CatsDogsDataset(Dataset):
    def __init__(self, hf_dataset, transform=None):
        self.dataset = hf_dataset
        self.transform = transform
    
    def __len__(self):
        return len(self.dataset)
    
    def __getitem__(self, index):
        item = self.dataset[index]
        image = item["image"].convert("RGB")
        label = item["labels"]

        if self.transform:
            image = self.transform(image)
        
        return image, label