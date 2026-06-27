import torch
import torch.nn as nn
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader, random_split
import os

# Configuration
DATA_DIR = "data/raw"
MODEL_DIR = "models"
BATCH_SIZE = 32
NUM_EPOCHS = 1
LEARNING_RATE = 0.001
VAL_SPLIT = 0.15
TEST_SPLIT = 0.15
NUM_CLASSES = 41

# Use GPU if avaliable, otherwise CPU
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {DEVICE}")

# Data transforms
train_transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(15),
    transforms.ColorJitter(brightness=0.2, contrast=0.2),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

val_transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Load dataset
full_dataset = datasets.ImageFolder(DATA_DIR, transform = train_transforms)
print(f"Total images: {len(full_dataset)}")
print(f"Classes: {full_dataset.classes}")

# Split dataset into train, validation, and test
total = len(full_dataset)
test_size = int(TEST_SPLIT * total)
val_size = int(VAL_SPLIT * total)
train_size = total - val_size - test_size

train_dataset, val_dataset, test_dataset = random_split(
    full_dataset, [train_size, val_size, test_size]
)

# Apply validation transforms to val and test sets
val_dataset.dataset.transform = val_transforms
test_dataset.dataset.transform = val_transforms

print(f"Train: {train_size}, Val: {val_size}, Test: {test_size}")

# Create data loaders
train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False)
test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)

# Load pre-trained EfficientNet
model = models.efficientnet_b0(weights=models.EfficientNet_B0_Weights.DEFAULT)

# Freeze all pretrained layers
for param in model.parameters():
    param.requires_grad = False

# Replace the classification head with one for our 41 classes
model.classifier = nn.Sequential(
    nn.Dropout(p=0.2),
    nn.Linear(model.classifier[1].in_features, NUM_CLASSES)
)

model = model.to(DEVICE)
print(f"Model loaded. Output classes: {NUM_CLASSES}")

# Loss function and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.classifier.parameters(), lr=LEARNING_RATE)

# Training loop
os.makedirs(MODEL_DIR, exist_ok = True)

for epoch in range(NUM_EPOCHS):
    # training phase
    model.train()
    train_loss = 0.0
    train_correct = 0
    train_total = 0

    for batch_idx, (images, labels) in enumerate(train_loader):
        if batch_idx % 20 == 0:
            print(f"Batch {batch_idx}/{len(train_loader)}")
        images, labels = images.to(DEVICE), labels.to(DEVICE)

        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        train_loss += loss.item()
        _, predicted = outputs.max(1)
        train_total += labels.size(0)
        train_correct += predicted.eq(labels).sum().item()

    # validation phase

    model.eval()
    val_loss = 0.0
    val_correct = 0
    val_total = 0

    with torch.no_grad():
        for images, labels in val_loader:
            images, labels = images.to(DEVICE), labels.to(DEVICE)
            outputs = model(images)
            loss = criterion(outputs, labels)

            val_loss += loss.item()
            _, predicted = outputs.max(1)
            val_total += labels.size(0)
            val_correct += predicted.eq(labels).sum().item()

    train_acc = 100. * train_correct / train_total
    val_acc = 100. * val_correct / val_total
    print (f"Epoch {epoch + 1}/{NUM_EPOCHS} - "
           f"Train Loss: {train_loss/len(train_loader):.3f}, "
           f"Train Acc: {train_acc:.1f}%, "
           f"Val Loss: {val_loss/len(val_loader):.3f}, "
           f"Val Acc: {val_acc:.1f}%")
    
# save the model
torch.save(model.state_dict(), os.path.join(MODEL_DIR, "baseline.pth"))
print("Model saved.")