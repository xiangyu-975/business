import time

from rpc import reco_pb2


def feed_article(stub):
    # 构建rpc调用的调用参数
    user_request = reco_pb2.UserRequest()
    user_request.user_id = '1'
    user_request.channel_id = 1
    user_request.article_num = 10
    user_request.time_stamp = round(time.time() * 1000)
