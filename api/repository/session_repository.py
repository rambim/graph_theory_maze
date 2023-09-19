from abc import ABC, abstractmethod
from redis import Redis
from fastapi import Depends

from api.schemas.position import Position
from api.db.redis_client import get_redis_client

class ISessionRepository (ABC):

  @abstractmethod
  def get_session_by_id (self, id: str) -> dict:
    raise NotImplemented ()

  @abstractmethod
  def create_session (self, session_id: str, maze_id: str, session_ttl: int, actual_position: int) -> str:
    raise NotImplemented ()

  @abstractmethod
  def update_actual_node (self, session_id: str, maze_id: str, new_position: int) -> int:
    raise NotImplemented ()


class RedisSessionRespositoryImpl (ISessionRepository):

  def __init__ (self, redis_client: Redis = Depends (get_redis_client)):
    self.redis_client = redis_client

  def get_session_by_id (self, session_id: str, maze_id: str) -> dict:
    return self.redis_client.hgetall (
      session_id + maze_id
    )

  def update_actual_node (self, session_id: str, maze_id: str, new_position: int) -> int:
    key = session_id + maze_id

    self.redis_client.hset (
      name = key,
      key = 'actual_position',
      value = new_position
    )

    return int (self.redis_client.hget (
      name = key,
      key = 'actual_position'
    ))

  def create_session (self, session_id: str, maze_id: str, session_ttl: int, actual_position: int) -> str:
    key: str = session_id + maze_id

    self.redis_client.hset (
      name = key,
      mapping = {
        'actual_position': actual_position
      }
    )

    self.redis_client.expire (
      name = key,
      time = session_ttl
    )

    return key if self.redis_client.hlen (name = key) > 0 else ''