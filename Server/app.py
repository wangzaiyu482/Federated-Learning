import multiprocessing
from flask_cors import CORS  # 导入CORS模块
from flask import Flask, jsonify
import startServer

app = Flask(__name__)
CORS(app)  # 允许所有域名跨域访问

@app.route('/run-script', methods=['GET'])
def run_script():
    result = {
        "result": '服务端启动成功'
    }
    try:
        p = multiprocessing.Process(target=startServer.start_server)
        p.start()
    except Exception as e:
        result["result"] = "服务端启动失败"
        result["error"] = str(e)
    return jsonify(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12345)  # 启动服务