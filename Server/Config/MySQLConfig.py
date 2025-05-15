import mysql.connector
from dotenv import load_dotenv
import os
import yaml
from typing import Dict, Optional

# 加载环境变量
load_dotenv()


class FLConfigExporter:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),  # 默认值'localhost'
            user=os.getenv('DB_USER', 'root'),  # 默认值'root'
            password=os.getenv('DB_PASSWORD', '1234'),  # 默认值'1234'
            database=os.getenv('DB_NAME', 'fed')  # 默认值'fed'
        )

    def __del__(self):
        if hasattr(self, 'connection') and self.connection.is_connected():
            self.connection.close()

    def get_config_by_id(self, config_id: int) -> Optional[Dict]:
        """根据ID获取配置"""
        with self.connection.cursor(dictionary=True) as cursor:
            query = """
            SELECT 
                num_epochs, server_address,num_clients,
                fraction_fit, fraction_evaluate, min_fit_clients,
                min_evaluate_clients, min_available_clients,
                proximal_mu, client_lr, local_epochs, strategy
            FROM federated_learning_configs
            WHERE id = %s
            """
            cursor.execute(query, (config_id,))
            result = cursor.fetchone()
            return result

    def export_to_yml(self, config_id: int, output_path: str) -> bool:
        """导出配置到YAML文件"""
        config = self.get_config_by_id(config_id)
        if not config:
            print(f"未找到ID为 {config_id} 的配置")
            return False

        # 构建YAML结构
        yaml_data = {
            'federated': {
                'num_epochs': config['num_epochs'],
                'server_address': config['server_address'],
                'num_clients': config['num_clients'],
                'fraction_fit': config['fraction_fit'],
                'fraction_evaluate': config['fraction_evaluate'],
                'min_fit_clients': config['min_fit_clients'],
                'min_evaluate_clients': config['min_evaluate_clients'],
                'min_available_clients': config['min_available_clients'],
                'proximal_mu': config['proximal_mu'],
                'client_lr': config['client_lr'],
                'local_epochs': config['local_epochs'],
                'strategy': config['strategy']
            }
        }

        # 写入YAML文件
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                yaml.dump(yaml_data, f, sort_keys=False, allow_unicode=True)
            print(f"配置已成功导出到 {output_path}")
            return True
        except Exception as e:
            print(f"导出失败: {str(e)}")
            return False


