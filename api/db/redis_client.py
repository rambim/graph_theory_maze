from redis import Redis
from config.config import Config
import os

_redis_client = None

config = Config ()

def get_redis_client () -> Redis:
  global _redis_client

  if _redis_client is None:
    _redis_client = Redis (
      host = config.GTM_REDIS_HOST,
      port = config.GTM_REDIS_PORT
    )

  return _redis_client