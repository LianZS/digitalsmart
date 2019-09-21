import redis
import json
from threading import Semaphore
from typing import Dict, Iterator, List


def check_state(func):
    """
    检查连接池是否关闭
    :param func:
    :return:
    """

    def wrapper(self, *args, **kwargs):
        if self._shutdown:
            raise RuntimeError('连接池已经关闭，无法创建新的连接')
        self._semaphore.acquire()
        result = func(self, *args, **kwargs)
        self._semaphore.release()

        return result

    return wrapper


class RedisCache(object):
    _instance = None
    _bool_instance_flag = False
    _shutdown = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._bool_instance_flag = True
        return cls._instance

    def __init__(self, max_workers=None):

        if RedisCache._bool_instance_flag:
            if max_workers is None:
                max_workers = 10
            if max_workers <= 0:
                raise ValueError("连接池必须大于0")
            self._max_workers = max_workers
            self._broken = False
            self._shutdown = False
            self._init_pool_()
            self._semaphore = Semaphore(max_workers)  # 解决并发时too many connect 错误

    def _init_pool_(self):
        """
        初始化连接池
        :return:
        """

        pool = redis.ConnectionPool(max_connections=self._max_workers, host='localhost', port=6379)
        self._redis_pool = redis.Redis(connection_pool=pool)

    @check_state
    def expire(self, name, time_interval) -> int:

        """
        设置有效时间
        :param name: 键名
        :param time_interval: 有效时间
        :return:
        """
        pipe = self._redis_pool.pipeline()
        result: int = self._redis_pool.expire(name, time_interval)
        pipe.execute()

        return result

    @check_state
    def ttl(self, name) -> int:
        """
        查看剩余有效期
        :param name: 键名
        :return:
        """

        result: int = self._redis_pool.ttl(name)
        return result

    @check_state
    def exit_key(self, key):
        result = self._redis_pool.exists(key)
        print(result)

    @check_state
    def get(self, name: str, *args):
        """

        :param name:键值
        :param start:起始索引
        :param end:结束索引
        :return:"""
        if isinstance(name, list):
            for key in name:
                if isinstance(key, bytes):
                    key = key.decode()
                result = self._redis_pool.get(key).decode()
                result = eval(result)
                if len(args) > 0:
                    data = dict()
                    for parem in args:
                        data[parem] = result[parem]
                    yield data
        else:
            result = self._redis_pool.get(name)
            if result is None:  # 不存在该key
                yield None


            else:
                result = result.decode()
                result = eval(result)
                if len(args) > 0:
                    data = dict()
                    for parem in args:
                        data[parem] = result[parem]
                    yield data
                else:
                    yield result

    @check_state
    def keys(self, pattern) -> List:
        keys = self._redis_pool.keys(pattern)
        return keys

    @check_state
    def strlen(self, name) -> int:
        """
        redis String 值长度
        :param name: 键名
        :return:
        """

        length: int = self._redis_pool.strlen(name)
        return length

    @check_state
    def hashget(self, key, data_key_name: str = None, data_value_name: str = None) -> Iterator[Dict]:
        """
          哈希查询
          :param key: 缓存键
          :param data_key_name: 数据的键名
          :param data_value_name: 数据的键值名
          :return:
          """

        result = self._redis_pool.hgetall(name=key)
        if data_key_name and data_value_name:
            for k in result.keys():  # 针对给原先的数据字典的键值添加名字的操作
                value = result[k].decode()
                k = k.decode()
                yield {data_key_name: k, data_value_name: value}
        else:
            data = dict()
            for k in result.keys():  #
                value = result[k].decode()
                k = k.decode()
                data[k] = value
            if len(data.keys()) == 0:
                yield None
            else:
                yield data

    @check_state
    def set(self, name, value) -> int:
        result = self._redis_pool.set(name=name, value=value)
        return result

    @check_state
    def hashkeys(self, name) -> list:
        """
        获取所有哈希keys
        :param name:
        :return:
        """
        result: list = self._redis_pool.hkeys(name)
        return result

    @check_state
    def hlen(self, name) -> int:
        """
        哈希长度
        :param name:
        :return:
        """
        length = self._redis_pool.hlen(name)
        return length

    @check_state
    def lrange(self, name, start, end) -> list:
        """
        list左查询
        :param name:
        :param start:
        :param end:
        :return:
        """
        max_len = self.llen(name)
        if end > max_len:
            raise AttributeError("索引值过大")
        result: list = self._redis_pool.lrange(name, start, end)
        return result

    @check_state
    def llen(self, name):
        """
        list长度
        :param name:
        :return:
        """
        result: int = self._redis_pool.llen(name)
        return result

    @check_state
    def zset(self, name, mapping: dict):
        """
        set添加
        :param name:
        :param mapping: 键值对
        :return:
        """
        with self._redis_pool.pipeline() as pipe:
            try:

                pipe.watch(name)
                pipe.multi()
                resuslt: bool = pipe.zadd(name, mapping)
                pipe.execute()
                return resuslt

            except redis.exceptions.WatchError:
                print("%s --WatchError" % name)

    @check_state
    def zlen(self, name) -> int:
        """
        set长度
        :param name:
        :return:
        """
        length: int = self._redis_pool.zcard(name)
        return length

    def zrange_members(self, name) -> list:
        """
        获取zset里面的所有元素
        :param name:
        :return:
        """
        length = self._redis_pool.zcard(name)
        result: list = self._redis_pool.zrange(name, 0, length, withscores=True)
        return result

    def shutdown(self):
        """
        关闭连接池
        :return:
        """
        self._shutdown = True

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._redis_pool.connection_pool.disconnect()


