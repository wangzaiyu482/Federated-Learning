import re
from typing import Dict, List, Tuple

import numpy as np
from flwr.common import Scalar


def parse_matrix_string(matrix_str: str) -> np.ndarray:
    cleaned = re.sub(r"[^\d\.\-\s]", " ", matrix_str)
    # 提取所有数字（包括浮点数和负数）
    numbers = re.findall(r"-?\d+\.\d+|-?\d+", cleaned)
    # 转换为 int 并 reshape
    return np.array([int(x) for x in numbers]).reshape(2, 2)

def weighted_average(metrics: List[Tuple[int, Dict]]) -> Dict:
    total_examples = sum(num_examples for num_examples, _ in metrics)
    weighted_metrics = {
        'accuracy': 0.0,
        'loss': 0.0,
        'recall': 0.0,
        'precision': 0.0,
        'F1': 0.0,
        'matrix': np.zeros((2, 2))  # 初始化混淆矩阵（数值格式）
    }

    for num_examples, metric in metrics:
        # 计算常规指标的加权和
        for key in ['accuracy', 'loss', 'recall', 'precision', 'F1']:
            if key in metric:
                weighted_metrics[key] += num_examples * metric[key]

        # 解析混淆矩阵字符串并加权求和
        if 'matrix' in metric:
            try:
                matrix = parse_matrix_string(metric['matrix'])  # 安全解析
                weighted_metrics['matrix'] += matrix
            except Exception as e:
                print(f"解析矩阵失败: {e}")
                continue

    # 计算加权平均值
    for key in ['accuracy', 'loss', 'recall', 'precision', 'F1']:
        if key in weighted_metrics:
            weighted_metrics[key] /= total_examples

    # 将混淆矩阵转换为字符串格式（保持原格式）
    weighted_metrics['matrix'] = str(weighted_metrics['matrix'].tolist())

    return weighted_metrics


def fit_config(rnd: int) -> Dict[str, Scalar]:
    """返回训练配置"""
    from Config.config import FEDERATED_CONFIG
    return {"num_epochs": FEDERATED_CONFIG['num_epochs']}


# metrics = [
#     (1760, {'F1': 60.96590757369995, 'matrix': '[[722. 394.]\n [293. 351.]]', 'accuracy': 59.5992237329483, 'loss': 0.6397156433625655, 'recall': 60.96590757369995, 'precision': 60.96590757369995}),
#     (1760, {'F1': 60.624998807907104, 'matrix': '[[809. 463.]\n [230. 258.]]', 'accuracy': 58.234742283821106, 'loss': 0.6408441045067527, 'recall': 60.624998807907104, 'precision': 60.624998807907104}),
#     (1760, {'F1': 58.92045497894287, 'matrix': '[[796. 486.]\n [237. 241.]]', 'accuracy': 56.25444948673248, 'loss': 0.6546976869756526, 'recall': 58.92045497894287, 'precision': 58.92045497894287}),
#     (1760, {'F1': 59.090906381607056, 'matrix': '[[833. 487.]\n [233. 207.]]', 'accuracy': 55.0757572054863, 'loss': 0.6513589533892545, 'recall': 59.090906381607056, 'precision': 59.090906381607056})
# ]
# print(weighted_average(metrics))
