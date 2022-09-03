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
    self.group = 'gname'+name
    self.cluster = None

  async def start(self):
    try:
      self.cluster = await redis.from_url('redis://data-redis-node-0:6379/0?decode_responses=True&health_check_interval=5')
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
      res = self.cluster.execute_command(command)
      logger.info(res)
      return res
    except Exception as e:
      logger.warn(e)

  async def xadd(self, key, val):
    try:
      res = await self.cluster.xadd(key, val)
      logger.info(f'{key}: {str(res)}')
      return res
    except Exception as e:
      logger.warn(f'{key}: {str(val)}')
      logger.warn(e)

  async def set(self, key, val):
    try:
      res = await self.cluster.set(key, str(val))
      logger.info(f'{key}: {str(res)}')
      return res
    except Exception as e:
      logger.warn(f'{key}: {str(val)}')
      logger.warn(e)

  async def xread(self, key, gname, cname):
    try:
      res = r.xreadgroup( groupname=gname, consumername=cname, block=10, count=2, streams={key:'>'})
      logger.info(res)
      return res
    except Exception as e:
      logger.warn(e)

  async def create_group(key, gname):
    try:
      self.cluster.xgroup_create( name=key, groupname=gname, id=0 )
    except ResponseError as e:
        print(f"raised: {e}")

  async def group_info(key):
    res = self.cluster.xinfo_groups( name=key )
    for i in res:
      logger.info( f"{key} -> group name: {i['name']} with {i['consumers']} consumers and {i['last-delivered-id']}" + f" as last read id")
