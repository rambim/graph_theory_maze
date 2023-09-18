# from pydantic_settings import BaseSettings

TIME_IN_SEC = 60 * 5

class Config:
  GTM_REDIS_HOST: str = 'localhost'
  GTM_REDIS_PORT: int = 6379
  GTM_SESSION_TTL: int = TIME_IN_SEC