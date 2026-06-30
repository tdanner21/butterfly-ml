import torch
import torch.nn as nn
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader, random_split
import os

# Configuration
DATA_DIR = "data/raw"
MODEL_DIR = "models"
BATCH_SIZE = 32
NUM_EPOCHS_BASELINE = 10
NUM_EPOCHS_FINETUNE = 10
LEARNING_RATE = 0.001
FINETUNE_LR = 0.0001
VAL_SPLIT = 0.15
TEST_SPLIT = 0.15
NUM_CLASSES = 41

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {DEVICE}")

# Transforms
train_transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(15),
    transforms.ColorJitter(brightness=0.2, contrast=0.2),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                        std=[0.229, 0.224, 0.225])
])

val_transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                        std=[0.229, 0.224, 0.225])
])

# Load dataset
full_dataset = datasets.ImageFolder(DATA_DIR, transform=train_transforms)
print(f"Total images: {len(full_dataset)}")

# Split dataset
total = len(full_dataset)
test_size = int(TEST_SPLIT * total)
val_size = int(VAL_SPLIT * total)
train_size = total - val_size - test_size

train_dataset, val_dataset, test_dataset = random_split(
    full_dataset, [train_size, val_size, test_size]
)

val_dataset.dataset.transform = val_transforms
test_dataset.dataset.transform = val_transforms

print(f"Train: {train_size}, Val: {val_size}, Test: {test_size}")

train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False)
test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)

# Load model
model = models.efficientnet_b0(weights=models.EfficientNet_B0_Weights.DEFAULT)

for param in model.parameters():
    param.requires_grad = False

model.classifier = nn.Sequential(
    nn.Dropout(p=0.4),
    nn.Linear(model.classifier[1].in_features, NUM_CLASSES)
)

model = model.to(DEVICE)
print("Model loaded.")

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.classifier.parameters(), lr=LEARNING_RATE)

# Phase 1: Baseline training
print("\n=== PHASE 1: BASELINE TRAINING ===\n")
for epoch in range(NUM_EPOCHS_BASELINE):
    model.train()
    train_loss = 0.0
    train_correct = 0
    train_total = 0

    for images, labels in train_loader:
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
    print(f"Epoch {epoch+1}/{NUM_EPOCHS_BASELINE} - "
          f"Train Acc: {train_acc:.1f}%, Val Acc: {val_acc:.1f}%")

# Phase 2: Fine-tuning
print("\n=== PHASE 2: FINE-TUNING ===\n")

for name, param in model.named_parameters():
    if any(block in name for block in ['features.6', 'features.7', 'features.8', 'classifier']):
        param.requires_grad = True
    else:
        param.requires_grad = False

optimizer = torch.optim.Adam(
    filter(lambda p: p.requires_grad, model.parameters()),
    lr=FINETUNE_LR
)

trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
print(f"Trainable parameters for fine-tuning: {trainable:,}")

for epoch in range(NUM_EPOCHS_FINETUNE):
    model.train()
    train_loss = 0.0
    train_correct = 0
    train_total = 0

    for images, labels in train_loader:
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
    print(f"Epoch {epoch+1}/{NUM_EPOCHS_FINETUNE} - "
          f"Train Acc: {train_acc:.1f}%, Val Acc: {val_acc:.1f}%")

# Per-class accuracy evaluation
model.eval()
class_correct = [0] * NUM_CLASSES
class_total = [0] * NUM_CLASSES

with torch.no_grad():
    for images, labels in val_loader:
        images, labels = images.to(DEVICE), labels.to(DEVICE)
        outputs = model(images)
        _, predicted = outputs.max(1)

        for i in range(len(labels)):
            label = labels[i].item()
            class_correct[label] += (predicted[i] == labels[i]).item()
            class_total[label] += 1

print("\nPer-class accuracy:\n")
classes = full_dataset.classes
for i in range(NUM_CLASSES):
    if class_total[i] > 0:
        acc = 100 * class_correct[i] / class_total[i]
        print(f"{classes[i]}: {acc:.1f}% ({class_correct[i]}/{class_total[i]})")

# Save model
os.makedirs(MODEL_DIR, exist_ok=True)
torch.save(model.state_dict(), os.path.join(MODEL_DIR, "finetuned.pth"))
print("\nModel saved.")