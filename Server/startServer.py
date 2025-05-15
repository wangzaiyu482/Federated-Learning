import flwr as fl
import torch

from pathlib import Path
from Config.config import FEDERATED_CONFIG
from ServerUtils.fitUtils import weighted_average, fit_config
from Strategies.FedAvg import FedAvg
from Strategies.FedMedian import FedMedian
from Strategies.FedProx import FedProx
from Strategies.FedTrimmedAvg import FedTrimmedAvg
from model.CancerModel import CancerModel

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
net = CancerModel().to(device)


Path("result/saved_models").mkdir(exist_ok=True)
Path("result/metrics").mkdir(exist_ok=True)


def start_server():
    # 策略选择
    strategy_mapping = {
        "FedAvg": FedAvg,
        "FedProx": FedProx,
        "FedTrimmedAvg": FedTrimmedAvg,
        "FedMedian": FedMedian
    }

    selected_strategy = FEDERATED_CONFIG["strategy"]
    strategy_class = strategy_mapping.get(selected_strategy, FedAvg)

    common_args = {
        "fraction_fit": FEDERATED_CONFIG['fraction_fit'],
        "fraction_evaluate": FEDERATED_CONFIG['fraction_evaluate'],
        "min_fit_clients": FEDERATED_CONFIG['min_fit_clients'],
        "min_evaluate_clients": FEDERATED_CONFIG['min_evaluate_clients'],
        "min_available_clients": FEDERATED_CONFIG['min_available_clients'],
        "fit_metrics_aggregation_fn": weighted_average,
        "evaluate_metrics_aggregation_fn": weighted_average,
        "on_fit_config_fn": fit_config,
    }

    if selected_strategy == "FedTrimmedAvg":
        strategy = strategy_class(
            **common_args
        )
    elif selected_strategy == "FedProx":
        strategy = strategy_class(
            proximal_mu=FEDERATED_CONFIG['proximal_mu'],
            **common_args
        )
    else:
        strategy = strategy_class(**common_args)

    fl.server.start_server(
        server_address=FEDERATED_CONFIG['server_address'],
        config=fl.server.ServerConfig(num_rounds=FEDERATED_CONFIG['num_epochs']),
        strategy=strategy
    )


if __name__ == "__main__":
    start_server()