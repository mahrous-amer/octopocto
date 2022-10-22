import os
import sys
import json
import logging
from numpy import sign
from redis.exceptions import ConnectionError, DataError, NoScriptError, RedisError, ResponseError
from redis.cluster import RedisCluster as redis

logger = logging.getLogger(__name__)

class Redis:

  def __init__(self, name):
    self.name = name.upper()
    self.group = 'G_'+name.upper()
    self.consumer = 'C_'+name.upper()
    self.prefix = 'OCTOCRYPTO::PYTHON::'
    self.cluster = None
    self.wait_time = None
    self.batch_count = None

  def apply_prefix(self, key):
    if key.find(self.prefix) != -1:
      return key
    else:
      return self.prefix + key

  def remove_prefix(self, key):
    ind = key.find(self.prefix);
    return key[ind:-1]

  def compare_id(x='0-0', y='0-0'):
    if x == y :
      return 0
    else :
      first = x.split('-',2)
      second = y.split('-',2)
      cmp = sign(first[0]-second[0])
      cmp2 = sign(first[1]-second[1])
    return cmp or cmp2

  def next_id(id):
    (left, right) = id.split('-', 2)
    return left + '-' + str(int(right)+1)

  def connect(self):
    try:
       self.cluster = redis.from_url(os.environ['REDIS'], decode_responses=True)
    except Exception as e:
      raise e

  def get_nodes(self):
    try:
        return self.cluster.get_nodes()
    except Exception as e:
      raise e

  def close(self):
    try:
        self.cluster.close()
    except Exception as e:
      raise e

  def exec(self, command, args):
    try:
      return self.cluster.execute_command(command)
    except Exception as e:
      raise e

  # async def cleanup():
  # TODO

  # async def watch_keyspace():
  # TODO

  def create_stream(stream):
    self.create_group(self.apply_prefix(stream));
    self.remove_group(self.apply_prefix(stream));
    logger.info('Created a Redis stream: %s', stream);

  def xadd(self, stream, fields, nomkstream=False):
    try:
      res = self.cluster.xadd(self.apply_prefix(stream), fields, id="*", nomkstream=nomkstream)
      logger.info(self.apply_prefix(stream) + ' ' + str( res ))
      return res
    except Exception as e:
      raise e

  def xreadgroup(self, stream):
    try:
      res = self.cluster.xreadgroup(self.group, self.consumer, {self.apply_prefix(stream):'>'}, count=1)
      return res
    except Exception as e:
      if str(e).find('NOGROUP') != -1:
        try:
          self.create_group(self.apply_prefix(stream))
          return self.cluster.xreadgroup(self.group, self.consumer, {self.apply_prefix(stream):'>'}, count=1)
        except Exception as ex:
          raise ex
      raise e

  def create_group(self, stream):
    try:
      self.cluster.xgroup_create(self.apply_prefix(stream), self.group, '$', True)
      self.cluster.xgroup_createconsumer(self.apply_prefix(stream), self.group, self.consumer)
    except ResponseError as e:
      raise e

  def remove_group(self, stream):
    try:
      self.cluster.xgroup_destroy(self.apply_prefix(stream), self.group)
    except ResponseError as e:
      raise e

  def group_info(self, stream):
    res = self.cluster.xinfo_groups( name=self.apply_prefix(stream) )
    for i in res:
      logger.info( f"{stream} -> group name: {i['name']} with {i['consumers']} consumers and {i['last-delivered-id']}" + f" as last read id")

  # async def pending():
  # TODO

  # async def pending_messages_info():
  # TODO

  # async def stream_length():
  # TODO

  # async def stream_info(self, steam):
  # TODO

  # async def oldest_processed_id(self, stream):
  # TODO

  def ack(self, stream, msg_ids):
    try:
      self.cluster.xack(self.apply_prefix(stream), self.group, msg_ids)
    except Exception as e:
      raise e

  def set(self, key, val):
    try:
      return self.cluster.set(key, str(val))
    except Exception as e:
      raise e

  def get(self, key):
    try:
      return self.cluster.get(key)
    except Exception as e:
      raise e

  def publish():
    try:
      return self.cluster.publish(msg_id)
    except Exception as e:
      raise e

  def subscribe():
    try:
      return self.cluster.subscribe(msg_id)
    except Exception as e:
      raise e

  def incr():
    try:
      return self.cluster.incr(msg_id)
    except Exception as e:
      raise e

  def rpush():
    try:
      return self.cluster.rpush(msg_id)
    except Exception as e:
      raise e

  def lpush():
    try:
      return self.cluster.lpush(msg_id)
    except Exception as e:
      raise e

  def rpop():
    try:
      return self.cluster.rpop(msg_id)
    except Exception as e:
      raise e

  def lpop():
    try:
      return self.cluster.lpop(msg_id)
    except Exception as e:
      raise e

  def hset():
    try:
      return self.cluster.hset(msg_id)
    except Exception as e:
      raise e

  def hget():
    try:
      return self.cluster.hget(msg_id)
    except Exception as e:
      raise e

  def hincrby():
    try:
      return self.cluster.hincrby(msg_id)
    except Exception as e:
      raise e

  def zadd():
    try:
      return self.cluster.zadd(msg_id)
    except Exception as e:
      raise e

  def zrem():
    try:
      return self.cluster.zrem(msg_id)
    except Exception as e:
      logger.warn(e)

  def zremrangebyscore():
    try:
      return self.cluster.zremrangebyscore(msg_id)
    except Exception as e:
      logger.warn(e)

  def zcount():
    try:
      return self.cluster.zcount(msg_id)
    except Exception as e:
      logger.warn(e)

  def zrange():
    try:
      return self.cluster.zrange(msg_id)
    except Exception as e:
      logger.warn(e)
