import multiprocessing

from Utils import startClientUtil

if __name__ == "__main__":
    # 配置参数
    NUM_CLIENTS = 3
    SERVER_ADDRESS = "127.0.0.1:8088"

    # 启动多个客户端
    processes = []
    for client_id in range(NUM_CLIENTS):
        p = multiprocessing.Process(target=startClientUtil.start_client_process,args=(client_id, SERVER_ADDRESS))
        p.start()
        processes.append(p)

    # 等待所有客户端完成
    for p in processes:
        p.join()