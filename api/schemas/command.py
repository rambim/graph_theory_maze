from pydantic import BaseModel

class Command (BaseModel):
  id: str
  labirinto: str

class StartCommand (Command):
  pass

class StartCustomCommand (StartCommand):
  pos_final: int

class MoveCommand (Command):
  nova_posicao: int

class ValidatePathCommand (Command):
  todos_movimentos: list [int]
