from flask import current_app
import json
from sqlalchemy.orm import load_only
from sqlalchemy.exc import DatabaseError

from redis.exceptions import RedisError
from models.user import User
from . import constants


class UserProfileCache(object):
    """
    用户资料信息缓存
    """

    def __init__(self, user_id):
        self.key = 'user:{}:info'.format(user_id)
        self.user_id = user_id

    def save(self):
        """
        查询数据库  保存缓存数据
        :return:
        """
        r = current_app.redis_cluster  # redis_cluster 连接的客户端对象
        try:
            user = User.query.options(load_only(User.name,
                                                User.profile_photo,
                                                User.introduction,
                                                User.certificate)).filter_by(id=self.user_id).first()
        except DatabaseError as e:
            current_app.logger.error(e)
            # 因为已经无法查到数据 数据库出现异常 所以不能返回一个有效数据 工具类也不能私自决定如何处理 所以
            # 一个原则，自己抛出异常，交给服务器自己处理
            raise e

        # 判断结果是否存在
        # 数据保存进redis缓存中
        # 如果数据库中没有查到数据，为了防护缓存穿透，保存redis记录（-1），返回
        if user is None:
            try:
                r.setex(self.key, constants.UserNotExistsCacheTTL.get_val(), -1)
            except RedisError as e:
                current_app.logger.error(e)
            return None
        else:
            cache_data = {
                'name': user.name,
                'photo': user.profile_photo,
                'intro': user.introduction,
                'certi': user.certificate
            }
            user_json = json.dumps(cache_data)
            # 保存到redis中，
            # r.setex(键，有效期，值）
            # 缓存雪崩
            try:
                r.setex(self.key, constants.UserProfileCacheTTL.get_val(), user_json)
            except RedisError as e:
                current_app.logger.error(e)
            return cache_data


def get(self):
    """
    查询数据库的缓存数据
    :return:
    """
    r = current_app.redis_cluster  # redis_cluster 连接的客户端对象

    # 查询redis的缓存数据  redis_cluster
    # python3中从redis中取出的redis对应的字符串数据对应到python中是bytes类型
    try:
        ret = r.get(self.key)
    except RedisError as e:
        # 记录日志
        current_app.logger.error(e)
        # 虽然redis出现移常，但是还可以挽回 从数据库中尝试查询数据，所有设置re=None，让代码进入数据库查询
        ret = None
    # python3 从redis中取出redis 字符串类型的数据 对应到python中是bytes类型  # ret -> bytes类型
    if ret is not None:
        # 如果存在记录 ，读取
        if ret == b'-1':
            # 表示用户不存在
            return None
        else:
            # 用户存在,取出了用户的json字符串
            # json.loads是可以解析bytes类型，不需要转成json格式
            user_dict = json.loads(ret)
            return user_dict
    else:
        return self.save()


# 查询数据库


def clear(self):
    """
    删除缓存数据
    :return:
    """
    r = current_app.redis_cluster
    try:
        r.delete(self.key)
    except RedisError as e:
        current_app.logger.error(e)


def determine_user_exists(self):
    """
    判断用户是否存在
    :return:
    """
    # 查询redis记录
    r = current_app.redis_cluster
    try:
        ret = r.get(self.key)
    except RedisError as e:
        current_app.logger.error(e)
        ret = None
    if ret is not None:
        # 如果redis存在数据，返回
        if ret == b'-1':
            # 表示用户不存在
            return False
        else:
            return True
    else:
        # 如果redis不存在数据 查询数据库 顺带形成缓存数据
        result = self.save()
        if result is None:
            return False
        else:
            return True
