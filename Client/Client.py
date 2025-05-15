import torch
import torchvision
from flwr.client import NumPyClient
from flwr.common import NDArrays, Scalar
from torch import nn

from Utils.DatasetUtil import load_data
from Utils.DeeplearningUtils import validate, train


class FlowerClient(NumPyClient):
    def __init__(self, train_load, val_load, local_epochs, learning_rate):
        self.model = self._get_model()
        self.train_load = train_load
        self.val_load = val_load
        self.lr = learning_rate
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        self.local_epochs = local_epochs

    def _get_model(self) -> torch.nn.Module:
        """初始化ResNet50模型"""
        model = torchvision.models.resnet50(pretrained=False)  # 使用pretrained=False避免自动下载
        inchannel = model.fc.in_features
        model.fc = nn.Linear(inchannel, 1)
        # model = Model()
        return model

    def fit(
            self, parameters: NDArrays, config: dict[str, Scalar]
    ) -> tuple[NDArrays, int, dict[str, Scalar]]:
        self.set_parameters(parameters)
        results = train(self.model, self.train_load, self.local_epochs, self.lr, self.device)
        return self.get_parameters(config), len(self.train_load.dataset), results

    def evaluate(
            self, parameters: NDArrays, config: dict[str, Scalar]
    ) -> tuple[float, int, dict[str, Scalar]]:
        self.set_parameters(self.model)
        loss, results = validate(self.model, self.val_load, self.device)
        return loss, len(self.val_load.dataset),results

    def get_parameters(self, config):
        return [val.cpu().numpy() for _, val in self.model.state_dict().items()]

    def set_parameters(self, parameters):
        if isinstance(parameters, list):
            params_dict = zip(self.model.state_dict().keys(), parameters)
            state_dict = {k: torch.tensor(v) for k, v in params_dict}
            self.model.load_state_dict(state_dict, strict=True)
        else:
            self.model.load_state_dict(parameters.state_dict())

# TODO 增加指定数据集的功能
def client_fn(partition_id):
    num_partitions = 3
    batch_size = 32
    train_loader, val_loader = load_data(partition_id, num_partitions, batch_size)
    local_epochs = 1
    learning_rate = 0.01

    # Return Client instance
    return FlowerClient(train_loader, val_loader, local_epochs, learning_rate).to_client()
