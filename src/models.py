from pydantic import BaseModel

class Command (BaseModel):
  id: str
  labirinto: str

class StartCommand (Command):
  pass

class MoveCommand (Command):
  nova_posicao: int

class ValidatePathCommand (Command):
  todos_movimentos: list [int]

class Position (BaseModel):
  pos_atual: int
  inicio: bool
  final: bool
  movimentos: list [int]

class ValidatePathResponse (BaseModel):
  caminho_valido: bool
  quantidade_movimentos: int
