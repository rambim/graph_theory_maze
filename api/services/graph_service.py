import random
from fastapi import Depends, HTTPException
from redisgraph import Node

from api.repository.graph_repository import IGraphRepository, RedisGraphRespoistoryImpl
from api.schemas.position import Position
from api.config.config import Config

class GraphService:

  def __init__ (self,
    graph_repository: IGraphRepository = Depends (RedisGraphRespoistoryImpl),
    app_config: Config = Depends (Config)
  ):
    self.graph_repository = graph_repository
    self.app_config = app_config



  def get_start_position (self, maze_id: str) -> Position:

    start_node: Node = self.graph_repository.get_start_node (maze_id = maze_id)

    neighbors_list: list [int] = self.__get_neighbors_list (maze_id, start_node.properties ['node_id'])

    return Position (
      pos_atual = start_node.properties ['node_id'],
      inicio = start_node.properties ['is_start'],
      final = start_node.properties ['is_end'],
      movimentos = neighbors_list
    )



  def get_actual_position (self, actual_position_number: int, maze_id: str) -> Position:
    node: Node = self.graph_repository.get_node_by_node_number (actual_position_number, maze_id)
    neighbors_list: list [int] = self.__get_neighbors_list (maze_id, node.properties ['node_id'])

    return Position (
      pos_atual = actual_position_number,
      inicio = node.properties ['is_start'],
      final = node.properties ['is_end'],
      movimentos = neighbors_list
    )



  def list_all_mazes (self) -> list [str]:
    return [maze for maze in self.graph_repository.list_all_graphs ()]



  def is_legal_move (self, maze_id: str, actual_position_number: int, new_position: int) -> bool:

    neighbors_list = self.__get_neighbors_list (maze_id, actual_position_number)

    return True if new_position in neighbors_list else False



  def verify_maze_exists (self, maze_id: str):
    mazes = self.list_all_mazes ()

    if maze_id not in mazes: raise HTTPException (status_code = 404, detail = 'Labirinto não encontrado.')



  def __get_neighbors_list (self, maze_id: str, actual_position_number: int) -> list [int]:
    actual_position_number = int (actual_position_number)

    neighbors: list [Node] = self.graph_repository.get_neighbors_nodes (maze_id, actual_position_number)

    return sorted ([int (node.properties ['node_id']) for node in neighbors])


  def validate_path (self, maze_id: str, moves: list [int]) -> bool:
    paths: list [list [int]] = self.graph_repository.get_all_valid_paths (maze_id)

    return True if moves in paths else False
  
  def set_final_position(self, maze_id: str, final_position: int) -> int:
    all_nodes = self.graph_repository.get_all_nodes(maze_id)
    start_position = self.get_start_position(maze_id)

    if final_position == 0:
      # Random position
      while True:
        random_position = random.choice(all_nodes)
        if random_position != start_position.pos_atual:
          return random_position

    # Check whether final position is valid
    if (final_position in all_nodes) and (final_position != start_position.pos_atual):
      return final_position
    else:
      raise HTTPException(status_code = 403, detail = "Posição final inválida!")