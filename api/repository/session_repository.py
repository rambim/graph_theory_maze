from abc import ABC, abstractmethod
from redis import Redis
from fastapi import Depends

from api.schemas.position import Position
from api.db.redis_client import get_redis_client

class ISessionRepository (ABC):

  @abstractmethod
  def get_session_by_id (self, id: str) -> str:
    raise NotImplemented ()

  @abstractmethod
  def create_session (self, id: str) -> str:
    raise NotImplemented ()

  @abstractmethod
  def update_actual_node (self, id: str, actual_node: int) -> int:
    raise NotImplemented ()


class RedisSessionRespositoryImpl (ISessionRepository):

  def __init__ (self, redis_client: Redis = Depends (get_redis_client)):
    self.redis_client = redis_client

  def get_session_by_id(self, id: str) -> str:
    return super().get_session_by_id(id)

  def update_actual_node(self, id: str, actual_node: int) -> int:
    return super().update_actual_node(id, actual_node)

  def create_session (self, session_id: str, maze_id: str, session_ttl: int) -> str:
    key: str = session_id + maze_id

    self.redis_client.hset (
      name = key,
      mapping = {
        'actual_position': 1
      }
    )

    self.redis_client.expire (
      name = key,
      time = session_ttl
    )

    return key if self.redis_client.hlen (name = key) > 0 else ''