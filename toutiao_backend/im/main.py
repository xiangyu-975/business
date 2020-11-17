import os

import eventlet

eventlet.monkey_patch()
import eventlet.wsgi
import sys
from server import app
import chat
import notify

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'common'))
# sys.argv 列表 保存了程序启动命令行的参数
# python main.py 8000
# sys.argv  --> ['main.py',8000]
if len(sys.argv) < 2:
    print('Usage:python main.py [port].')
    exit(1)
port = int(sys.argv[1])



# 创建eventlet服务器对象
# eventlet.wsgi.server(eventlet.listen(('', 8000)), app)
SERVER_ADDRESS = ('0.0.0.0', port)
listen_sock = eventlet.listen(SERVER_ADDRESS)
eventlet.wsgi.server(listen_sock, app)
