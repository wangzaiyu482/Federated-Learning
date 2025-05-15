from collections import OrderedDict

import flwr as fl
import torch

from Config.RedisConfig import redis
from model.ResnetModel import get_resnet50

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
net = get_resnet50().to(device)



def save_model(parameters, server_round):
    """保存模型到文件"""
    model_path = f"result/saved_models/fed_avg_model_round_{server_round}.pth"
    try:
        # 检查参数是否为空
        if parameters is None:
            raise ValueError("The provided parameters are empty. Cannot save an empty model.")
        print(f"Saving round {server_round} aggregated_parameters...")
        # Convert `Parameters` to `list[np.ndarray]`
        aggregated_ndarrays = fl.common.parameters_to_ndarrays(parameters)
        # Convert `list[np.ndarray]` to PyTorch `state_dict`
        params_dict = zip(net.state_dict().keys(), aggregated_ndarrays)
        state_dict = OrderedDict({k: torch.tensor(v) for k, v in params_dict})
        net.load_state_dict(state_dict, strict=True)

        # Save the model to disk
        torch.save(net.state_dict(), model_path)
    except Exception as e:
        print(f"Failed to save model")


def save_results_by_Client(server_round, results, prefix,clazz):
    for client_index, (_, res) in enumerate(results):
        key = f"{clazz}:Round {server_round}:Client{client_index}({prefix});"
        value = str(res.metrics)
        redis.set(key, value)
        print(key + value)


def save_results(server_round, metrics, prefix,clazz):
    key = f"{clazz}:Round {server_round} aggregate({prefix})"
    value = str(metrics)
    redis.set(key, value)
    print(key + value)
