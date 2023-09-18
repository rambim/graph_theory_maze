from fastapi import Depends

from api.repository.session_repository import ISessionRepository, RedisSessionRespositoryImpl
from api.config.config import Config


class SessionService:

  def __init__ (self,
    session_repository: ISessionRepository = Depends (RedisSessionRespositoryImpl),
    app_config: Config = Depends (Config)
  ):
    self.session_repository = session_repository
    self.app_config = app_config

  def create_session (self, session_id: str, maze_id: str):
    self.session_repository.create_session (session_id, maze_id, self.app_config.GTM_SESSION_TTL)