import os
import sys
import logging
import asyncio
import async_timeout
from numpy import sign
from redis.exceptions import ConnectionError, DataError, NoScriptError, RedisError, ResponseError
from redis.asyncio.cluster import RedisCluster as redis

logger = logging.getLogger(__name__)

class Redis:

  def __init__(self, name):
    self.name = name
    self.group = 'g'+name
    self.prefix = 'octocrypto::py::'
    self.cluster = None
    self.wait_time = None
    self.batch_count = None

  def apply_prefix(self, key):
    if key.find(self.prefix):
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

  async def connect(self):
    try:
       self.cluster = await redis.from_url(os.environ['REDIS'])
    except Exception as e:
      logger.warn(e)

  async def get_nodes(self):
    try:
        return self.cluster.get_nodes()
    except Exception as e:
      logger.warn(e)

  async def close(self):
    try:
        await self.cluster.close()
    except Exception as e:
      logger.warn(e)

  async def exec(self, command, args):
    try:
      return await self.cluster.execute_command(command)
    except Exception as e:
      logger.warn(e)

  # async def cleanup():
  # TODO

  # async def watch_keyspace():
  # TODO

  async def create_stream(stream):
    await self.create_group(stream, 'INIT', '$', 1);
    await self.remove_group(stream, 'INIT');
    logger.info('Created a Redis stream: %s', stream);

  async def xadd(self, stream, fields, nomkstream=False):
    try:
      res = await self.cluster.xadd(self.apply_prefix(stream), fields, id="*", nomkstream=nomkstream)
      stream = self.apply_prefix(stream)
      return res
    except Exception as e:
      logger.warn(e)

  async def xreadgroup(self, key, gname, cname):
    try:
      res = await self.cluster.xreadgroup(groupname=gname, consumername=cname, block=10, count=2, streams={key:'>'})
      return res
    except Exception as e:
      logger.warn(e)

  async def create_group(stream, gname, start='$', mkstream=0):
    try:
      await self.cluster.xgroup_create( name=self.apply_prefix(stream), groupname=gname)
    except ResponseError as e:
      logger.warn(f"Raised: {e}")

  async def remove_group(stream, gname):
    try:
      await self.cluster.xgroup_destroy(self.apply_prefix(stream), gname)
    except ResponseError as e:
      logger.warn(f"Raised: {e}")

  async def group_info(key):
    res = self.cluster.xinfo_groups( name=self.apply_prefix(stream) )
    for i in res:
      logger.info( f"{key} -> group name: {i['name']} with {i['consumers']} consumers and {i['last-delivered-id']}" + f" as last read id")

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

  async def ack(self, msg_id):
    try:
      return await self.cluster.xack(msg_id)
    except Exception as e:
      logger.warn(e)

  async def set(self, key, val):
    try:
      return await self.cluster.set(key, str(val))
    except Exception as e:
      logger.warn(e)

  async def get(self, key):
    try:
      return await self.cluster.get(key)
    except Exception as e:
      logger.warn(e)

  async def publish():
    try:
      return await self.cluster.publish(msg_id)
    except Exception as e:
      logger.warn(e)

  async def subscribe():
    try:
      return await self.cluster.subscribe(msg_id)
    except Exception as e:
      logger.warn(e)

  async def incr():
    try:
      return await self.cluster.incr(msg_id)
    except Exception as e:
      logger.warn(e)

  async def rpush():
    try:
      return await self.cluster.rpush(msg_id)
    except Exception as e:
      logger.warn(e)

  async def lpush():
    try:
      return await self.cluster.lpush(msg_id)
    except Exception as e:
      logger.warn(e)

  async def rpop():
    try:
      return await self.cluster.rpop(msg_id)
    except Exception as e:
      logger.warn(e)

  async def lpop():
    try:
      return await self.cluster.lpop(msg_id)
    except Exception as e:
      logger.warn(e)

  async def hset():
    try:
      return await self.cluster.hset(msg_id)
    except Exception as e:
      logger.warn(e)

  async def hget():
    try:
      return await self.cluster.hget(msg_id)
    except Exception as e:
      logger.warn(e)

  async def hincrby():
    try:
      return await self.cluster.hincrby(msg_id)
    except Exception as e:
      logger.warn(e)

  async def zadd():
    try:
      return await self.cluster.zadd(msg_id)
    except Exception as e:
      logger.warn(e)

  async def zrem():
    try:
      return await self.cluster.zrem(msg_id)
    except Exception as e:
      logger.warn(e)

  async def zremrangebyscore():
    try:
      return await self.cluster.zremrangebyscore(msg_id)
    except Exception as e:
      logger.warn(e)

  async def zcount():
    try:
      return await self.cluster.zcount(msg_id)
    except Exception as e:
      logger.warn(e)

  async def zrange():
    try:
      return await self.cluster.zrange(msg_id)
    except Exception as e:
      logger.warn(e)
