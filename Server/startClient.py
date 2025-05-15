import subprocess

#新建子进程把绝对路径放进去
subprocess.run(["python",r"D:\pythonProject\Client\start.py"],capture_output=True,text=True)
