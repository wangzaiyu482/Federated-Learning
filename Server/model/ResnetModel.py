import torchvision
from torch import nn


def get_resnet50():
    model = torchvision.models.resnet50(pretrained=False)  # 使用pretrained=False避免自动下载
    inchannel = model.fc.in_features
    model.fc = nn.Linear(inchannel, 1)
    return model

