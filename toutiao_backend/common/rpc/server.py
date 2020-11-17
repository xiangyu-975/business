import time
from concurrent.futures import ThreadPoolExecutor

import grpc
import reco_pb2_grpc
from rpc import reco_pb2


# rpc接口定义中服务对应成Python的类
class UserRecommendService(reco_pb2_grpc.UserRecommendService):
    # 在接口定义的同名方法中补全，被调用时应该执行的逻辑
    def user_recommend(self, request, context):
        # request 调用的是请求数据的对象
        user_id = request.user_id
        channel_id = request.channel_id
        article_num = request.article_num
        time_stamp = request.time_stamp

        response = reco_pb2.ArticleResponse()
        response.exposure = 'exposure param'
        response.time.stamp = round(time.time() * 1000)
        recommends = []
        for i in range(article_num):
            article = reco_pb2.Article()
            article.track.click = 'click param{}'.format(i + 1)
            article.track.collect = 'collect param{}'.format(i + 1)
            article.track.share = 'share param{}'.format(i + 1)
            article.track.read = 'read param{}'.format(i + 1)
            article.article_id = i + 1
            recommends.append(article)
        response.recommends.extend(recommends)
        # 最终返回一个结果
        return response


def serve():
    """
    创建rpc服务器
    :return:
    """
    # 创建一个rpc的服务器
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    # 向服务器中添加被调用的服务方法
    # reco_pb2_grpc.add_UserRecommendServicer_to_server(业务代码, server)
    reco_pb2_grpc.add_UserRecommendServicer_to_server(UserRecommendService(), server)

    # 微服务器绑定ip地址和端口
    server.add_insecure_port('127.0.0.1:8888')
    # 启动服务器运行
    server.start()
    # 防止服务器退出
    while True:
        time.sleep(10)


if __name__ == '__main__':
    serve()
