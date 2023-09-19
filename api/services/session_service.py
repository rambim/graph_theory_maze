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

  def create_session (self, session_id: str, maze_id: str):
    # TODO: Refact: remove usage of graph_service from serssion_service
    start_position = self.graph_service.get_start_position (maze_id = maze_id)
    
    self.session_repository.create_session (session_id, maze_id, self.app_config.GTM_SESSION_TTL, actual_position = start_position.pos_atual)

  def get_actual_position_number_by_session_id (self, session_id: str, maze_id: str) -> int:
    
    session_data: dict = self.session_repository.get_session_by_id (session_id = session_id, maze_id = maze_id)

    print (session_data)

    if session_data == {} or session_data is None: raise HTTPException (status_code = 404, detail = 'ID não encontrado ou expirado!')
    
    return int (session_data ['actual_position'])

  def update_session_actual_position (self, session_id: str, maze_id: str, new_position: int) -> int:
    print (self.session_repository.update_actual_node (session_id, maze_id, new_position))