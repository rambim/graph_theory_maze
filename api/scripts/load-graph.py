from redis import Redis
from redisgraph import Node, Edge, Graph
import sys, os

class MazeLoader:

  def __init__ (self,
    GTM_REDIS_HOST: str = os.getenv ('GTM_REDIS_HOST', 'localhost'),
    GTM_REDIS_PORT: int = int (os.getenv ('GTM_REDIS_PORT', 6379))
  ):

    self.redis_cliente = Redis (
      host = GTM_REDIS_HOST,
      port = GTM_REDIS_PORT
    )


  def load_maze (self, maze_id: str, maze_file_path: str):
    graph = Graph (
      maze_id,
      self.redis_cliente
    )

    with open (maze_file_path, 'r') as file:
      for line in file:
        n1, n2 = '', ''

        n1, n2 = line.split (':')

        if n1.strip () == 'start':
          graph.query (
            f'match (n1:node {{node_id: {int (n2.strip ())}}}) set n1.is_start = true'
          )

        elif n1.strip () == 'end':
          graph.query (
            f'match (n1:node {{node_id: {int (n2.strip ())}}}) set n1.is_end = true'
          )

        else:
          graph.query (
            f'merge (n1:node {{is_end: false, is_start: false, node_id: {int (n1.strip ())}}}) merge (n2:node {{is_end: false, is_start: false, node_id: {int (n2.strip ())}}}) create (n1) -[:connects]-> (n2)'
          )




if __name__ == '__main__':
  maze_id = None
  maze_file_path = None
  ml: MazeLoader = None

  if len (sys.argv) == 5:
    redis_host = sys.argv [1]
    redis_port = sys.argv [2]
    maze_id = sys.argv [3]
    maze_file_path = sys.argv [4]

    ml = MazeLoader (
      GTM_REDIS_HOST = redis_host,
      GTM_REDIS_PORT = redis_port
    )

  elif len (sys.argv) == 3:
    maze_id = sys.argv [1]
    maze_file_path = sys.argv [2]
    ml = MazeLoader ()

  else:
    raise Exception ('Incorrect number of arguments. Use `python load-graph.py <redis_host> <redis_port> <maze_id> <maze_file_path>` ou `python load-graph.py <maze_id> <maze_file_path>`')

  try:
    ml.load_maze (
      maze_id = maze_id,
      maze_file_path = maze_file_path
    )

    print (f'{maze_file_path} carregado com sucesso!')
  except Exception as e:
    print (f'Algo deu errado!')
    raise e
