import socketio

RABBITMQ = 'amqp://python:rabbitmqpwd@localhost:5672/toutiao'
JWT_SECRET = 'TPmi4aLWRbyVq8zu9v82dWYW17/z+UvRnYTt4P6fAXA'
mgr = socketio.KombuManager(RABBITMQ)

# 作为im服务器的启动程序
# 创建socketio对象
# async_mode='eventlet'告知socketio 服务器使用eventlet协程服务器来托管运行
sio = socketio.Server(async_mode='eventlet', client_manager=mgr)
app = socketio.Middleware(sio)
