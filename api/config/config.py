import os

TIME_IN_SEC = 60 * 5

class Config:
  GTM_REDIS_HOST: str = os.getenv ('GTM_REDIS_HOST', 'localhost')
  GTM_REDIS_PORT: int = int (os.getenv ('GTM_REDIS_PORT', 6379))
  GTM_SESSION_TTL: int = int (os.getenv ('GTM_SESSION_TTL', TIME_IN_SEC))