import flwr as fl

from ServerUtils.saveUtils import save_model, save_results


class FedProx(fl.server.strategy.FedProx):
    """自定义策略，包含模型保存和指标跟踪"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # def initialize_parameters(self, client_manager: ClientManager) -> Optional[Parameters]:
    #     model = get_resnet50()
    #     params = [val.cpu().numpy() for _, val in model.state_dict().items()]
    #     return ndarrays_to_parameters(params)

    def aggregate_fit(self, server_round, results, failures):
        # 保存每一个Client的参数
        prefix = "Training"
        # save_results_by_Client(server_round, results, prefix,"FedProx")
        # 聚合
        aggregated_parameters, metrics = super().aggregate_fit(server_round, results, failures)
        # 保存聚合模型和参数
        save_model(aggregated_parameters, server_round)
        save_results(server_round, metrics, prefix,"FedProx")

        return aggregated_parameters, metrics

    def aggregate_evaluate(self, server_round, results, failures):
        """聚合评估结果"""
        prefix = "Validation"
        # save_results_by_Client(server_round, results, prefix,"FedProx")
        loss_aggregated, metrics_aggregated = super().aggregate_evaluate(server_round, results, failures)
        save_results(server_round, metrics_aggregated, prefix,"FedProx")
        return loss_aggregated, metrics_aggregated