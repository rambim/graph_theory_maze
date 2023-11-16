from fastapi import Depends, HTTPException

from api.repository.session_repository import ISessionRepository, RedisSessionRespositoryImpl
from api.config.config import Config
from api.services.graph_service import GraphService


class SessionService:

  def __init__ (self,
    session_repository: ISessionRepository = Depends (RedisSessionRespositoryImpl),
    graph_service: GraphService = Depends (GraphService),
    app_config: Config = Depends (Config)
  ):
    self.session_repository = session_repository
    self.graph_service = graph_service
    self.app_config = app_config


  def create_session (self, session_id: str, maze_id: str, final_position: int):
    # TODO: Refact: remove usage of graph_service from here.
    start_position = self.graph_service.get_start_position (maze_id = maze_id)

    self.session_repository.create_session (
      session_id,
      maze_id,
      self.app_config.GTM_SESSION_TTL,
      actual_position = start_position.pos_atual,
      final_position = final_position
    )

  
  def get_actual_position_number_by_session_id (self, session_id: str, maze_id: str) -> int:
    session_data: dict = self.verify_session_exists (session_id + maze_id)

    return int (session_data ['actual_position'])
  

  def get_final_position_number_by_session_id (self, session_id: str, maze_id: str) -> int:
    session_data: dict = self.verify_session_exists (session_id + maze_id)

    return int (session_data ['final_position'])


  def update_session_actual_position (self, session_id: str, maze_id: str, new_position: int) -> None:
    self.verify_session_exists (session_id + maze_id)
    self.session_repository.update_actual_node (session_id, maze_id, new_position)


  def verify_session_exists (self, session_id: str) -> dict | None:
    session: dict = self.session_repository.get_session_by_id (session_id)

    if session == {} or session is None: raise HTTPException (status_code = 404, detail = 'ID não encontrado para o labirinto em questão ou está expirado!')

    return session
