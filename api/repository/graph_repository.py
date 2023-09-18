from abc import ABC, abstractmethod
from fastapi import Depends
from redis import Redis
from redisgraph import Node, Graph

from api.schemas.position import Position
from api.db.redis_client import get_redis_client

class IGraphRepository (ABC):

  @abstractmethod
  def get_start_node (self, maze_id: str) -> Position:
    raise NotImplemented ()

  @abstractmethod
  def get_end_node (self, maze_id: str) -> Position:
    raise NotImplemented ()

  @abstractmethod
  def get_neighbors_nodes (self, maze_id: str, actual_position: int) -> list [int]:
    raise NotImplemented ()


class RedisGraphRespoistoryImpl (IGraphRepository):
  def __init__ (self, redis_client: Redis = Depends (get_redis_client)):
    self.redis_client = redis_client

  def get_start_node (self, maze_id: str) -> Node:
    maze = Graph (
      maze_id,
      self.redis_client
    )

    result = maze.query (
      """MATCH (start_node:node {is_start: true}) return start_node"""
    )

    node: Node = result.result_set [0][0]

    # return node.properties ['node_id']

    return node


  def get_end_node (self, maze_id: str) -> Node:
    maze = Graph (
      maze_id,
      self.redis_client
    )

    result = maze.query (
      """MATCH (end_node:node {is_end: true}) return end_node"""
    )

    node: Node = result.result_set [0][0]

    # return node.properties ['node_id']
    return node

  def get_neighbors_nodes (self, maze_id: str, actual_position: int) -> list[Node]:
    maze = Graph (
      maze_id,
      self.redis_client
    )

    params_graph_query = {
      'id': actual_position
    }

    result = maze.query (
      """MATCH (:node {node_id: $id}) -[:connects]- (n) return n""",
      params_graph_query
    )

    nodes: Node = [node [0] for node in result.result_set]

    # node_ids: list [int] = [node.properties ['node_id'] for node in nodes]
    # node_ids.sort ()

    return nodes
    


