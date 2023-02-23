https://github.com/ultralytics/yolov5.git
export PYTHONPATH=$PYTHONPATH:/home/yourusername/yolov5  # Replace "yourusername" with your actual username
set PYTHONPATH=%PYTHONPATH%;C:\path\to\yolov5


import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import transforms
from yolov5.models.yolo import Model
from yolov5.utils.datasets import LoadImagesAndLabels, collate_fn

# Define the input and output directories
img_dir = "path/to/preprocessed/images"
label_dir = "path/to/preprocessed/annotations"

# Define the batch size and number of workers for data loading
batch_size = 8
num_workers = 4

# Define the transforms for data augmentation
transforms = transforms.Compose([
    transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.2),
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.RandomVerticalFlip(p=0.5),
    transforms.RandomRotation(degrees=10, resample=False, expand=False),
    transforms.Resize((416, 416)),
    transforms.ToTensor(),
])

# Load the images and annotations into a dataset
dataset = LoadImagesAndLabels(img_dir, label_dir, transform=transforms)

# Define the data loader
dataloader = DataLoader(dataset, batch_size=batch_size, num_workers=num_workers, collate_fn=collate_fn)

# Define the model
model = Model(num_classes=1)

# Define the optimizer and loss function
optimizer = optim.Adam(model.parameters(), lr=0.001)
loss_fn = nn.BCEWithLogitsLoss()

# Train the model for 10 epochs
num_epochs = 10
for epoch in range(num_epochs):
    for batch_idx, (images, targets, _) in enumerate(dataloader):
        optimizer.zero_grad()
        output = model(images)
        loss = loss_fn(output, targets)
        loss.backward()
        optimizer.step()
        print(f"Epoch {epoch+1}/{num_epochs}, Batch {batch_idx+1}/{len(dataloader)}, Loss: {loss.item():.4f}")
