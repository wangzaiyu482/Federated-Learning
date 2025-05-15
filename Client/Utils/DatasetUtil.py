import pandas as pd
import torch
from PIL import Image
from torch.utils.data import Dataset, random_split, DataLoader
from torchvision import transforms


class CancerDataset(Dataset):
    def __init__(self, csv_file, root_dir, transform=None):
        self.data_frame = pd.read_csv(csv_file)
        self.data_frame['label'] = self.data_frame['label'].astype(str)
        self.data_frame['id'] = self.data_frame['id'].apply(lambda x: x + '.tif' if not x.endswith('.tif') else x)
        self.root_dir = root_dir
        self.transform = transform

    def __len__(self):
        return len(self.data_frame)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        img_name = self.data_frame.iloc[idx]['id']
        image = Image.open(f'{self.root_dir}/{img_name}')
        label = int(self.data_frame.iloc[idx]['label'])

        if self.transform:
            image = self.transform(image)
        return image, torch.tensor([label], dtype=torch.float32)


# 数据预处理
train_transform = transforms.Compose([
    transforms.Resize((48, 48)),
    transforms.RandomRotation(10),
    transforms.RandomHorizontalFlip(),
    transforms.RandomVerticalFlip(),
    transforms.ToTensor()
    # transforms.Normalize(mean=[0.4049, 0.0925, 0.3929], std=[0.4778, 0.5642, 0.4325])
])

val_transform = transforms.Compose([
    # transforms.Resize((48, 48)),
    transforms.ToTensor()
    # transforms.Normalize(mean=[0.4049, 0.0925, 0.3929], std=[0.4778, 0.5642, 0.4325])
])

# 定义全局变量
train_data = None

# TODO 增加数据非独立同分布功能
def load_data(partition_id: int, num_partitions: int, batch_size: int):
    csv_file_path = r"D:\Dataset\data\train_labels.csv"
    image_folder_path = r"D:\Dataset\data\train"
    global train_data
    # 如果全局变量未初始化，则加载完整训练集和测试集
    if train_data is None:
        train_data = CancerDataset(csv_file=csv_file_path, root_dir=image_folder_path, transform=train_transform)

    # 划分训练集为多个分区(IID划分)
    partition_sizes = [len(train_data) // num_partitions] * num_partitions
    remainder = len(train_data) % num_partitions
    for i in range(remainder):
        partition_sizes[i] += 1

    partitions = random_split(train_data, partition_sizes)

    # 获取当前分区的数据
    partition_data = partitions[partition_id]

    # 将当前分区划分为训练集和验证集(80%训练, 20%验证)
    train_size = int(0.8 * len(partition_data))
    val_size = int(0.2 * len(partition_data))
    t = len(partition_data) - train_size - val_size
    train_data, val_data, _ = random_split(partition_data, [train_size, val_size, t])

    # 创建数据加载器
    train_loader = DataLoader(
        train_data,
        batch_size=batch_size,
        shuffle=True,
        pin_memory=True
    )

    val_loader = DataLoader(
        val_data,  # 注意: 这里使用验证集作为"测试集"
        batch_size=batch_size,
        shuffle=False,
        pin_memory=True
    )

    return train_loader, val_loader
