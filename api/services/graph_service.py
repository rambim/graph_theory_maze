from repository.graph_repository import IGraphRepository, RedisGraphRespoistoryImpl
from schemas.position import Position
from redisgraph import Node
from config.config import Config

from fastapi import Depends

class GraphService:
  def __init__ (self,
    graph_repository: IGraphRepository = Depends (RedisGraphRespoistoryImpl),
    app_config: Config = Depends (Config)
  ):
    self.graph_repository = graph_repository
    self.app_config = app_config

  def get_start_position (self, maze_id: str) -> Position:
    # TODO: Verify if maze exists
    start_position: Node = self.graph_repository.get_start_node (maze_id = maze_id)
    neighbors: list [Node] = self.graph_repository.get_neighbors_nodes (maze_id, start_position.properties ['node_id'])

    return Position (
      pos_atual = start_position.properties ['node_id'],
      inicio = start_position.properties ['is_start'],
      final = start_position.properties ['is_end'],
      movimentos = sorted ([node.properties ['node_id'] for node in  neighbors])
    )




