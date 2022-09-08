import sys
import logging
import asyncio
import async_timeout
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
    ind = key.find(self.prefix):
    return key[ind:-1]

  def compare_id(x='0-0', y='0-0'):
    return 0 if x = y
    first = x.split('-',2)
    second = y.split('-',2)
    return first[0] <=> second[0] or first[1] <=> second[1]

  def next_id(id):
    (left, right) = id.split('-', 2)
    return left + '-' + str(int(right)++)

  async def connect(self):
    try:
      redis = await redis.from_url('redis://data-redis-node-0:6379/0?decode_responses=True&health_check_interval=5')
      self.cluster = redis.intialize()
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

  async def cleanup():
  async def watch_keyspace():

  async def create_stream():

  async def xadd(self, key, val):
    try:
      res = await self.cluster.xadd(key, val)
      logger.info(f'{key}: {str(res)}')
      return res
    except Exception as e:
      logger.warn(f'{key}: {str(val)}')
      logger.warn(e)

  async def xreadgroup(self, key, gname, cname):
    try:
      res = r.xreadgroup(groupname=gname, consumername=cname, block=10, count=2, streams={key:'>'})
      logger.info(res)
      return res
    except Exception as e:
      logger.warn(e)

  async def create_group(key, gname):
    try:
      self.cluster.xgroup_create( name=key, groupname=gname, id=0 )
    except ResponseError as e:
        print(f"raised: {e}")

  async def remove_group():

  async def group_info(key):
    res = self.cluster.xinfo_groups( name=key )
    for i in res:
      logger.info( f"{key} -> group name: {i['name']} with {i['consumers']} consumers and {i['last-delivered-id']}" + f" as last read id")

  async def pending():
  async def pending_messages_info():
  async def stream_length():
  async def stream_info(self, steam):
  async def oldest_processed_id(self, stream):

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
