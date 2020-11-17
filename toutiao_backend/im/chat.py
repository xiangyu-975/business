from server import sio
import time


@sio.on('connect')
def on_connect(sid, environ):
    """
    与客户端建立好连接后执行
    :param sid:string sid 是socketio为当前连接客户端生成的识别io
    :param environ: dict 在连接握手时客户端发送过来的握手数据(HTTP报文解析之后的字典)
    :return:
    """
    # sio,emit中需要传参：事件类型，消息数据，接收人
    data = {
        'msg': 'hello',
        'timestamp': round(time.time() * 1000)
    }

    # 与前端约定好，聊天内容数据都定义为message类型
    sio.emit('message', data, room=sid)


@sio.on('message')
def on_message(sid, data):
    """
    与前端约定前端发送的聊天类型为message
    :param sid:string sid 是发送的聊天数据事件类型也是message类型
    :param data:data是客户端发送的信息数据
        与前端约定好 前端发送的数据格式也是
        {
        'msg':xx,
        'timestamp':xxx
        }
    :return:
    """
    # TODO 此处使用rpc调用聊天机器人系统  获取聊天恢复内容
    resp_data = {
        "msg": 'I have received your msg: {}'.format(data.get('msg')),
        "timestamp": round(time.time() * 1000)
    }
    sio.send(resp_data, room=sid)
    # sio.emit('message', resp_data, room=sid)
