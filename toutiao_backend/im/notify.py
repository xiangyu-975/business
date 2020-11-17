from server import sio, JWT_SECRET
from werkzeug.wrappers import Request
import jwt


def verify_jwt(token, secret=None):
    """
    检验jwt
    :param token: jwt
    :param secret: 密钥
    :return: dict: payload
    """
    try:
        payload = jwt.decode(token, secret, algorithm=['HS256'])
    except jwt.PyJWTError:
        payload = None

    return payload


@sio.on('connect')
def on_connect(sid, environ):
    """
    与客户端建立好连接后执行
    :param sid: string sid是socketio为当前连接客户生成的识别id
    :param environ: dict 在连接握手数据(HTTP报文解析之后的字典)
    :return:
    """
    # 前端连接socketio服务器时候，携带的的查询字符串中包含的token 是随着第一次websocket握手的http报文携带
    # 可以通过environ取出
    # 借助werkzeug工具集 来帮助我们解读 客户端请求http数据
    request = Request(environ)
    # 对于接毒出来的request对象，可以像在flask中使用一样来读取数据
    token = request.args.get('token')
    if token is not None:
        payload = verify_jwt(token, JWT_SECRET)
        if payload is not None:
            user_id = payload.get('user_id')
            # 将用户加入用户id名称的房间
            sio.enter_room(sid, str(user_id))


@sio.on('disconnect')
def on_disconnect(sid):
    """
    客户端断开连接的时候
    :return:
    """
    # 查询sid存在的房间
    rooms = sio.rooms(sid)
    for room in rooms:
        # 将用户移除房间
        sio.leave_room(sid, room)
