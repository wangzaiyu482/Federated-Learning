import torch
import torch.nn as nn
from tqdm import tqdm

from Utils.BinaryMatrixUtil import Matrix

# TODO 增加功能传递优化器和损失函数
def train(model, train_loader, epochs, learning_rate, device):
    model.to(device)
    # 二分类使用 BCEWithLogitsLoss
    criterion = nn.BCEWithLogitsLoss().to(device)
    optimizer = torch.optim.SGD(model.parameters(), learning_rate)
    model.train()
    for i in range(epochs):
        train_loss = 0
        matrix = torch.zeros(2, 2)
        progress_bar = tqdm(train_loader)
        for j, (inputs, labels) in enumerate(progress_bar):
            inputs = inputs.to(device)
            labels = labels.to(device)
            # 拿到预测值计算损失值
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            train_loss += loss.item()
            # 优化开始梯度清零反向传播+更新
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            # 计算混淆矩阵
            m = Matrix(outputs, labels, matrix)
            m.confusion_matrix()
            progress_bar.set_postfix({'loss': train_loss / (j + 1), 'acc': m.get_accuracy()})
            progress_bar.refresh()
        # 输出值
        train_loss = train_loss / len(train_loader)
        # m.print_matrix()
        print(f"准确率为：{m.get_accuracy()}，损失为：{train_loss}")
    results = {
        "loss": train_loss,
        "accuracy": m.get_accuracy(),
        "precision":m.get_precision(),
        "recall": m.get_recall(),
        "F1": m.get_f1(),
        "matrix":m.get_string_matrix()
    }
    return results


def validate(model, test_loader, device):
    model.to(device)
    # 二分类使用 BCEWithLogitsLoss
    criterion = nn.BCEWithLogitsLoss()
    correct, loss = 0, 0.0
    matrix = torch.zeros(2, 2)
    with torch.no_grad():
        progress_bar = tqdm(test_loader, desc='Validation')
        for inputs, labels in progress_bar:
            inputs = inputs.to(device)
            labels = labels.to(device)
            # 拿到预测值计算损失值
            outputs = model(inputs)
            loss += criterion(outputs, labels).item()
            m = Matrix(outputs, labels, matrix)
            m.confusion_matrix()
            progress_bar.set_postfix({'loss': loss / (progress_bar.n + 1), 'acc': m.get_accuracy()})
            progress_bar.refresh()
    acc = m.get_accuracy()
    loss = loss / len(test_loader)
    results = {
        "loss": loss,
        "accuracy": m.get_accuracy(),
        "precision":m.get_precision(),
        "recall": m.get_recall(),
        "F1": m.get_f1(),
        "matrix":m.get_string_matrix()
    }
    print(f"准确率:{m.get_accuracy()}, 验证损失:{loss}")
    return loss, results




