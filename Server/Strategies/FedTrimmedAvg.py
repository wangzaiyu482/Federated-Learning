"没有成功不知道原因"

import flwr as fl

from ServerUtils.saveUtils import save_model, save_results

clazz = "FedTrimmedAvg"

class FedTrimmedAvg(fl.server.strategy.FedTrimmedAvg):
    """带服务器动量的FedAvgM策略"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # def initialize_parameters(self, client_manager: ClientManager) -> Optional[Parameters]:
    #     model = get_resnet50()
    #     params = [val.cpu().numpy() for _, val in model.state_dict().items()]
    #     self.initial_parameters = params
    #     return super().initialize_parameters(client_manager)

    def aggregate_fit(self, server_round, results, failures):
        # 保存每一个Client的参数
        prefix = "Training"
        # save_results_by_Client(server_round, results, prefix, clazz)
        # 聚合
        aggregated_parameters, metrics = super().aggregate_fit(server_round, results, failures)
        # 保存聚合模型和参数
        save_model(aggregated_parameters, server_round)
        save_results(server_round, metrics, prefix, clazz)

        return aggregated_parameters, metrics

    def aggregate_evaluate(self, server_round, results, failures):
        """聚合评估结果"""
        prefix = "Validation"
        # save_results_by_Client(server_round, results, prefix,clazz)
        loss_aggregated, metrics_aggregated = super().aggregate_evaluate(server_round, results, failures)
        save_results(server_round, metrics_aggregated, prefix,clazz)
        return loss_aggregated, metrics_aggregated