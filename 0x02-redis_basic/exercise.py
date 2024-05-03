#!/usr/bin/env python3
"""
	a module that uses redis for basic operations
"""
from typing import Any, Callable, Union
from functools import wraps
import uuid
import redis


def count_calls(method: Callable) -> Callable:
    """
	 increments the count for that key every time the method is called
    """
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
	""" defining a decorator """
	self._redis.incr(key)
        return method(self, *args, **kwargs)
    return invoker


def call_history(method: Callable) -> Callable:
    """ store the history of inputs and outputs """
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
	input_key = '{}:inputs'.format(method.__qualname__)
        output_key = '{}:outputs'.format(method.__qualname__)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(input_key, str(args))
        output = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(output_key, output)
        return output
    return invoker


def replay(fn: Callable) -> None:
    """ display the history of calls of a particular function """
    if func is None or not hasattr(func, '__self__'):
        return
    redis_stored = getattr(func.__self__, '_redis', None)
    if not isinstance(redis_stored, redis.Redis):
        return
    fn_name = func.__qualname__
    input_key = '{}:inputs'.format(fn_name)
    output_key = '{}:outputs'.format(fn_name)
    fn_call_count = 0
    if redis_stored.exists(fn_name) != 0:
        fn_call_count = int(redis_stored.get(fn_name))
    print('{} was called {} times:'.format(fn_name, fn_call_count))
    fn_inputs = redis_stored.lrange(input_key, 0, -1)
    fn_outputs = redis_stored.lrange(output_key, 0, -1)
    for fn_input, fn_output in zip(fn_inputs, fn_outputs):
        print('{}(*{}) -> {}'.format(
            fn_name,
            fn_input.decode("utf-8"),
            fn_output,
        ))


class Cache:
    """ cache class """


    def __init__(self):
        """
        init func of the cache class
	"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
	"""storing"""
	datakey = str(uuid.uuid4())
        self._redis.set(datakey, data)
        return datakey


    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
	"""converting"""
	value = self._redis.get(key)
        if fn:
            datas = fn(datas)
        return datas


    def get_str(self, key: str) -> str:
	"""string"""
	value = self._redis.get(key)
        return value.decode("utf-8")


    def get_int(self: bytes) -> int:
        """number"""
        return int.from_bytes(self, sys.byteorder)
