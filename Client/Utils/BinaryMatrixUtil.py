import torch
import numpy as np


class Matrix:
    def __init__(self, outputs, labels, matrix=None, num_classes=2):
        self.outputs = outputs.squeeze()
        self.labels = labels
        self.num_classes = num_classes
        if matrix is None:
            self.matrix = torch.zeros(num_classes, num_classes, dtype=torch.int64)
        else:
            self.matrix = matrix

    def confusion_matrix(self):
        # 二分类问题，使用 sigmoid 后判断阈值
        if self.num_classes == 2:
            outputs = (torch.sigmoid(self.outputs) > 0.5).float()
            for p, t in zip(outputs, self.labels):
                self.matrix[int(t.item()), int(p.item())] += 1  # 修正索引顺序
        else:
            # 多分类问题，使用 argmax 获取预测类别
            _, predicted = torch.max(self.outputs, 1)
            for p, t in zip(predicted, self.labels):
                self.matrix[int(t.item()), int(p.item())] += 1

    def get_matrix(self):
        return self.matrix

    def get_accuracy(self):
        """计算整体准确率"""
        matrix = self.matrix.cpu().numpy()
        return matrix.diagonal().sum() / matrix.sum() * 100 if matrix.sum() > 0 else 0

    def get_precision(self, class_idx=None):
        """计算精确率
        如果指定class_idx，则返回该类别的精确率
        否则返回所有类别的平均精确率
        """
        matrix = self.matrix.cpu().numpy()
        if class_idx is not None:
            tp = matrix[class_idx, class_idx]
            fp = matrix[:, class_idx].sum() - tp
            return tp / (tp + fp) * 100 if (tp + fp) > 0 else 0

        # 计算所有类别的平均精确率
        precisions = []
        for i in range(self.num_classes):
            tp = matrix[i, i]
            fp = matrix[:, i].sum() - tp
            precisions.append(tp / (tp + fp) * 100 if (tp + fp) > 0 else 0)
        return np.mean(precisions)

    def get_recall(self, class_idx=None):
        """计算召回率
        如果指定class_idx，则返回该类别的召回率
        否则返回所有类别的平均召回率
        """
        matrix = self.matrix.cpu().numpy()
        if class_idx is not None:
            tp = matrix[class_idx, class_idx]
            fn = matrix[class_idx, :].sum() - tp
            return tp / (tp + fn) * 100 if (tp + fn) > 0 else 0

        # 计算所有类别的平均召回率
        recalls = []
        for i in range(self.num_classes):
            tp = matrix[i, i]
            fn = matrix[i, :].sum() - tp
            recalls.append(tp / (tp + fn) * 100 if (tp + fn) > 0 else 0)
        return np.mean(recalls)

    def get_f1(self, class_idx=None):
        """计算F1分数
        如果指定class_idx，则返回该类别的F1分数
        否则返回所有类别的平均F1分数
        """
        p = self.get_precision(class_idx) / 100
        r = self.get_recall(class_idx) / 100
        return 2 * p * r / (p + r) * 100 if (p + r) > 0 else 0

    def get_string_matrix(self):
        matrix = np.array(self.matrix.cpu())
        return str(matrix)



