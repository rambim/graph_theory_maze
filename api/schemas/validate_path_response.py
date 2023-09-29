from pydantic import BaseModel

class ValidatePathResponse (BaseModel):
  caminho_valido: bool
  quantidade_movimentos: int