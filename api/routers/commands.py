from fastapi import APIRouter, Depends
from schemas.command import StartCommand, MoveCommand
from schemas.position import Position
from services.graph_service import GraphService
from services.session_service import SessionService

command_routes = APIRouter ()

@command_routes.post ("/iniciar")
async def start_maze (
  start_command: StartCommand,
  session_service: SessionService = Depends (SessionService),
  graph_service: GraphService = Depends (GraphService)
  ) -> Position:

  session_service.create_session (start_command.id, start_command.labirinto)
  start_position = graph_service.get_start_position (start_command.labirinto)

  return start_position




# @router.post ("/movimentar")
# async def move (move_command: MoveCommand) -> Position:
#   node = service.move (move_command.labirinto, move_command.nova_posicao)

#   return node

 