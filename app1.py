import os
import cv2
import numpy as np
from PIL import Image
import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from tqdm import tqdm

# Define the transform to apply to each image
transform = transforms.Compose([
    transforms.Resize((640, 640)), # Resize the image to (640, 640)
    transforms.ToTensor() # Convert the image to a tensor
])

# Define the YOLOv5 dataset class
class YOLOv5Dataset(Dataset):
    def __init__(self, img_dir, label_dir, transform=None):
        self.img_dir = img_dir
        self.label_dir = label_dir
        self.transform = transform
        
        # Load the list of image and label files
        self.img_files = os.listdir(img_dir)
        self.label_files = os.listdir(label_dir)
        
    def __len__(self):
        return len(self.img_files)
    
    def __getitem__(self, idx):
        # Load the image
        img_path = os.path.join(self.img_dir, self.img_files[idx])
        img = Image.open(img_path)
        
        # Load the labels
        label_path = os.path.join(self.label_dir, self.label_files[idx])
        with open(label_path, 'r') as f:
            labels = f.readlines()
        labels = [label.strip().split() for label in labels]
        labels = np.array(labels, dtype=np.float32)
        
        # Apply the transform to the image
        if self.transform:
            img = self.transform(img)
            
        return img, labels
    
# Define a function to visualize the bounding boxes on the images
def visualize(img, boxes):
    img = np.array(img)
    for box in boxes:
        x1, y1, x2, y2 = box
        img = cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
    return img

# Define the paths to your image and label directories
img_dir = 'path/to/your/image/directory'
label_dir = 'path/to/your/label/directory'

# Create the YOLOv5 dataset
dataset = YOLOv5Dataset(img_dir, label_dir, transform=transform)

# Create the dataloader to load the data in batches
dataloader = DataLoader(dataset, batch_size=8, shuffle=True)

# Loop over the data and visualize a few samples
for batch in tqdm(dataloader):
    imgs, labels = batch
    for i in range(len(imgs)):
        img = transforms.ToPILImage()(imgs[i])
        boxes = labels[i][:, 1:] # Get the bounding boxes from the labels
        img = visualize(img, boxes)
        img.show()
