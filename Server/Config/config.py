import os

import yaml

from Config.MySQLConfig import FLConfigExporter

# 获取当前脚本所在的目录
script_dir = os.path.dirname(os.path.abspath(__file__))
# 构建 config.yaml 的绝对路径
config_path = os.path.join(script_dir, 'config.yml')

exporter = FLConfigExporter()

def getconfig():
    # 导出配置ID为1的记录
    config_id = 1  # 替换为您要导出的配置ID
    output_file = "Config/config.yml"  # 输出文件名

    if exporter.export_to_yml(config_id, output_file):
        print("导出成功！")
    else:
        print("导出失败")
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    return config

# 联邦学习配置
config = getconfig()
FEDERATED_CONFIG = config['federated']
