from fastapi import APIRouter, Depends, HTTPException

from api.schemas.command import StartCommand, MoveCommand, ValidatePathCommand
from api.schemas.position import Position
from api.schemas.validate_path_response import ValidatePathResponse
from api.services.graph_service import GraphService
from api.services.session_service import SessionService

command_routes = APIRouter ()

@command_routes.post ("/iniciar")
async def start_maze (
  start_command: StartCommand,
  session_service: SessionService = Depends (SessionService),
  graph_service: GraphService = Depends (GraphService)
  ) -> Position:

  graph_service.verify_maze_exists (start_command.labirinto)
  session_service.create_session (start_command.id, start_command.labirinto)

  start_position = graph_service.get_start_position (start_command.labirinto)

  return start_position



@command_routes.get ("/labirintos")
async def list_mazes (graph_service: GraphService = Depends (GraphService)) -> list [str]:
  print("oi labirintos")
  return graph_service.list_all_mazes ()



@command_routes.post ("/movimentar")
async def move (
  move_command: MoveCommand,
  session_service: SessionService = Depends (SessionService),
  graph_service: GraphService = Depends (GraphService)
) -> Position:

  graph_service.verify_maze_exists (move_command.labirinto)
  actual_position_number: int = session_service.get_actual_position_number_by_session_id (move_command.id, move_command.labirinto)

  if graph_service.is_legal_move (move_command.labirinto, actual_position_number, move_command.nova_posicao):
    session_service.update_session_actual_position (move_command.id, move_command.labirinto, move_command.nova_posicao)

  else:
    # TODO: Raise specific exception and tranfer the logic of response to the controler
    raise HTTPException (status_code = 403, detail = 'Movimento ilegal!')

  actual_position_number: int = session_service.get_actual_position_number_by_session_id (move_command.id, move_command.labirinto)
  position = graph_service.get_actual_position (actual_position_number, move_command.labirinto)

  return position



@command_routes.post ("/validar_caminho")
async def validate_path (
  validate_path_command: ValidatePathCommand,
  session_service: SessionService = Depends (SessionService),
  graph_service: GraphService = Depends (GraphService)
) -> ValidatePathResponse:

  graph_service.verify_maze_exists (validate_path_command.labirinto)
  session_service.verify_session_exists (validate_path_command.id + validate_path_command.labirinto)

  is_path_valid = True

  # Save current position before validation
  original_position = session_service.get_actual_position_number_by_session_id(
    validate_path_command.id,
    validate_path_command.labirinto
  )

  # Move to start position without creating a new session
  first_move = validate_path_command.todos_movimentos.pop(0)
  last_move = validate_path_command.todos_movimentos.pop()
  start_node = graph_service.get_start_position(validate_path_command.labirinto)
  
  if first_move != start_node.pos_atual:
    is_path_valid = False
  else:
    move_command = MoveCommand(
      id=validate_path_command.id,
      labirinto=validate_path_command.labirinto,
      nova_posicao=first_move
    )
    session_service.update_session_actual_position(
      move_command.id,
      move_command.labirinto,
      move_command.nova_posicao
    )

    try:
      for position in validate_path_command.todos_movimentos:
        move_command.nova_posicao = position
        await move(move_command, session_service, graph_service)

      move_command.nova_posicao = last_move
      last_node = await move(move_command, session_service, graph_service)
      if last_node.final is False:
        is_path_valid = False

    except HTTPException:
      is_path_valid = False

  # Return to original position before validation
  session_service.update_session_actual_position(
    validate_path_command.id,
    validate_path_command.labirinto,
    original_position
  )
  
  # +2 -> Add first and last move back to total
  moves_count: int = len (validate_path_command.todos_movimentos) + 2

  return ValidatePathResponse (caminho_valido = is_path_valid, quantidade_movimentos = moves_count)

