import torch
from torch.utils.data import random_split, DataLoader

import DeeplearningUtils
from DatasetUtil import CancerDataset,train_transform

csv_file_path = r"D:\Dataset\data\train_labels.csv"
image_folder_path = r"D:\Dataset\data\train"
dataset = CancerDataset(csv_file=csv_file_path, root_dir=image_folder_path, transform=train_transform)

train_size = int(0.8 * len(dataset))
val_size = len(dataset)-train_size
train_data, val_data = random_split(dataset, [train_size, val_size])

train_loader = DataLoader(train_data, batch_size=128, shuffle=True)
val_loader = DataLoader(val_data, batch_size=128, shuffle=False)

# 初始化
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 定义模型
# Resnet_Model = torchvision.models.resnet50(pretrained=True)
# # 将原来的ResNet18的最后两层全连接层拿掉,替换成一个输出单元为10的全连接层
# inchannel = Resnet_Model.fc.in_features
# Resnet_Model.fc = nn.Linear(inchannel, 1)
# model = Resnet_Model.to(device)

# model = task.Model().to(device)
model = torch.load("../model/resnet_model2.pth")
learning_rate = 0.001

train_losses = []
train_accuracies = []
val_losses = []
val_accuracies = []
for i in range(1, 4):
    print("-------------------------训练--------------------------------")
    print(f"第{i}轮")
    results,_ = DeeplearningUtils.train(model, train_loader, 1, learning_rate, device)
    train_losses.append(results["loss"])
    train_accuracies.append(results["accuracy"])

    loss, acc, _= DeeplearningUtils.validate(model, val_loader, device)
    val_losses.append(loss)
    val_accuracies.append(sum(acc) / len(acc))



torch.save(model, '../model/resnet_model2.pth')