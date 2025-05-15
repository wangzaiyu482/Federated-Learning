import logging

from flwr.client import start_client

from Client import client_fn


def start_client_process(client_id: int, server_addr: str):
    """启动单个客户端进程"""
    logging.basicConfig(level=logging.INFO,format=f"%(asctime)s [Client {client_id}] %(message)s")

    try:
        start_client(server_address=server_addr,client=client_fn(client_id))
    except Exception as e:
        logging.error(f"Client {client_id} failed: {str(e)}")