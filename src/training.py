import os
from torchvision import datasets, models, transforms
from torch.utils.data import DataLoader
import torch
import torch.nn as nn
import torch.optim as optim


import os
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, models, transforms
from torch.utils.data import DataLoader, random_split

from fixture.predefined_slots import MUMMY, REELS, DRAGON, MAJESTIC, BELLS, GANGSTER, BLAZINGFRUITS, MEGAREELS, DISCO, \
    REELSDELUXE, CRYSTALTREASURE, VULCAN, ICEDFRUITS


def train_icon_classifier(
    dataset_dir,
    output_model_path="model.pth",
    num_epochs=10,
    batch_size=32,
    lr=1e-4
):
    # Transformations
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406],
                             [0.229, 0.224, 0.225]),
    ])

    # Full dataset
    full_dataset = datasets.ImageFolder(root=dataset_dir, transform=transform)
    num_total = len(full_dataset)
    num_val = int(0.1 * num_total)
    num_train = num_total - num_val

    train_dataset, val_dataset = random_split(full_dataset, [num_train, num_val])
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size)

    # Model - resnet
    model = models.resnet18(pretrained=True)
    model.fc = nn.Linear(model.fc.in_features, len(full_dataset.classes))

    # Model - mobilenet
    # model = models.mobilenet_v2(pretrained=True)
    # model.classifier[1] = nn.Linear(model.classifier[1].in_features, len(full_dataset.classes))

    model = model.cuda()

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)

    # Training loop
    for epoch in range(num_epochs):
        model.train()
        train_loss, train_correct, train_total = 0, 0, 0
        for images, labels in train_loader:
            images, labels = images.cuda(), labels.cuda()
            outputs = model(images)
            loss = criterion(outputs, labels)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            train_loss += loss.item() * images.size(0)
            train_correct += (outputs.argmax(1) == labels).sum().item()
            train_total += labels.size(0)

        train_acc = train_correct / train_total
        train_loss /= train_total

        # Validation
        model.eval()
        val_loss, val_correct, val_total = 0, 0, 0
        with torch.no_grad():
            for images, labels in val_loader:
                images, labels = images.cuda(), labels.cuda()
                outputs = model(images)
                loss = criterion(outputs, labels)
                val_loss += loss.item() * images.size(0)
                val_correct += (outputs.argmax(1) == labels).sum().item()
                val_total += labels.size(0)

        val_acc = val_correct / val_total
        val_loss /= val_total

        print(f"Epoch {epoch+1}/{num_epochs} | "
              f"Train Loss: {train_loss:.4f}, Acc: {train_acc:.4f} | "
              f"Val Loss: {val_loss:.4f}, Acc: {val_acc:.4f}")

    # Save model and class names
    torch.save({
        'model': model.state_dict(),
        'classes': full_dataset.classes
    }, output_model_path)


if __name__ == '__main__':
    train_icon_classifier(dataset_dir=VULCAN.dataset_folder_path + '_augmented',
                          output_model_path=VULCAN.model_path)

