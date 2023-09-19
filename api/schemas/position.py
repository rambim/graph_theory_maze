from pydantic import BaseModel

class Position (BaseModel):
  pos_atual: int
  inicio: bool
  final: bool
  movimentos: list [int]