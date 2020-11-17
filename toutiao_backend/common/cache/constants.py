import random


class BaseCacheTTL(object):
    """
    缓存有效期
    为防止缓存雪崩 ，在设置缓存的有效期时采用不同有效期的方案
    通过增加随机值实现
    """
    # 有效期的基础值
    TTL = 2 * 60 * 60  # 由子路由设定
    MAX_DELTA = 10 * 60  # 有效期随机量最大上限偏差

    @classmethod
    def get_val(cls):
        return cls.TTL + random.randrange(0, cls.MAX_DELTA)


class UserProfileCacheTTL(BaseCacheTTL):
    """
    用户资料数据缓存时间，秒
    """
    TTL = 30 * 60


class UserNotExistsCacheTTL(BaseCacheTTL):
    """
    用户不存在的有效期
    """
    TTL = 5 * 60


class ArticleProfileCacheTTL(BaseCacheTTL):
    # 文章资料缓存有效期
    TTL = 60 * 60
