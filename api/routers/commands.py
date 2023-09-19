from fastapi import APIRouter, Depends

from api.schemas.command import StartCommand
from api.schemas.position import Position
from api.services.graph_service import GraphService
from api.services.session_service import SessionService

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


@command_routes.get ("/labirintos")
async def list_mazes (graph_service: GraphService = Depends (GraphService)) -> list [str]:
  return graph_service.list_all_graphs ()


# @router.post ("/movimentar")
# async def move (move_command: MoveCommand) -> Position:
#   node = service.move (move_command.labirinto, move_command.nova_posicao)

#   return node

 